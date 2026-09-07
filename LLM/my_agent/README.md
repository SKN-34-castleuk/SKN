# 📄 논문 Q&A 에이전트

arXiv 논문을 대량으로 수집해 Pinecone 벡터 DB에 적재하고, 질문에 따라 **스스로 검색 도구를 골라 호출**해
논문 내용을 근거로 답하는 RAG 에이전트입니다. Streamlit 채팅 UI를 포함합니다.

- **적재된 논문**: 245편 / 18,176 청크 (자연어처리·LLM 6주제, 금융·투자 6주제)
- **스택**: LangChain · LangGraph · OpenAI · Pinecone · Cohere Rerank · Streamlit

---

## 구조

| 파일 | 역할 |
|---|---|
| `ingest.py` | 논문 수집·적재. 주제별 arXiv 검색 → PDF → 청킹 → Pinecone |
| `papers.json` | 적재된 논문 매니페스트. `ingest.py`가 갱신, 나머지가 읽음 |
| `paper_agent.py` | 검색 도구 7종 + 에이전트 정의 (UI와 분리된 순수 로직) |
| `app.py` | Streamlit 채팅 UI |
| `paper_agent.ipynb` | 각 단계의 원리를 설명하는 노트북 |

적재(쓰기)와 질의(읽기)를 파일 단위로 분리한 이유는 **Streamlit이 위젯을 조작할 때마다 스크립트를
처음부터 다시 실행**하기 때문입니다. 적재 코드가 `app.py`에 있으면 메시지를 보낼 때마다 논문을 다시
임베딩해 중복이 쌓입니다.

```
                    ┌──────────────┐
   arXiv ──────────▶│  ingest.py   │──────▶ Pinecone (18,176 벡터)
   (주제별 검색)      └──────┬───────┘         └── 임베딩 + 청크 원문 + 메타데이터
                           │
                           ▼
                     papers.json  ◀────────┐
                                           │ 논문 목록 조회
   질문 ──▶ app.py ──▶ paper_agent.py ─────┘
                            │
                            ├── 저장된 논문: 벡터 검색 20개 → 리랭킹 → 4개
                            └── 외부 검색: arXiv / HuggingFace Daily Papers
```

---

## 빠른 시작

### 1. 설치

```bash
pip install -U langchain langchain-openai langchain-pinecone langchain-text-splitters \
    pinecone python-dotenv arxiv pymupdf requests cohere streamlit
```

### 2. API 키

프로젝트 루트(`SKN/LLM/`)의 `.env`에 다음을 넣습니다.

```
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
COHERE_API_KEY=...        # 선택 — 없으면 리랭킹을 건너뜁니다
```

### 3. 논문 적재

```bash
python ingest.py              # 주제당 10편씩, 아직 없는 논문만 적재
python ingest.py --per 20     # 주제당 20편씩
python ingest.py --reset      # 인덱스를 비우고 처음부터
```

논문을 늘리려면 `ingest.py`의 `TOPICS`에 주제와 arXiv 검색식을 추가하고 다시 실행하면 됩니다.
이미 적재된 논문은 건너뛰므로 추가된 만큼만 시간이 걸립니다.

### 4. 실행

```bash
streamlit run app.py
```

---

## 검색 도구

에이전트는 도구의 **이름과 docstring을 읽고** 언제 쓸지 스스로 판단합니다.

### 저장된 논문 — 본문까지 읽을 수 있음

| 도구 | 역할 |
|---|---|
| `search_papers(query, topic="")` | 저장된 논문에서 검색. `topic`으로 주제 한정 |
| `search_in_paper(query, paper_id)` | 특정 논문 안에서만 검색 (논문 비교에 사용) |
| `find_paper(keyword)` | 제목·주제 키워드로 arXiv 번호 찾기 |
| `list_papers()` | 주제별 편수 요약 |

### 저장되지 않은 논문 — 제목·초록만 확인 가능

| 도구 | 신호 | 출처 |
|---|---|---|
| `trending_papers(limit)` | **추천 수**(화제성) | Hugging Face Daily Papers |
| `latest_papers(category, keyword)` | **등록일**(분야별 최신) | arXiv `cat:` 분류 |
| `search_new_papers(keyword)` | **주제 관련도** | arXiv 초록 검색 |

> "요즘 핫한 논문"과 "최신 논문"은 다른 질문입니다. arXiv는 인용수·조회수 같은 인기 지표를
> 제공하지 않아 **최신순**만 알 수 있습니다. 화제성은 연구자들이 직접 추천을 누르는
> Hugging Face Daily Papers에서 가져오는데, 이쪽은 AI·머신러닝에 치우쳐 있어서
> 금융 등 다른 분야의 동향은 `latest_papers`로 봐야 합니다.

---

## LangGraph는 어디에 쓰였나

`StateGraph`로 그래프를 직접 조립하지는 않았지만, **에이전트 루프 자체가 LangGraph 위에서 돕니다.**
`langchain.agents.create_agent`가 반환하는 것은 컴파일된 LangGraph 그래프입니다.

```python
>>> type(agent)
langgraph.graph.state.CompiledStateGraph
>>> agent.get_graph().nodes
['__start__', 'model', 'tools', '__end__']
```

```
__start__ ──▶ model ──┬──▶ tools ──┐
                      │            │  (도구 결과를 들고 다시 판단)
                      │            ▼
                      │          model
                      └──▶ __end__      (도구가 더 필요 없으면 종료)
```

이 구조를 직접 쓰는 부분이 세 군데 있습니다.

