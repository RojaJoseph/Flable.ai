@echo off
cls
echo ================================================================
echo   FLABLE.AI - Password Hash Fix
echo ================================================================
echo.
echo This will fix the password hash issue and let you login!
echo.
pause

cd /d "%~dp0"
cd backend

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running user seed script...
echo This will update the password hash to the correct format.
echo.
python seed_user.py

echo.
echo ================================================================
echo   DONE! Try logging in now:
echo ================================================================
echo.
echo   Email: demo@flable.ai
echo   Password: demo123
echo.
echo   Go to: http://localhost:3000/login
echo.
pause
