"""논문 수집 · 적재 스크립트 (한 번 실행하면 새로 추가된 논문만 적재).

    python ingest.py              # 주제 목록대로 수집 후, 아직 없는 논문만 적재
    python ingest.py --per 20     # 주제당 20편씩 수집
    python ingest.py --reset      # 인덱스를 비우고 처음부터 다시 적재

논문 목록은 papers.json(매니페스트)에 기록됩니다. 앱과 노트북은 이 파일을 읽으므로
논문 번호를 코드에 손으로 적어둘 필요가 없습니다.
"""

import argparse
import hashlib
import json
import time
from pathlib import Path

import arxiv
import pymupdf
import requests
from dotenv import find_dotenv, load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

load_dotenv(find_dotenv())

INDEX_NAME = "paper-agent"
EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536
MANIFEST = Path(__file__).with_name("papers.json")

# 주제 → arXiv 검색식. 주제를 추가하면 다음 실행 때 그만큼 논문이 늘어납니다.
TOPICS = {
    "트랜스포머·언어모델": 'abs:"transformer" AND abs:"language model" AND cat:cs.CL',
    "RAG·검색증강생성": 'abs:"retrieval-augmented generation"',
    "LLM 에이전트·도구사용": 'abs:"language model" AND abs:"agent" AND abs:"tool"',
    "인컨텍스트 학습·프롬프팅": 'abs:"in-context learning" AND cat:cs.CL',
    "효율적 파인튜닝": 'abs:"parameter-efficient fine-tuning" OR abs:"low-rank adaptation"',
    "환각·사실성 평가": 'abs:"hallucination" AND abs:"language model"',
    "포트폴리오 최적화": 'abs:"portfolio optimization" AND cat:q-fin.*',
    "강화학습 트레이딩": 'abs:"reinforcement learning" AND abs:"trading"',
    "주가 예측": 'abs:"stock" AND abs:"prediction" AND cat:q-fin.*',
    "금융 LLM·NLP": 'abs:"large language model" AND cat:q-fin.*',
    "금융 감성분석": 'abs:"sentiment analysis" AND abs:"financial"',
    "금융 리스크·변동성": 'abs:"volatility" AND abs:"machine learning" AND cat:q-fin.*',
}

# 주제 검색 결과와 무관하게 항상 포함할 논문 (기초·대표 논문은 관련도 상위에 안 뜰 수 있음)
SEED_IDS = {
    "1706.03762": "트랜스포머·언어모델",      # Attention Is All You Need
    "1810.04805": "트랜스포머·언어모델",      # BERT
    "2005.11401": "RAG·검색증강생성",         # Retrieval-Augmented Generation
    "2312.14203": "금융 LLM·NLP",             # Shai: 자산운용 특화 LLM
    "2601.07942": "포트폴리오 최적화",         # 딥러닝 포트폴리오 최적화
    "2502.00828": "포트폴리오 최적화",         # LLM 결합 의사결정 신경망
    "2304.06037": "강화학습 트레이딩",         # Deep Q-Learning 퀀트 트레이딩
    "2002.06975": "주가 예측",                # 딥러닝 횡단면 주가 예측
    "2510.15929": "금융 감성분석",            # 금융 뉴스 감성분석 LLM 비교
}

_client = arxiv.Client(page_size=100, delay_seconds=3.0, num_retries=3)


def load_manifest() -> dict:
    """지금까지 적재한 논문 목록을 읽습니다."""
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {}


def save_manifest(manifest: dict) -> None:
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _to_meta(result, topic: str) -> dict:
    return {
        "paper_id": result.get_short_id().split("v")[0],
        "title": result.title.replace("\n", " ").strip(),
        "authors": ", ".join(a.name for a in result.authors)[:200],
        "published": str(result.published.date()),
        "category": result.primary_category,
        "topic": topic,
        "pdf_url": result.pdf_url,
    }


def collect_candidates(per_topic: int) -> dict:
    """고정 논문 + 주제별 arXiv 검색 결과의 메타데이터를 모읍니다."""
    found = {}

    # 고정 논문은 하나씩 조회합니다.
    # id_list에 여러 개를 한 번에 넣으면 arXiv가 429로 거부하는 경우가 있습니다.
    for pid, topic in SEED_IDS.items():
        try:
            r = next(_client.results(arxiv.Search(id_list=[pid])))
            found[r.get_short_id().split("v")[0]] = _to_meta(r, topic)
        except Exception as e:
            print(f"  [건너뜀] 고정 논문 {pid} 조회 실패 ({str(e)[:60]})")
        time.sleep(1)
    print(f"  고정 논문: {len(found)}편")

    for topic, query in TOPICS.items():
        try:
            search = arxiv.Search(query=query, max_results=per_topic,
                                  sort_by=arxiv.SortCriterion.Relevance)
            results = list(_client.results(search))
        except Exception as e:
            print(f"  [건너뜀] {topic}: 검색 실패 ({e})")
            continue
        for r in results:
            pid = r.get_short_id().split("v")[0]
            if pid in found:            # 여러 주제에 걸친 논문은 처음 주제로 분류
                continue
            found[pid] = _to_meta(r, topic)
        print(f"  {topic}: {len(results)}편")
    return found


