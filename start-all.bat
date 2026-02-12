@echo off
echo ====================================================
echo FLABLE.AI - STARTING ALL SERVICES
echo ====================================================
echo.

REM Check if setup was run
if not exist "backend\venv" (
    echo ERROR: Setup not complete!
    echo Please run: setup-local.bat
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo ERROR: Frontend not set up!
    echo Please run: setup-local.bat
    pause
    exit /b 1
)

echo Starting services...
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.

REM Start backend in new window
start "Flable.ai - Backend (FastAPI)" cmd /k "cd /d %~dp0 && run-backend.bat"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Start frontend in new window
start "Flable.ai - Frontend (Next.js)" cmd /k "cd /d %~dp0 && run-frontend.bat"

echo.
echo ====================================================
echo ✓ SERVICES STARTING!
echo ====================================================
echo.
echo Two windows opened:
echo   - Backend (FastAPI)  → http://localhost:8000
echo   - Frontend (Next.js) → http://localhost:3000
echo.
echo Visit: http://localhost:3000
echo.
echo To stop: Close the terminal windows
echo.
pause
