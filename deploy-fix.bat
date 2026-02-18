@echo off
cls
echo ================================================================
echo   FLABLE.AI - FINAL COMPLETE FIX
echo ================================================================
echo.
echo This will fix ALL issues and deploy to Render!
echo.
pause

cd /d F:\flable.ai

echo.
echo [1/4] Testing local setup...
cd backend
call venv\Scripts\activate.bat
python test_setup.py
if errorlevel 1 (
    echo.
    echo Tests failed! Fix errors before continuing.
    pause
    exit /b 1
)
cd ..

echo.
echo [2/4] Committing changes to Git...
git add .
git commit -m "Complete fix - bcrypt, CORS, database"

echo.
echo [3/4] Pushing to GitHub...
git push

echo.
echo [4/4] Done! Render will auto-deploy in 2-3 minutes.
echo.
echo ================================================================
echo   NEXT STEPS:
echo ================================================================
echo.
echo 1. Wait 2-3 minutes for Render to deploy
echo 2. Check: https://dashboard.render.com
echo 3. Test: https://flable-ai-xwuo.onrender.com/health
echo 4. Register: http://localhost:3000/register
echo.
echo ================================================================
echo.
pause
