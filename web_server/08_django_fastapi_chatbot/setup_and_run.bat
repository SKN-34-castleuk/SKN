@echo off
echo ===== ChatBot Application Setup and Run Script =====
echo.

echo 1. Installing Python dependencies...
echo.

echo Installing Django webapp dependencies...
cd django_webapp
pip install -r requirements.txt
echo.

echo Installing FastAPI LangChain dependencies...
cd ../fastapi_langchain
pip install -r requirements.txt
cd ..
echo.

echo 2. Setting up Django database...
cd django_webapp
python manage.py makemigrations chat
python manage.py migrate
echo.

echo 3. Starting applications...
echo.
cd ..

echo Starting FastAPI service in background...
start cmd /k "cd fastapi_langchain && uvicorn main:app --reload --port 8001"
timeout /t 3

echo Starting Django webapp...
cd django_webapp
start cmd /k "python manage.py runserver 8000"
cd ..

echo.
echo ===== Setup Complete! =====
echo.
echo Applications are running:
echo - Django Web App: http://localhost:8000
echo - FastAPI Service: http://localhost:8001
echo - FastAPI Docs: http://localhost:8001/docs
echo.
echo Make sure to set your OPENAI_API_KEY in fastapi_langchain/.env file!
echo.
pause 