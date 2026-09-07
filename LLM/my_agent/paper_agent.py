"""논문 Q&A 에이전트 로직 (UI와 분리된 순수 로직 모듈).

논문 수집·적재는 ingest.py가 담당하고, 이 모듈은 이미 만들어진 인덱스에 연결만 합니다.
Streamlit은 위젯을 조작할 때마다 스크립트를 처음부터 다시 실행하기 때문에,
적재 코드가 여기 있으면 메시지를 보낼 때마다 논문이 다시 저장됩니다.
"""

import json
import os
import urllib.request
from collections import Counter
from pathlib import Path

import arxiv
from dotenv import find_dotenv, load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv(find_dotenv())   # 상위 폴더의 .env에서 API 키 로드

INDEX_NAME = "paper-agent"
CHAT_MODEL = "gpt-5.6-luna"
EMBED_MODEL = "text-embedding-3-small"
RERANK_MODEL = "rerank-v3.5"

CANDIDATE_K = 20   # 벡터 검색으로 넓게 뽑고
FINAL_K = 4        # 리랭커로 좁힙니다

MANIFEST = Path(__file__).with_name("papers.json")

SYSTEM_PROMPT = """당신은 논문 읽기를 도와주는 연구 조교 에이전트입니다.
저장된 논문은 자연어처리·LLM(트랜스포머, RAG, 에이전트, 파인튜닝, 환각 평가)과
금융·투자(포트폴리오, 트레이딩, 주가예측, 금융 LLM, 감성분석, 리스크) 분야입니다.

규칙:
1. 저장된 논문의 내용에 관한 질문은 검색 도구로 먼저 확인한 뒤, 검색된 내용에 근거해서만 답하세요.
   - 주제 전반에서 찾을 때: search_papers (topic을 지정하면 해당 주제로 범위를 좁힙니다)
   - 특정 논문을 지정하거나 논문끼리 비교할 때: find_paper로 번호를 찾은 뒤 search_in_paper
2. 저장되지 않은 논문을 찾을 때는 목적에 맞는 도구를 고르세요.
   - "요즘 핫한/화제인 논문": trending_papers (추천 수 기준, AI·ML 위주)
   - "OO 분야 최신 논문": latest_papers (분류 코드로 최신순, 금융 등 모든 분야)
   - "OO 주제 논문 찾아줘": search_new_papers (주제 관련도순)
   이 세 도구의 결과는 제목·초록까지만 알 수 있으므로, 본문은 아직 읽을 수 없다고 밝히세요.
3. 답변 끝에 참고한 논문 제목을 '📎 출처:' 형식으로 표시하세요.
4. 검색 결과에 없는 내용은 지어내지 말고 "저장된 논문에서 찾을 수 없습니다"라고 말하세요.
5. 전문용어는 필요하면 한 줄로 쉽게 풀어 설명하세요.
6. 답변은 한국어로 하세요."""

_client = arxiv.Client()


def load_papers() -> dict:
    """적재된 논문 목록(papers.json)을 읽습니다. ingest.py가 갱신합니다."""
    if not MANIFEST.exists():
        return {}
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _get_reranker():
    """Cohere 리랭커. 키가 없거나 패키지가 없으면 None (벡터 검색만 사용)."""
    if not os.getenv("COHERE_API_KEY"):
        return None
    try:
        import cohere

        return cohere.ClientV2(api_key=os.environ["COHERE_API_KEY"])
    except Exception:
        return None


def _limit_per_paper(docs, top_n: int, per_paper: int = 2):
    """한 논문이 검색 결과를 독점하지 않도록 논문당 청크 수를 제한합니다.

    관련도 순서는 그대로 두되, 같은 논문의 청크가 per_paper개를 넘으면 뒤로 미룹니다.
    결과가 모자라면 미뤄둔 청크로 채웁니다.
    """
    picked, spare, counts = [], [], Counter()
    for d in docs:
        pid = d.metadata.get("paper_id")
        if counts[pid] < per_paper:
            picked.append(d)
            counts[pid] += 1
        else:
            spare.append(d)
        if len(picked) == top_n:
            return picked
    return (picked + spare)[:top_n]


def format_hits(results) -> str:
    """검색 결과를 출처와 함께 하나의 문자열로 정리합니다."""
    return "\n\n---\n\n".join(
        f"[출처: {d.metadata.get('title')} ({d.metadata.get('paper_id')})]\n{d.page_content}"
        for d in results
    )


