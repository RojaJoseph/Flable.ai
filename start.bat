@echo off
cls
echo.
echo ================================================================
echo   FLABLE.AI - One-Click Launcher
echo ================================================================
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

echo Starting from: %CD%
echo.

REM Check if setup has been run
if not exist "backend\venv" (
    echo First time setup detected...
    echo.
    echo [1/2] Setting up Backend...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -q -r requirements.txt
    python -c "from database.connection import init_db; init_db()" 2>nul
    cd ..
    echo   Done!
    echo.
)

if not exist "frontend\node_modules" (
    echo [2/2] Setting up Frontend...
    cd frontend
    call npm install
    cd ..
    echo   Done!
    echo.
)

echo ================================================================
echo   Starting Services...
echo ================================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

REM Start backend in background
cd backend
start /B cmd /c "venv\Scripts\activate.bat && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 2>nul"
cd ..

REM Wait for backend
timeout /t 5 /nobreak >nul

REM Start frontend in background
cd frontend
start /B cmd /c "npm run dev 2>nul"
cd ..

REM Wait for frontend
timeout /t 5 /nobreak >nul

echo.
echo ================================================================
echo   RUNNING! Open: http://localhost:3000
echo ================================================================
echo.

REM Open browser
start http://localhost:3000

REM Keep window open
echo Press any key to stop services...
pause >nul

REM Kill processes
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul

echo.
echo Services stopped.
timeout /t 2 /nobreak >nul
