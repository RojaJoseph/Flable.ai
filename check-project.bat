@echo off
cls
echo ============================================================
echo   FLABLE.AI - COMPLETE PROJECT CHECK
echo ============================================================
echo.

cd /d F:\flable.ai

echo [1/6] Checking Project Structure...
echo.

REM Check backend structure
if not exist "backend\main.py" (
    echo [ERROR] backend\main.py not found!
    goto :error
)
if not exist "backend\api\routes\" (
    echo [ERROR] backend\api\routes\ not found!
    goto :error
)
if not exist "backend\database\models.py" (
    echo [ERROR] backend\database\models.py not found!
    goto :error
)
echo   ✓ Backend structure OK

REM Check frontend structure  
if not exist "frontend\package.json" (
    echo [ERROR] frontend\package.json not found!
    goto :error
)
if not exist "frontend\src\app\" (
    echo [ERROR] frontend\src\app\ not found!
    goto :error
)
echo   ✓ Frontend structure OK

echo.
echo [2/6] Checking Backend Dependencies...
echo.

cd backend

if not exist "venv\" (
    echo [WARN] Virtual environment not found!
    echo   → Run: setup-local.bat
    goto :skip_venv_check
)

call venv\Scripts\activate.bat 2>nul
if errorlevel 1 (
    echo [ERROR] Could not activate virtual environment!
    goto :error
)

python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [ERROR] FastAPI not installed!
    echo   → Run: pip install -r requirements.txt
    goto :error
)
echo   ✓ FastAPI installed

python -c "import sqlalchemy" 2>nul
if errorlevel 1 (
    echo [ERROR] SQLAlchemy not installed!
    goto :error
)
echo   ✓ SQLAlchemy installed

python -c "import pydantic" 2>nul
if errorlevel 1 (
    echo [ERROR] Pydantic not installed!
    goto :error
)
echo   ✓ Pydantic installed

:skip_venv_check
cd ..

echo.
echo [3/6] Checking Frontend Dependencies...
echo.

cd frontend

if not exist "node_modules\" (
    echo [WARN] Node modules not found!
    echo   → Run: npm install
    goto :skip_npm_check
)
echo   ✓ Node modules installed

:skip_npm_check
cd ..

echo.
echo [4/6] Checking Configuration Files...
echo.

if not exist "backend\.env" (
    echo [WARN] backend\.env not found!
    echo   → Will use default configuration
) else (
    echo   ✓ Backend .env exists
)

if not exist "frontend\.env.local" (
    echo [WARN] frontend\.env.local not found!
    echo   → Will use default configuration
) else (
    echo   ✓ Frontend .env.local exists
)

echo.
echo [5/6] Checking Database...
echo.

if exist "backend\flable.db" (
    echo   ✓ SQLite database exists
) else (
    echo [INFO] Database not initialized
    echo   → Will be created on first run
)

echo.
echo [6/6] Checking Key Files...
echo.

REM Check important backend files
if exist "backend\api\routes\auth.py" (echo   ✓ auth.py) else (echo [ERROR] auth.py missing!)
if exist "backend\api\routes\campaigns.py" (echo   ✓ campaigns.py) else (echo [ERROR] campaigns.py missing!)
if exist "backend\api\routes\integrations.py" (echo   ✓ integrations.py) else (echo [ERROR] integrations.py missing!)
if exist "backend\database\connection.py" (echo   ✓ connection.py) else (echo [ERROR] connection.py missing!)
if exist "backend\database\models.py" (echo   ✓ models.py) else (echo [ERROR] models.py missing!)

echo.
echo ============================================================
echo   ✓ PROJECT CHECK COMPLETE!
echo ============================================================
echo.
echo Next Steps:
echo   1. Run: setup-local.bat (if not done)
echo   2. Add Shopify credentials to backend\.env
echo   3. Run: start-local.bat
echo.
pause
exit /b 0

:error
echo.
echo ============================================================
echo   ✗ PROJECT CHECK FAILED!
echo ============================================================
echo.
echo Please fix the errors above and try again.
echo.
pause
exit /b 1