def build_tools(vectorstore, papers: dict):
    """검색 도구를 만듭니다. 벡터스토어와 논문 목록을 클로저로 잡아둡니다."""
    reranker = _get_reranker()

    def rerank(query: str, docs, top_n: int = FINAL_K):
        """넓게 뽑은 후보를 질문과의 관련도로 다시 정렬합니다.

        논문이 수백 편이 되면 벡터 유사도만으로는 엉뚱한 분야의 청크가 상위에 올라옵니다.
        리랭커는 질문과 청크를 함께 읽고 점수를 매기므로 훨씬 정확합니다.
        Cohere를 쓸 수 없으면 벡터 검색 순서를 그대로 사용합니다.
        """
        if not docs:
            return []
        ranked = docs
        if reranker is not None:
            try:
                res = reranker.rerank(model=RERANK_MODEL, query=query,
                                      documents=[d.page_content for d in docs],
                                      top_n=min(len(docs), top_n * 3))
                ranked = [docs[r.index] for r in res.results]
            except Exception:
                pass   # 리랭킹 실패 시 벡터 검색 순서 그대로
        return _limit_per_paper(ranked, top_n)

    @tool
    def search_papers(query: str, topic: str = "") -> str:
        """저장된 논문에서 질문과 관련된 내용을 검색합니다.
        논문의 방법, 실험 결과, 개념 설명 등 논문 내용에 관한 질문에는 이 도구를 먼저 사용하세요.
        topic에 list_papers로 확인한 주제명을 넣으면 그 주제의 논문만 검색합니다.
        검색어는 영어로 작성하면 더 정확합니다."""
        kwargs = {"filter": {"topic": topic}} if topic else {}
        candidates = vectorstore.similarity_search(query, k=CANDIDATE_K, **kwargs)
        if not candidates:
            return ("관련 내용을 찾지 못했습니다."
                    + (f" (topic='{topic}' 필터를 뺀 검색도 시도해보세요)" if topic else ""))
        return format_hits(rerank(query, candidates))

    @tool
    def search_in_paper(query: str, paper_id: str) -> str:
        """특정 논문 안에서만 검색합니다.
        논문이 지정되었거나 논문끼리 비교할 때 논문마다 한 번씩 사용하세요.
        paper_id는 find_paper로 확인한 arXiv 번호(예: 1810.04805)를 그대로 넣으세요."""
        candidates = vectorstore.similarity_search(query, k=CANDIDATE_K,
                                                   filter={"paper_id": paper_id})
        if not candidates:
            return f"arXiv:{paper_id} 에서 관련 내용을 찾지 못했습니다. find_paper로 번호를 확인하세요."
        return format_hits(rerank(query, candidates))

    @tool
    def find_paper(keyword: str) -> str:
        """제목이나 주제에 키워드가 들어간 논문을 찾아 arXiv 번호를 알려줍니다.
        'BERT 논문에서~'처럼 특정 논문을 다뤄야 할 때, search_in_paper에 넣을 번호를 얻는 용도입니다.
        저장된 논문 목록에서만 찾습니다(본문 검색이 아님). 키워드는 영어가 잘 맞습니다."""
        kw = keyword.lower().strip()
        hits = [p for p in papers.values()
                if kw in p["title"].lower() or kw in p.get("topic", "").lower()]
        if not hits:
            return (f"'{keyword}'가 제목에 들어간 저장 논문이 없습니다. "
                    f"내용으로 찾으려면 search_papers를 쓰세요.")
        hits = sorted(hits, key=lambda p: p.get("published", ""), reverse=True)[:15]
        return "\n".join(
            f"- {p['title']} (arXiv:{p['paper_id']}, {p.get('published', '')}, 주제: {p.get('topic', '')})"
            for p in hits
        )

    @tool
    def list_papers() -> str:
        """저장된 논문이 어떤 주제로 몇 편 있는지 알려줍니다.
        '무슨 논문 있어?'처럼 범위를 물으면 사용하세요.
        논문이 많아 전체 제목 대신 주제별 편수와 예시를 보여줍니다.
        특정 논문을 찾으려면 find_paper를 쓰세요."""
        if not papers:
            return "저장된 논문이 없습니다. ingest.py를 실행해 논문을 적재하세요."
        by_topic = Counter(p.get("topic", "기타") for p in papers.values())
        lines = [f"총 {len(papers)}편이 저장되어 있습니다. 주제별 편수:"]
        for topic, n in by_topic.most_common():
            sample = next(p["title"] for p in papers.values() if p.get("topic") == topic)
            lines.append(f"- {topic}: {n}편  (예: {sample[:60]})")
        lines.append("\n특정 논문의 번호가 필요하면 find_paper를 사용하세요.")
        return "\n".join(lines)

    @tool
    def search_new_papers(keyword: str) -> str:
        """아직 저장되지 않은 논문을 arXiv에서 주제로 검색합니다(관련도순).
        저장된 논문에 없는 주제의 논문을 찾아달라고 하면 사용하세요. keyword는 영어로 작성하세요.
        제목과 초록만 얻을 수 있고, 본문 내용은 읽을 수 없습니다."""
        search = arxiv.Search(query=f'abs:"{keyword}"', max_results=5,
                              sort_by=arxiv.SortCriterion.Relevance)
        try:
            found = [r for r in _client.results(search)
                     if r.get_short_id().split("v")[0] not in papers]
        except Exception as e:   # arXiv 장애·429가 답변 전체를 막지 않도록
            return f"arXiv 검색에 실패했습니다({e}). 저장된 논문 안에서 답하거나 잠시 후 다시 시도하세요."
        if not found:
            return f"'{keyword}'로 새로 찾은 논문이 없습니다(이미 저장된 논문일 수 있습니다)."
        return "\n".join(
            f"- {r.title} (arXiv:{r.get_short_id()}, {r.published.date()})\n  {r.summary[:150].strip()}..."
            for r in found
        )

    @tool
    def trending_papers(limit: int = 10) -> str:
        """요즘 화제가 되는 논문을 추천 수 기준으로 알려줍니다.
        '요즘 핫한 논문', '요즘 뜨는 연구'처럼 최신 동향을 물으면 사용하세요.
        Hugging Face Daily Papers 기준이라 AI·머신러닝 분야에 치우쳐 있습니다.
        금융·물리 등 다른 분야의 최신 논문은 latest_papers를 사용하세요."""
        try:
            with urllib.request.urlopen(
                "https://huggingface.co/api/daily_papers?limit=60", timeout=20
            ) as r:
                items = json.load(r)
        except Exception as e:
            return f"화제 논문 목록을 가져오지 못했습니다({e}). latest_papers를 대신 사용하세요."

        ranked = sorted((i["paper"] for i in items),
                        key=lambda p: p.get("upvotes") or 0, reverse=True)[:limit]
        if not ranked:
            return "화제가 된 논문을 찾지 못했습니다."
        return "\n".join(
            f"- 추천 {p.get('upvotes', 0)}회 | {p['title']} "
            f"(arXiv:{p['id']}, {str(p.get('publishedAt', ''))[:10]})"
            f"{' [저장됨]' if p['id'] in papers else ''}\n"
            f"  {(p.get('ai_summary') or p.get('summary') or '')[:160]}..."
            for p in ranked
        )

    @tool
    def latest_papers(category: str = "", keyword: str = "") -> str:
        """특정 분야의 최신 논문을 arXiv에서 등록일 최신순으로 가져옵니다.
        '금융 쪽 최신 논문'처럼 분야를 지정한 최신 동향 질문에 사용하세요.
        category 예시 — q-fin.PM(포트폴리오), q-fin.TR(트레이딩), q-fin.ST(통계적 금융),
        cs.CL(자연어처리), cs.LG(머신러닝), econ.EM(계량경제), q-bio.NC(신경과학), math.PR(확률론).
        category와 keyword는 함께 쓸 수 있고, 최소 하나는 지정해야 합니다."""
        parts = []
        if category:
            parts.append(f"cat:{category}")
        if keyword:
            parts.append(f'abs:"{keyword}"')
        if not parts:
            return "category 또는 keyword 중 하나는 지정해야 합니다."
        try:
            search = arxiv.Search(query=" AND ".join(parts), max_results=6,
                                  sort_by=arxiv.SortCriterion.SubmittedDate)
            results = list(_client.results(search))
        except Exception as e:
            return f"arXiv 검색에 실패했습니다({e})."
        if not results:
            return "해당 조건의 최신 논문을 찾지 못했습니다. 분류 코드나 검색어를 바꿔보세요."
        return "\n".join(
            f"- {r.title} (arXiv:{r.get_short_id()}, {r.published.date()}, {r.primary_category})\n"
            f"  {r.summary[:150].strip()}..."
            for r in results
        )

    return [search_papers, search_in_paper, find_paper, list_papers,
            search_new_papers, trending_papers, latest_papers]


def build_agent():
    """Pinecone 인덱스에 연결하고 에이전트를 만듭니다. (agent, papers)를 반환합니다."""
    papers = load_papers()
    if not papers:
        raise RuntimeError(
            f"논문 목록({MANIFEST.name})이 없습니다. 먼저 `python ingest.py`를 실행하세요."
        )

    vectorstore = PineconeVectorStore(
        index_name=INDEX_NAME,
        embedding=OpenAIEmbeddings(model=EMBED_MODEL),
    )

    # gpt-5.6-luna는 추론 모델이라 도구를 붙이면 Chat Completions API로는 호출할 수 없습니다.
    # (400: "Function tools with reasoning_effort are not supported ... use /v1/responses")
    llm = ChatOpenAI(model=CHAT_MODEL, use_responses_api=True, temperature=0)

    agent = create_agent(
        model=llm,
        tools=build_tools(vectorstore, papers),
        system_prompt=SYSTEM_PROMPT,
        checkpointer=InMemorySaver(),   # thread_id별 대화 기억
    )
    return agent, papers


def token_text(chunk) -> str:
    """스트리밍 청크에서 텍스트만 꺼냅니다 (추론 블록은 빈 문자열이 됩니다)."""
    return str(getattr(chunk, "text", "") or "")
