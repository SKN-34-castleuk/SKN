from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 프롬프트 템플릿, 대화 이력 Placeholder
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableWithMessageHistory  # 대화 이력 결합용 Runnable
from langchain_core.chat_history import BaseChatMessageHistory  # 채팅 이력 기본 클래스
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage  # Lanchain 메시지 타입

from dotenv import load_dotenv
import os

from .models import ChatMessage  # 채팅 메시지 DB 모델

load_dotenv()

# 데이터베이스 기반 채팅메시지 히스토리 객체
class DatabaseChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id):
        self.session_id = session_id

    # 데이터베이스의 해당 세션의 대화내역을 로드
    @property  # 메서드를 필드처럼 사용 (접근시마다 메서드 호출)
    def messages(self):
        # 해당 세션의 대화 내역 조회
        chat_messages: list[ChatMessage] = ChatMessage.objects.filter(session_id = self.session_id)

        messages = []
        for chat_message in chat_messages:
            if chat_message.message_type == 'human':
                messages.append(HumanMessage(content=chat_message.content))  # 사용자 메시지 형태로 변환
            else:
                messages.append(AIMessage(content=chat_message.content))  # AI 메시지로 변환
        return messages

    # Langchain 메시지를 데이터베이스 저장하는 함수
    def add_message(self, message: BaseMessage):
        # langchain message객체를 model 객체로 변환후 저장
        if isinstance(message, HumanMessage):  # 메시지 타입이 HumanMessage이면
            message_type = 'human'
        else:  # # 메시지 타입이 AIMessage이면
            message_type = 'ai'

        ChatMessage.objects.create(
            session_id = self.session_id,
            message_type = message_type,
            content = message.content
        )  # DB 데이터 생성

    # 해당 세션의 대화내역 삭제
    def clear(self):
        ChatMessage.objects.filter(session_id=self.session_id).delete()

prompt = ChatPromptTemplate.from_messages([
    ('system', '넌 IT분야의 직업상담사 챗봇이야.'),
    MessagesPlaceholder(variable_name = 'history'),  # 이전 대화 이력을 추가
    ('human', '{query}'),  # 현재 사용지 질문
])

# session_id를 받아 DB 기반 대화 이력 객체 반환하는 함수
def get_by_session_id(session_id):
    return DatabaseChatMessageHistory(session_id)

llm = init_chat_model('gpt-5.6-luna')
chain = prompt | llm
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history = get_by_session_id,  # 세션별 이력 조회 함수 연결
    input_messages_key = 'query',  # 사용자 입력
    history_messages_key = 'history',  # 대화 이력 키
)

# 세션별 대화 이력을 포함해서 체인을 실행하는 함수
def invoke_chain_with_history(session_id, query):
    return chain_with_history.invoke({
        'query': query  # 현재 사용자 질문
    }, config = {
        'configurable': {
            'session_id': session_id  # 어떤 세션의 이력을 사용할지 지정
        }
    })