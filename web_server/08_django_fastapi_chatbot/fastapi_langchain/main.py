from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # CORS 미들웨어
from routers import chat_router  # 채팅 라우터 모듈
import uvicorn  # ASGI 서버 실행 도구

# FastAPI 앱 생성
app = FastAPI(
    title="ChatBot LangChain API",
    description="FastAPI + LangChain + OpenAI 챗봇 서비스",
    version="1.0.0"
)

# CORS 설정 — Django 앱에서의 요청 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],  # Django 앱 주소 허용
    allow_credentials=True,  # 쿠키/인증 정보 포함 허용
    allow_methods=["*"],  # 모든 http 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 라우터 등록 — /chat/ 이하 모든 URL을 chat_router에서 처리
app.include_router(chat_router.router, prefix="/chat", tags=["chat"])


@app.get("/")
async def root():
    return {"message": "ChatBot LangChain API is running!", "docs": "/docs"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 현재 파일을 직접 실행하면 Uvicorn 서버를 실행하는 코드 (8001 포트에서 서버 실행)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)