def fetch_text(pdf_url: str) -> str:
    """PDF를 내려받아 페이지별 텍스트를 이어붙입니다."""
    pdf_bytes = requests.get(pdf_url, timeout=90).content
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as pdf:
        return "\n".join(page.get_text() for page in pdf)


def chunk_id(chunk) -> str:
    """청크 내용 기반 결정론적 id (재실행해도 중복되지 않도록)."""
    key = f"{chunk.metadata['paper_id']}:{chunk.page_content}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()


def ensure_index(pc: Pinecone) -> None:
    if INDEX_NAME not in [i["name"] for i in pc.list_indexes()]:
        pc.create_index(name=INDEX_NAME, dimension=EMBED_DIM, metric="cosine",
                        spec=ServerlessSpec(cloud="aws", region="us-east-1"))
        while not pc.describe_index(INDEX_NAME).status["ready"]:
            time.sleep(1)
        print("인덱스 생성 완료")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per", type=int, default=10, help="주제당 수집할 논문 수")
    ap.add_argument("--reset", action="store_true", help="인덱스를 비우고 처음부터")
    args = ap.parse_args()

    pc = Pinecone()
    ensure_index(pc)
    index = pc.Index(INDEX_NAME)

    manifest = {} if args.reset else load_manifest()
    if args.reset:
        print("인덱스를 비우는 중...")
        index.delete(delete_all=True)
        save_manifest({})

    print(f"\n[1/3] arXiv에서 주제별 {args.per}편씩 수집")
    candidates = collect_candidates(args.per)
    todo = {pid: m for pid, m in candidates.items() if pid not in manifest}
    print(f"\n후보 {len(candidates)}편 / 이미 적재됨 {len(candidates) - len(todo)}편 "
          f"/ 새로 적재할 논문 {len(todo)}편")
    if not todo:
        print("추가할 논문이 없습니다.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    store = PineconeVectorStore(index_name=INDEX_NAME,
                                embedding=OpenAIEmbeddings(model=EMBED_MODEL))

    print(f"\n[2/3] PDF 다운로드 → 청킹 → 업로드")
    ok = fail = total_chunks = 0
    for n, (pid, meta) in enumerate(sorted(todo.items()), 1):
        try:
            text = fetch_text(meta["pdf_url"])
            if len(text) < 3000:        # 본문 추출이 사실상 실패한 경우(스캔 PDF 등)
                raise ValueError(f"본문이 너무 짧음 ({len(text)}자)")

            doc = Document(page_content=text, metadata={
                "paper_id": pid, "Title": meta["title"], "Authors": meta["authors"],
            })
            chunks = splitter.split_documents([doc])
            for c in chunks:            # Pinecone은 문자열/숫자/불리언/문자열리스트만 허용
                c.metadata = {
                    "title": meta["title"],
                    "paper_id": pid,
                    "authors": meta["authors"],
                    "topic": meta["topic"],
                    "published": meta["published"],
                }
            store.add_documents(chunks, ids=[chunk_id(c) for c in chunks])

            meta = {k: v for k, v in meta.items() if k != "pdf_url"}
            meta["chunks"] = len(chunks)
            manifest[pid] = meta
            total_chunks += len(chunks)
            ok += 1
            print(f"  [{n}/{len(todo)}] ✔ {pid} {meta['title'][:52]} ({len(chunks)}청크)")
        except Exception as e:
            fail += 1
            print(f"  [{n}/{len(todo)}] ✘ {pid} 실패: {str(e)[:70]}")
        finally:
            save_manifest(manifest)     # 중간에 끊겨도 진행 상황이 남도록 매번 저장
            time.sleep(1)               # arXiv에 부담을 주지 않도록

    print(f"\n[3/3] 완료 — 성공 {ok}편 / 실패 {fail}편 / 새 청크 {total_chunks:,}개")
    print(f"매니페스트: 논문 {len(manifest)}편  ({MANIFEST})")
    time.sleep(5)
    print("인덱스 벡터 수:", index.describe_index_stats()["total_vector_count"])


if __name__ == "__main__":
    main()
