@echo off
echo ================================================
echo   Flable.ai - Manual Backend Test
echo ================================================
echo.

echo [1/4] Testing Backend Health...
curl -s http://127.0.0.1:8000/health
echo.
echo.

echo [2/4] Testing Login...
echo Email: demo@flable.ai
echo Password: demo123
echo.
curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"demo@flable.ai\",\"password\":\"demo123\"}" > temp_tokens.json

type temp_tokens.json
echo.
echo.

echo [3/4] Extracting Token...
for /f "tokens=2 delims=:," %%a in ('findstr "access_token" temp_tokens.json') do set TOKEN=%%a
set TOKEN=%TOKEN:"=%
set TOKEN=%TOKEN: =%
echo Token (first 50 chars): %TOKEN:~0,50%
echo.

echo [4/4] Testing Dashboard with Token...
curl -s -H "Authorization: Bearer %TOKEN%" http://127.0.0.1:8000/api/v1/dashboard
echo.
echo.

del temp_tokens.json
echo.
echo ================================================
echo   Test Complete!
echo ================================================
echo.
echo If you see data above, your backend works perfectly!
echo The issue is frontend caching - restart Next.js dev server.
echo.
pause
