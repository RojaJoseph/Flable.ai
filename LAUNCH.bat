@echo off
cls
color 0A
echo.
echo  ███████╗██╗      █████╗ ██████╗ ██╗     ███████╗     █████╗ ██╗
echo  ██╔════╝██║     ██╔══██╗██╔══██╗██║     ██╔════╝    ██╔══██╗██║
echo  █████╗  ██║     ███████║██████╔╝██║     █████╗      ███████║██║
echo  ██╔══╝  ██║     ██╔══██║██╔══██╗██║     ██╔══╝      ██╔══██║██║
echo  ██║     ███████╗██║  ██║██████╔╝███████╗███████╗    ██║  ██║██║
echo  ╚═╝     ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝
echo.
echo  AI-Powered Marketing Platform - Complete Setup Wizard
echo  ═══════════════════════════════════════════════════════════════
echo.
timeout /t 2 /nobreak >nul

echo [STEP 1/4] Checking project health...
echo.
call check-project.bat
if errorlevel 1 (
    echo.
    echo [ERROR] Project check failed!
    echo Please fix the errors and run this script again.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo [STEP 2/4] Configuration Check
echo ═══════════════════════════════════════════════════════════════
echo.

if exist "backend\.env" (
    echo ✓ Backend configuration found
    echo.
    findstr /C:"SHOPIFY_CLIENT_ID=your_client_id_here" backend\.env >nul
    if errorlevel 1 (
        echo ✓ Shopify credentials configured
    ) else (
        echo.
        echo ⚠ WARNING: Shopify credentials not configured!
        echo.
        echo To use Shopify integration:
        echo   1. Edit: backend\.env
        echo   2. Add your SHOPIFY_CLIENT_ID
        echo   3. Add your SHOPIFY_CLIENT_SECRET
        echo.
        echo You can skip this for now and configure later.
        echo.
        choice /C YN /M "Continue without Shopify"
        if errorlevel 2 (
            echo.
            echo Exiting. Please configure Shopify and try again.
            pause
            exit /b 0
        )
    )
) else (
    echo ⚠ Backend .env not found - will use defaults
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo [STEP 3/4] Database Check
echo ═══════════════════════════════════════════════════════════════
echo.

if not exist "backend\flable.db" (
    echo Initializing SQLite database...
    cd backend
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
        python -c "from database.connection import init_db; init_db()" 2>nul
        if errorlevel 0 (
            echo ✓ Database initialized successfully
        ) else (
            echo ⚠ Database will be created on first run
        )
    ) else (
        echo ⚠ Database will be created on first run
    )
    cd ..
) else (
    echo ✓ Database already exists
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo [STEP 4/4] Ready to Launch!
echo ═══════════════════════════════════════════════════════════════
echo.
echo Your Flable.ai platform is ready!
echo.
echo Starting services will open 2 windows:
echo   • Backend (FastAPI)  → http://localhost:8000
echo   • Frontend (Next.js) → http://localhost:3000
echo.
echo Access points:
echo   → Main App:  http://localhost:3000
echo   → API Docs:  http://localhost:8000/docs
echo   → Health:    http://localhost:8000/health
echo.
pause

echo.
echo Starting Flable.ai...
timeout /t 2 /nobreak >nul

call start-local.bat

echo.
echo ═══════════════════════════════════════════════════════════════
echo  ✓ LAUNCH COMPLETE!
echo ═══════════════════════════════════════════════════════════════
echo.
echo Two windows have opened with your services.
echo.
echo 🌐 Visit: http://localhost:3000
echo.
echo Next steps:
echo   1. Register a new account
echo   2. Explore the dashboard
echo   3. Connect Shopify (if configured)
echo   4. Create your first campaign!
echo.
echo 📖 Need help? Check PROJECT_COMPLETE.md
echo.
pause
