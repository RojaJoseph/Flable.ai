@echo off
cls
echo ================================================================
echo   FIX BCRYPT ISSUE - Switch to Argon2
echo ================================================================
echo.
echo This will:
echo   1. Remove old bcrypt/passlib
echo   2. Install Argon2 (pure Python, always works!)
echo   3. Delete old database (bcrypt hashes won't work with Argon2)
echo   4. Test everything
echo   5. Deploy to Render
echo.
pause

cd /d F:\flable.ai\backend

echo.
echo [1/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [2/6] Uninstalling old password libraries...
pip uninstall bcrypt passlib -y

echo.
echo [3/6] Installing Argon2...
pip install argon2-cffi==23.1.0 --break-system-packages

echo.
echo [4/6] Deleting old database (old password hashes won't work)...
if exist flable.db (
    del flable.db
    echo ✅ Old database deleted
) else (
    echo ℹ No old database found
)

echo.
echo [5/6] Running tests...
python test_setup.py
if errorlevel 1 (
    echo.
    echo ❌ Tests failed! Check errors above.
    pause
    exit /b 1
)

cd ..

echo.
echo [6/6] Deploying to Render...
git add .
git commit -m "Switch to Argon2 password hashing - fixes all bcrypt issues"
git push

echo.
echo ================================================================
echo   SUCCESS! 🎉
echo ================================================================
echo.
echo Render will deploy in 2-3 minutes.
echo.
echo Next steps:
echo   1. Wait for Render: https://dashboard.render.com
echo   2. Test health: https://flable-ai-xwuo.onrender.com/health
echo   3. Register: http://localhost:3000/register
echo   4. Login: http://localhost:3000/login
echo.
echo Note: You need to register again (old passwords deleted)
echo.
pause
