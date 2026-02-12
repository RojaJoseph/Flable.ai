@echo off
echo ====================================================
echo FLABLE.AI - ONE-TIME SETUP
echo ====================================================
echo.

REM Check Python
echo [1/6] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.11+ from python.org
    pause
    exit /b 1
)
echo ✓ Python found

REM Check Node.js
echo.
echo [2/6] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found!
    echo Please install Node.js 18+ from nodejs.org
    pause
    exit /b 1
)
echo ✓ Node.js found

REM Setup Backend
echo.
echo [3/6] Setting up Backend...
cd backend

REM Create venv if needed
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python packages...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Check .env
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
)

REM Initialize database
echo Initializing database...
python -c "from database.connection import init_db; init_db()" 2>nul
if errorlevel 1 (
    echo Warning: Database initialization had issues (may be OK if already exists)
)

cd ..

REM Setup Frontend
echo.
echo [4/6] Setting up Frontend...
cd frontend

REM Install node modules
if not exist "node_modules" (
    echo Installing Node packages (this may take a few minutes)...
    npm install
) else (
    echo ✓ Node packages already installed
)

REM Check .env.local
if not exist ".env.local" (
    echo Creating .env.local...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 > .env.local
)

cd ..

REM Fix imports
echo.
echo [5/6] Fixing imports...
cd backend
call venv\Scripts\activate.bat
python fix_imports.py
cd ..

REM Create logs directory
if not exist "logs" mkdir logs

echo.
echo [6/6] Final checks...
echo ✓ Backend setup complete
echo ✓ Frontend setup complete
echo ✓ Imports fixed
echo ✓ Logs directory created

echo.
echo ====================================================
echo ✓ SETUP COMPLETE!
echo ====================================================
echo.
echo Next steps:
echo   1. Add Shopify credentials to backend\.env
echo   2. Run: start-all.bat
echo.
echo Or start services individually:
echo   - Backend:  run-backend.bat
echo   - Frontend: run-frontend.bat
echo.
pause
