"""논문 Q&A 에이전트 - Streamlit 채팅 UI.

실행: streamlit run app.py
사전 준비: paper_agent.ipynb를 한 번 실행해 Pinecone 인덱스를 만들어 두세요.
"""

import uuid

import streamlit as st

from collections import Counter

from paper_agent import CHAT_MODEL, build_agent, token_text

st.set_page_config(page_title="논문 Q&A 에이전트", page_icon="📄")

TOOL_LABELS = {
    "search_papers": "논문 전체 검색",
    "search_in_paper": "특정 논문 검색",
    "list_papers": "논문 목록 확인",
    "find_paper": "논문 번호 조회",
    "search_new_papers": "arXiv 주제 검색",
    "trending_papers": "화제의 논문 (추천수)",
    "latest_papers": "분야별 최신 논문",
}


# 위젯을 만질 때마다 스크립트가 재실행되므로, 무거운 객체는 캐시해서 한 번만 만듭니다.
@st.cache_resource(show_spinner="에이전트를 준비하는 중...")
def get_agent():
    return build_agent()


try:
    agent, papers = get_agent()
except Exception as e:
    st.error(f"에이전트를 준비하지 못했습니다: {e}")
    st.info("`.env`의 API 키를 확인하고, `python ingest.py`로 논문을 먼저 적재해주세요.")
    st.stop()

# 대화 상태 (재실행에도 유지되도록 session_state에 보관)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

with st.sidebar:
    st.subheader(f"📚 읽을 수 있는 논문 {len(papers)}편")
    # 논문이 수백 편이라 전부 펼치면 사이드바를 덮으므로 주제별로 접어둡니다.
    by_topic = Counter(p.get("topic", "기타") for p in papers.values())
    newest_first = sorted(papers.values(), key=lambda x: x.get("published", ""), reverse=True)
    for topic, n in by_topic.most_common():
        with st.expander(f"{topic} ({n})"):
            for p in newest_first:
                if p.get("topic") == topic:
                    st.markdown(
                        f"- [{p['title']}](https://arxiv.org/abs/{p['paper_id']})  \n"
                        f"  `{p['paper_id']}` · {p.get('published', '')}"
                    )

    st.divider()
    st.caption(f"모델: `{CHAT_MODEL}`")
    if st.button("🗑️ 새 대화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())   # 새 thread = 기억 초기화
        st.rerun()

st.title("📄 논문 Q&A 에이전트")
st.caption(f"저장된 논문 {len(papers)}편을 검색해 근거와 함께 답합니다. 없는 내용은 지어내지 않습니다.")


def render_steps(steps: list[str]) -> None:
    """에이전트가 호출한 도구 기록을 접이식으로 보여줍니다."""
    if steps:
        with st.expander(f"🔧 도구 호출 {len(steps)}회"):
            for s in steps:
                st.markdown(f"- {s}")


# 이전 대화 다시 그리기
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            render_steps(msg.get("steps", []))
        st.markdown(msg["content"])


def answer(question: str) -> tuple[str, list[str]]:
    """에이전트를 스트리밍 실행하면서 도구 호출과 답변을 실시간으로 그립니다."""
    status = st.status("생각하는 중...", expanded=True)
    body = st.empty()
    text, steps = "", []

    stream = agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": st.session_state.thread_id}},
        stream_mode=["updates", "messages"],   # updates=도구 호출, messages=토큰
    )

    for mode, payload in stream:
        if mode == "updates":
            for update in payload.values():
                for m in (update.get("messages", []) if isinstance(update, dict) else []):
                    for tc in getattr(m, "tool_calls", None) or []:
                        label = TOOL_LABELS.get(tc["name"], tc["name"])
                        arg = " / ".join(f"{k}: {v}" for k, v in tc["args"].items())
                        step = f"**{label}** — {arg}" if arg else f"**{label}**"
                        steps.append(step)
                        status.markdown(f"🔧 {step}")
        else:
            chunk, meta = payload
            if meta.get("langgraph_node") == "model":
                text += token_text(chunk)
                if text:
                    body.markdown(text)

    status.update(label=f"완료 — 도구 {len(steps)}회 호출", state="complete", expanded=False)
    return text, steps


if question := st.chat_input("논문에 대해 물어보세요"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            text, steps = answer(question)
        except Exception as e:
            st.error(f"답변 생성 중 오류가 발생했습니다: {e}")
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": text, "steps": steps})
