# Quick Fix for Login Issues

## Problem
Your app had two issues:
1. **Password Hash Mismatch**: User password was created with `pbkdf2_sha256` but auth system only accepted `bcrypt`
2. **CORS Error**: Backend crashed before sending CORS headers due to password error

## What Was Fixed
✅ Updated `backend/utils/auth_utils.py` to accept both hash types
✅ CORS configuration was already correct

## Steps to Fix

### 1. Restart Backend
```bash
# Stop the current backend (Ctrl+C in the terminal)
# Then restart it
cd F:\flable.ai\backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test Login
- Email: `demo@flable.ai`
- Password: `demo123`

### 3. If Still Having Issues

If login still fails, run this script to recreate the user with proper bcrypt hash:

```bash
cd F:\flable.ai\backend
python reset_demo_user.py
```

## Verification

1. Backend should start without errors
2. You should see in logs: `✓ Database tables created`
3. Login should work at `http://localhost:3000`
4. No CORS errors in browser console

## Future Prevention

For new users, ensure `bcrypt` is installed:
```bash
pip install bcrypt
```

This ensures passwords are hashed with bcrypt by default.