- **`InMemorySaver` (checkpointer)** — `langgraph.checkpoint.memory`. `thread_id`별로 대화 이력을
  저장해 후속 질문("그건 왜 그래?")을 이해하게 합니다.
- **`agent.stream(stream_mode=["updates", "messages"])`** — LangGraph의 스트리밍 API입니다.
  `updates`는 노드가 끝날 때마다 상태 변화를, `messages`는 토큰을 흘려보냅니다.
  `app.py`는 전자로 도구 호출을 실시간 표시하고, 후자로 답변을 한 글자씩 그립니다.
- **노드 이름** — `app.py`가 `meta["langgraph_node"] == "model"`로 필터링해 도구 실행 중의
  중간 출력이 아니라 최종 답변 토큰만 화면에 그립니다.

즉 **"어떤 도구를 언제 부를지"의 판단은 LLM에게 맡기고**, 그 판단을 실행하는 루프·상태 관리·스트리밍을
LangGraph가 담당합니다. 검색 결과를 평가해 질문을 재작성하는 식으로 흐름을 직접 설계하려면
그때는 `StateGraph`로 그래프를 조립하게 됩니다(아래 확장 아이디어의 Agentic RAG).

---

## 검색 전략

논문이 수백 편이 되면 벡터 유사도만으로는 엉뚱한 분야의 청크가 상위에 올라옵니다. 2단계로 검색합니다.

```
질문 → 벡터 검색 20개 (CANDIDATE_K) → Cohere 리랭킹 → 논문당 최대 2개 → 상위 4개 (FINAL_K)
```

- **리랭킹** — 벡터 검색은 질문과 청크를 *각각 따로* 벡터로 만들어 비교하지만, 리랭커는 둘을
  *함께 읽고* 점수를 매기므로 훨씬 정확합니다. 대신 느리고 비용이 들어서 후보를 줄인 뒤 적용합니다.
  `COHERE_API_KEY`가 없거나 호출이 실패하면 벡터 검색 순서를 그대로 씁니다.
- **논문당 상한** — 한 논문이 결과 4개를 독점하면 비교 질문에 답할 수 없습니다. 관련도 순서는
  유지하되 같은 논문의 청크가 2개를 넘으면 뒤로 미룹니다.

---

## Pinecone에 저장되는 것

벡터 1건 = `1536차원 임베딩` + `메타데이터`이고, 메타데이터에 **청크 원문(`text`)** 이 함께 들어갑니다.
그래야 검색 결과를 `page_content`로 돌려줄 수 있습니다. 즉 논문 본문은 청크 단위로 쪼개져
Pinecone에 그대로 보관되며, 이 덕분에 `app.py`는 PDF를 다시 받지 않아도 동작합니다.

```jsonc
{
  "id": "3f1a…",                  // 청크 내용의 SHA-1 (결정론적)
  "values": [0.009, -0.0007, …],  // 1536차원
  "metadata": {
    "text": "…청크 원문 1000자…",
    "title": "Attention Is All You Need",
    "paper_id": "1706.03762",
    "topic": "트랜스포머·언어모델",
    "authors": "…", "published": "2017-06-12"
  }
}
```

**검색은 읽기 전용입니다.** 질문·답변·대화 내용은 Pinecone에 저장되지 않습니다. 검색할 때는 질문을
임베딩해 쿼리로 보내고 유사한 청크를 돌려받을 뿐입니다. 대화 기억은 `InMemorySaver`가 파이썬 프로세스
메모리에 들고 있는 것이라 재시작하면 사라집니다.

---

## 겪었던 문제와 해결

| 문제 | 원인 | 해결 |
|---|---|---|
| `AttributeError: 'Search' object has no attribute 'results'` | `langchain_community`의 `ArxivLoader`가 `arxiv` 2.0에서 제거된 API를 호출 | `arxiv` 4.x API(`Client().results()`)로 직접 로드 |
| `400 Function tools with reasoning_effort are not supported` | 추론 모델은 도구를 붙이면 Chat Completions API를 못 씀 | `ChatOpenAI(..., use_responses_api=True)` |
| 같은 청크가 2번씩 검색됨 | 적재 셀을 두 번 실행 → 매번 새 UUID 발급 | 청크 내용 기반 결정론적 id로 upsert |
| 답변이 문자열이 아니라 리스트 | Responses API는 `content`가 블록 리스트(추론+답변) | `message.text`로 본문만 추출 |
| 도구 호출 로그가 턴마다 누적 | checkpointer 때문에 이전 턴 메시지까지 순회 | 마지막 `HumanMessage` 이후만 확인 |
| arXiv 429로 앱이 아예 안 뜸 | 시작 경로에서 arXiv로 논문 제목 조회 | 제목을 `papers.json`에서 읽고, 외부 호출은 도구 안에서만 |
| `id_list`로 여러 논문을 한 번에 조회하면 429 | 주제 검색은 통과하는데 `id_list` 일괄 조회만 거부됨 | 고정 논문은 하나씩 조회 (`ingest.py`) |

---

## 확장 아이디어

- 섹션(Abstract/Method/Experiments) 인식 청킹 → 참고문헌 목록이 검색되는 문제 완화
- 하이브리드 검색(키워드 + 벡터)으로 고유명사·수식 검색 정확도 향상
- Agentic RAG 그래프 — 검색 결과를 평가해 부적합하면 질문을 재작성하고 재검색
- 에이전트가 직접 논문을 적재하는 도구 + 승인 미들웨어(HITL)
- RAGAS 등으로 답변 정확도·근거 충실도 평가
