# 🚀 Local FastAPI Deployment Guide

## Prerequisites
- Python 3.11+ installed
- PostgreSQL running locally
- Redis running locally (optional but recommended)

---

## Step 1: Database Setup

### Install PostgreSQL (if not installed)
Download from: https://www.postgresql.org/download/windows/

### Create Database
```sql
-- Open pgAdmin or psql
CREATE DATABASE flable_db;
CREATE USER flable WITH PASSWORD 'flable123';
GRANT ALL PRIVILEGES ON DATABASE flable_db TO flable;
```

---

## Step 2: Redis Setup (Optional)

### Install Redis on Windows
Download from: https://github.com/microsoftarchive/redis/releases
Or use: `choco install redis` (if you have Chocolatey)

### Start Redis
```powershell
redis-server
```

---

## Step 3: Backend Setup

### Navigate to Backend
```powershell
cd f:\flable.ai\backend
```

### Create Virtual Environment
```powershell
python -m venv venv
```

### Activate Virtual Environment
```powershell
.\venv\Scripts\activate
```

### Install Dependencies
```powershell
pip install -r requirements.txt
```

### Configure Environment
```powershell
# Copy and edit .env file
cp ..\.env.example .env

# Edit .env and update:
# DATABASE_URL=postgresql://flable:flable123@localhost:5432/flable_db
# REDIS_URL=redis://localhost:6379/0
# SECRET_KEY=your-secret-key-change-this
```

### Initialize Database
```powershell
# Run migrations
alembic upgrade head

# Or create tables directly
python -c "from database.connection import init_db; init_db()"
```

---

## Step 4: Start FastAPI Server

### Development Mode (with auto-reload)
```powershell
# Make sure you're in backend/ with venv activated
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode (with Gunicorn)
```powershell
gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 4
```

---

## Step 5: Verify Deployment

### Check Health
Open browser: http://localhost:8000/health

### Check API Docs
Open browser: http://localhost:8000/docs

### Test API
```powershell
# Register a user
curl -X POST http://localhost:8000/api/v1/auth/register `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "full_name": "Test User"
  }'
```

---

## Step 6: Start Background Workers (Optional)

### In a new PowerShell window:
```powershell
cd f:\flable.ai\backend
.\venv\Scripts\activate
celery -A celery_app worker --loglevel=info --pool=solo
```

Note: Use `--pool=solo` on Windows

---

## 🎯 Quick Commands

### Start Backend Only
```powershell
cd f:\flable.ai\backend
.\venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Stop Server
Press `Ctrl + C` in the terminal

### View Logs
Logs are in: `f:\flable.ai\logs\`

---

## 🔧 Troubleshooting

### Port Already in Use
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <process_id> /F
```

### Database Connection Error
- Verify PostgreSQL is running
- Check credentials in `.env`
- Ensure database exists

### Module Import Errors
```powershell
# Fix Python path
cd f:\flable.ai\backend
$env:PYTHONPATH = "f:\flable.ai\backend"
```

---

## 📊 Access Points

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Metrics**: http://localhost:8000/metrics

---

## 🛑 Stop Everything

```powershell
# Stop FastAPI: Ctrl + C in terminal
# Stop Celery: Ctrl + C in celery terminal
# Stop PostgreSQL: Services app or pgAdmin
# Stop Redis: Ctrl + C in redis terminal
```
