# 🔧 AUTH FIX - 401 Error Solution

## The Problem
Login works ✅ but Dashboard fails with 401 ❌

This means JWT tokens are being created but not validated correctly.

---

## ⚡ QUICK FIX

### Step 1: Restart Backend with Logging
```bash
# Stop current backend (Ctrl+C)

# Restart with debug logs
cd F:\flable.ai\backend
venv\Scripts\activate
python -m uvicorn main:app --reload --log-level debug
```

### Step 2: Test with Debug Tool
Go to: **http://localhost:3000/debug**

Click: **"Run Full Test"**

This will show you EXACTLY where it fails!

---

## 🧪 Manual Testing

### Test 1: Login
```bash
# In browser console or Postman
POST http://localhost:8000/api/v1/auth/login
Body:
{
  "email": "admin@flable.ai",
  "password": "admin123"
}

# Should return:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Test 2: Debug Token
```bash
GET http://localhost:8000/api/v1/auth/debug/token
Header: Authorization: Bearer <your_token>

# Should return token details
```

### Test 3: Auth Me
```bash
GET http://localhost:8000/api/v1/auth/me
Header: Authorization: Bearer <your_token>

# Should return user info
```

### Test 4: Dashboard
```bash
GET http://localhost:8000/api/v1/dashboard
Header: Authorization: Bearer <your_token>

# Should return dashboard data
```

---

## 🔍 Common Issues & Fixes

### Issue 1: Token Format
**Symptom:** "Could not validate credentials"

**Fix:** Check token is sent as:
```
Authorization: Bearer eyJhbGci...
```

NOT:
```
Authorization: eyJhbGci...  (missing Bearer)
Authorization: bearer eyJhbGci...  (lowercase)
```

### Issue 2: Wrong API URL
**Symptom:** Network error or 404

**Fix:** Check `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Issue 3: Token Expired
**Symptom:** Works initially, then fails

**Fix:** Tokens expire after 30 minutes. Login again or use refresh token.

### Issue 4: User Not Found
**Symptom:** "User not found"

**Fix:** Create user first:
```bash
cd backend
python seed_user.py
```

### Issue 5: CORS Error
**Symptom:** Preflight request failed

**Fix:** Check `backend/.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 📊 Check Backend Logs

When you run the test, check backend terminal for:

```
✓ GOOD:
INFO: 127.0.0.1:XXXXX - "POST /api/v1/auth/login HTTP/1.1" 200 OK
DEBUG: Created access token for user_id: 1
DEBUG: Token decoded successfully. Payload: {'sub': 1, ...}
DEBUG: User authenticated successfully: admin@flable.ai

✗ BAD:
ERROR: JWT decode error: ...
ERROR: No 'sub' field in token payload
ERROR: User not found with ID: 1
```

---

## 🛠️ Files I Updated

1. **backend/utils/auth_utils.py** - Added detailed logging
2. **backend/api/routes/auth.py** - Added debug endpoint
3. **frontend/src/app/debug/page.tsx** - Debug tool page

---

## 🎯 Step-by-Step Debug Process

### 1. Check Backend is Running
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### 2. Check User Exists
```bash
cd backend
python -c "from database.connection import get_db; from database.models import User; db = next(get_db()); print(db.query(User).all())"
```

### 3. Test Login Directly
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@flable.ai","password":"admin123"}'
```

### 4. Use Debug Endpoint
```bash
curl -X GET http://localhost:8000/api/v1/auth/debug/token \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 5. Check Dashboard
```bash
curl -X GET http://localhost:8000/api/v1/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🚀 Quick Reset

If all else fails:

```bash
# 1. Stop everything
taskkill /F /IM python.exe
taskkill /F /IM node.exe

# 2. Delete database
del F:\flable.ai\backend\flable.db

# 3. Restart
cd F:\flable.ai
START.bat

# 4. Create user
cd backend
python seed_user.py

# 5. Test at http://localhost:3000/debug
```

---

## 📝 What the Debug Tool Shows

The debug tool tests:
1. ✅ Backend health
2. ✅ Token creation (login)
3. ✅ Token validation (/auth/me)
4. ✅ Token debug endpoint
5. ✅ Dashboard with token

It will show you EXACTLY which step fails!

---

## 💡 Most Likely Issue

Based on your screenshot, the issue is:
- Login works ✅ (tokens created)
- Dashboard fails ❌ (tokens not validated)

This usually means:
1. **Token format issue** - Check logs
2. **User not in database** - Run seed_user.py
3. **Token decode error** - Check SECRET_KEY matches

---

## 🎯 Try This NOW:

1. Go to: **http://localhost:3000/debug**
2. Click: **"Run Full Test"**
3. Check which step fails
4. Look at backend logs
5. Report what you see!

The debug tool will tell us EXACTLY what's wrong! 🔍

---

## 📞 Next Steps

After running the debug tool, you'll see:
- ✅ Green checks = Working
- ❌ Red X = Failed
- Error details in red box

Share the results and I can give you the exact fix!
