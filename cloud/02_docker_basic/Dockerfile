# Python 베이스 이미지 사용
FROM python:3.12-slim

# 작업 디렉토리
WORKDIR /app

# 코드 복사
COPY . /app

# requirements 환경 설치
RUN pip install --no-cache-dir -r requirements.txt

# 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]