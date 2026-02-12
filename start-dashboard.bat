@echo off
REM Complete Dashboard Startup Script
REM This starts BOTH backend and frontend

echo ========================================
echo   Flable.ai - Complete Dashboard
echo ========================================
echo.
echo Starting Backend and Frontend...
echo.

REM Start Backend in new window
echo [1/2] Starting FastAPI Backend...
start "Flable.ai Backend" cmd /k "cd /d %~dp0backend && .\venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start Frontend in new window  
echo [2/2] Starting Next.js Frontend...
start "Flable.ai Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo ✅ Both services starting...
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo.
echo Wait 10-15 seconds, then open browser to:
echo   http://localhost:3000
echo.
echo To stop: Close both terminal windows
echo ========================================
pause
