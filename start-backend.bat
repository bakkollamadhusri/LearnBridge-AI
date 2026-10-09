@echo off
echo ========================================================
echo  Starting LearnBridge AI - FastAPI Backend
echo  API Host: http://127.0.0.1:8000
echo  Swagger Docs: http://127.0.0.1:8000/docs
echo ========================================================
cd /d "%~dp0backend"
py -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
