import os
from typing import Dict, List, Optional  # 타입 힌트 작성
from dotenv import load_dotenv  # .env
from langchain_openai import ChatOpenAI  # OpenAI 채팅 모델
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 프롬프트 템플릿 구성요소
from langchain_core.runnables.history import RunnableWithMessageHistory  # 대화 이력 포함한 실행 객체
# 메모리 기반 대화 이력 저장소, 대화 이력 기본 타입
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
import logging  # 로그 출력 기능

load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)  # INFO 레벨 이상 로그 출력
logger = logging.getLogger(__name__)  # 현재 모듈용 로거 생성

# OpenAI 및 Langchain 채팅 서비스
class LangChainChatService:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY를 등록해 주세요!")

        self.model_name = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
        self.llm = ChatOpenAI(api_key = self.api_key, model = self.model_name)

        # 프롬프트 템플릿 (대화 이력 자리를 포함)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. You provide clear, accurate, and helpful responses. You can communicate in Korean or English based on the user's preference. Be conversational and friendly."),
            MessagesPlaceholder(variable_name="history"),  # 이전 대화 이력 삽입 위치
            ("human", "{input}")  # 사용자 입력값
        ])

        self.chain = self.prompt | self.llm  # 프롬프트와 모델 연결해서 체인 생성

        self.session_stores: Dict[str, InMemoryChatMessageHistory] = {}  # 세션별 메모리 저장

        # 대화 이력을 포함한 실행 객체
        self.runnable_with_history = RunnableWithMessageHistory(
            self.chain,  # 실행할 체인
            self.get_session_history,  # 세션 이력 조회 함수
            input_messeages_key = "input",    # 입력 메시지 키 이름
            history_messages_key = "history"  # 이력 메시지 키 이름
        )

        logger.info(f"Langchain 서비스 초기화 완료 - 모델: {self.model_name}")

    # 세션별 대화 이력을 조회하거나 새로 생성하는 함수
    def get_session_history(self, session_id:str) -> BaseChatMessageHistory:
        if session_id not in self.session_stores:
            self.session_stores[session_id] = InMemoryChatMessageHistory()  # 새로운 세션 이력 공간 생성
            logger.info(f"세션 대화 이력 새로 생성 : {session_id}")

        return self.session_stores[session_id]  # 해당 세션 대화 이력 반환

    # 사용자 메시지를 받아 AI 응답을 생성하는 비동기 함수
    async def get_chat_response(self, message: str, session_id: str = "default") -> str:
        try:
            logger.info(f"세션 {session_id}의 OpenAI 요청 메시지 : {message[:50]}...")

            # RunnableWithMessageHistory를 사용하여 응답 생성
            response = await self.runnable_with_history.ainvoke(
                {"input": message},  # 사용자 입력 전달
                config = {"configurable": {"session_id": session_id}}  # 세션 ID 전달
            )

            bot_response = response.content  # 응답 본문 추출
            logger.info(f"세션 {session_id}의 응답 수신 : {bot_response[:50]}...")

            return bot_response
        except Exception as e:
            logger.error(f"채팅 응답 생성 중 오류 발생 {str(e)}")
            raise Exception(f"AI 응답 실패: {str(e)}")  # 예외 다시 발생

    # 특정 세션의 대화 이력을 삭제하는 함수
    def clear_session_memory(self, session_id: str) -> bool:
        if session_id in self.session_stores:
            del self.session_stores[session_id]  # 해당 세션의 이력 삭제
            logger.info(f"세션 대화 이력 삭제 완료 : {session_id}")
            return True
        return False

    # 화면 표시용 대화 이력으로 변환해서 반환하는 함수
    def get_chat_history_for_display(self, session_id: str) -> List[Dict]:
        # 해당 세션 이력이 없으면 빈 리스트 반환
        if session_id not in self.session_stores:
            return []

        chat_history = self.session_stores[session_id]  # 세션 이력 조회
        messages = chat_history.messages  # 저장된 메시지 목록

        history = []
        for msg in messages:
            if msg.type == "human":
                history.append({"type": "user", "content": msg.content})
            elif msg.type == "ai":
                history.append({"type": "assistant", "content": msg.content})

        return history

    # 현재 활성화된 세션 목록을 반환하는 함수
    def get_active_sessions(self) -> List[str]:
        return list(self.session_stores.keys())  # 세션 ID 리스트 반환

    # 외부에서 받은 이력으로 세션 대화 내용을 덮어쓰는 함수
    def set_history(self, session_id: str, items: List[dict]) -> int:
        self.session_stores[session_id] = InMemoryChatMessageHistory()  # 기존 이력 초기화
        loaded = 0  # 적재된 메시지 수
        
        for item in items:
            try:
                msg_type = (item.get("type") or "").lower()  # 메시지 타입 소문자 처리
                content = item.get("content") or ""          # 메시지 내용 조회
                if not content:   # 내용이 없으면 건너뜀
                    continue
                if msg_type in ("human", "user"):
                    self.session_stores[session_id].add_user_message(content)  # 사용자 메시지 추가
                    loaded += 1  # 메시지 적재 수 증가
                elif msg_type in ("ai", "assistant"):
                    self.session_stores[session_id].add_ai_message(content)    # AI 메시지 추가
                    loaded += 1  # 메시지 적재 수 증가
            except Exception as e:
                logger.warning(f" 세션 {session_id}의 잘못된 이력 항목 건너뜀: {e}")
            
        logger.info(f"세션 {session_id}에 {loaded}개의 이력 메시지 적재 완료!")
        return loaded


# 전역 서비스 인스턴스 (앱 실행 시 1번만 생성)
chat_service = LangChainChatService()