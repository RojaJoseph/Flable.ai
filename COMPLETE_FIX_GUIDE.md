# Complete Fix Guide - Step by Step

## Current Issues & Solutions

### Issue: 401 Unauthorized After Login

**Root Cause**: Old invalid tokens in browser localStorage from previous sessions

**Solution**: Clear browser storage and login fresh

## Step-by-Step Fix

### Step 1: Clear Browser Storage

**Option A: Use the Token Manager Page** (Recommended)
1. Open this file in your browser:
   ```
   F:\flable.ai\frontend\clear-tokens.html
   ```
2. Click "Clear All Tokens"
3. It will auto-redirect you to login

**Option B: Manual Browser Clear**
1. Open your application at `http://localhost:3000`
2. Press `F12` to open Developer Tools
3. Go to "Application" tab (Chrome) or "Storage" tab (Firefox)
4. Under "Local Storage" → `http://localhost:3000`
5. Delete `access_token` and `refresh_token`
6. Refresh the page

**Option C: Console Command**
1. Open Developer Tools (`F12`)
2. Go to Console tab
3. Run:
   ```javascript
   localStorage.clear()
   ```
4. Refresh the page

### Step 2: Restart Backend (If Not Running)

```bash
cd F:\flable.ai\backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

You should see:
```
✓ Database tables created
⚠ Redis not available - running without cache
Application startup complete.
```

### Step 3: Login Fresh

1. Go to `http://localhost:3000/login`
2. Enter credentials:
   - Email: `demo@flable.ai`
   - Password: `demo123`
3. Click "Sign In"

### Step 4: Verify Success

After login, you should see:
- ✅ Redirected to dashboard
- ✅ Stats showing (Total Campaigns, Total Spend, etc.)
- ✅ No errors in browser console
- ✅ No 401 errors in backend logs

## What Was Fixed

### Backend Changes:
1. ✅ `auth_utils.py` - Added pbkdf2_sha256 hash support
2. ✅ `main.py` - Disabled trailing slash redirects
3. ✅ `auth.py` - Fixed refresh token endpoint to accept request body
4. ✅ `dashboard.py` - Added routes for both slash variants
5. ✅ `campaigns.py` - Added routes for both slash variants

### Frontend Changes:
1. ✅ `api.ts` - Improved token refresh logic
2. ✅ `api.ts` - Better error handling for expired tokens
3. ✅ `api.ts` - Skip adding tokens to login/register requests
4. ✅ Added token manager utility page

## Testing the Full Flow

### 1. Backend Health Check
```bash
curl http://127.0.0.1:8000/health
```
Should return:
```json
{"status":"healthy","version":"1.0.0","environment":"development"}
```

### 2. Login Test
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@flable.ai","password":"demo123"}'
```
Should return tokens.

### 3. Run Test Script
```bash
cd F:\flable.ai\backend
python test_api.py
```

### 4. Frontend Test
1. Clear tokens (use clear-tokens.html)
2. Login at localhost:3000/login
3. Dashboard should load successfully

## Expected Backend Logs (Success)

```
INFO: 127.0.0.1:XXXXX - "POST /api/v1/auth/login HTTP/1.1" 200 OK
INFO: 127.0.0.1:XXXXX - "GET /api/v1/dashboard HTTP/1.1" 200 OK
INFO: 127.0.0.1:XXXXX - "GET /api/v1/campaigns?limit=10 HTTP/1.1" 200 OK
```

## Expected Frontend (No Errors)

Browser Console should show:
- ✅ No CORS errors
- ✅ No 401 errors
- ✅ No 422 errors
- ✅ All API calls returning 200

## Troubleshooting

### Problem: Still getting 401 after login

**Solution:**
1. Make sure you cleared localStorage
2. Try incognito/private mode
3. Check browser console for actual error
4. Check backend logs for detailed error

### Problem: Refresh token 422 error

**Solution:**
This should be fixed. If still happening:
1. Clear browser storage completely
2. Restart backend
3. Login fresh

### Problem: CORS errors

**Solution:**
1. Check backend is running on 127.0.0.1:8000
2. Check frontend is running on localhost:3000
3. Verify .env has correct ALLOWED_ORIGINS

### Problem: Database errors

**Solution:**
```bash
cd F:\flable.ai\backend
python reset_demo_user.py
```

## Quick Commands Reference

### Backend
```bash
# Start backend
cd F:\flable.ai\backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Test API
python test_api.py

# Reset user
python reset_demo_user.py
```

### Frontend
```bash
# Start frontend
cd F:\flable.ai\frontend
npm run dev
# or
yarn dev
```

### Clear Tokens
Just open: `F:\flable.ai\frontend\clear-tokens.html`

## Files to Reference

- `FIXES_APPLIED.md` - Detailed technical changes
- `QUICK_FIX.md` - Quick reference
- `clear-tokens.html` - Token management utility
- `test_api.py` - API testing script
- `reset_demo_user.py` - User reset utility

## Success Criteria

✅ Login returns 200 OK
✅ Dashboard loads without 401 errors  
✅ Campaigns list loads without errors
✅ No CORS errors in console
✅ Token refresh works (if needed)
✅ All stats display correctly

Your app should now work perfectly! 🎉

## Need More Help?

If issues persist after following all steps:
1. Clear ALL browser data (cookies, cache, localStorage)
2. Restart both backend and frontend
3. Use incognito mode for testing
4. Check the actual error messages in console/logs
