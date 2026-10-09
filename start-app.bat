@echo off
echo ========================================================
echo  Launching LearnBridge AI Platform (Full-Stack)
echo  Tagline: Learn Anything. Connect with Everyone. Grow Together.
echo ========================================================
start "LearnBridge AI - FastAPI Backend (Port 8000)" cmd /k "cd /d %~dp0backend && py -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
timeout /t 2 /nobreak >nul
start "LearnBridge AI - Next.js Frontend (Port 3000)" cmd /k "cd /d %~dp0frontend && npm run dev"
echo.
echo [OK] Both servers launched!
echo Open your browser at: http://localhost:3000
echo Backend docs available at: http://127.0.0.1:8000/docs
echo.
pause
