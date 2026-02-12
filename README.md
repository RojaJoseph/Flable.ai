# 🚀 Flable.ai - Enterprise AI Marketing Platform

<div align="center">

![Flable.ai](https://img.shields.io/badge/Flable.ai-AI%20Marketing-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

**AI-Powered Marketing Platform for E-commerce**

Automate campaigns • Optimize ROAS • Scale with AI

[Quick Start](#-quick-start) •
[Features](#-features) •
[Documentation](#-documentation) •
[API](#-api-documentation)

</div>

---

## 📖 Overview

Flable.ai is a full-stack, enterprise-grade AI marketing platform that helps e-commerce businesses automate and optimize their marketing campaigns. Built with modern technologies and powered by machine learning, it provides:

- 🤖 **AI-Powered Optimization** - Machine learning models continuously improve campaign performance
- 📊 **Real-Time Analytics** - Track metrics and get actionable insights
- 🛍️ **E-commerce Integration** - Seamless Shopify integration with product and order sync
- 💰 **Budget Optimization** - Smart budget allocation across campaigns
- 📈 **ROAS Prediction** - Forecast returns before spending
- 🔄 **Automated Management** - Set it and forget it campaign management

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed
- 8GB RAM minimum
- Windows 10/11, macOS, or Linux

### 1. Clone or Navigate to Project
```bash
cd F:\flable.ai
```

### 2. Start Everything (Windows)
```bash
start.bat
```

### 3. Access the Platform
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. Create Account & Start!
1. Go to http://localhost:3000
2. Click "Get Started"
3. Create your account
4. Connect Shopify (optional)
5. Create campaigns!

📖 **Detailed guide**: See [QUICKSTART.md](QUICKSTART.md)

---

## ✨ Features

### Core Platform
- ✅ User authentication & management (JWT)
- ✅ Campaign creation & management
- ✅ Real-time analytics dashboard
- ✅ AI-powered optimization engine
- ✅ Budget allocation optimization
- ✅ Performance forecasting

### Integrations
- ✅ **Shopify** - Products, orders, customers sync
- 🔜 **Google Ads** - Coming soon
- 🔜 **Facebook Ads** - Coming soon
- 🔜 **Google Analytics** - Coming soon

### AI & ML Features
- ✅ ROAS prediction
- ✅ Conversion forecasting
- ✅ Budget optimization
- ✅ Anomaly detection
- ✅ Campaign recommendations
- ✅ Auto-scaling

### Technical Features
- ✅ RESTful API with FastAPI
- ✅ Real-time data processing
- ✅ Background task processing (Celery)
- ✅ Caching (Redis)
- ✅ Monitoring (Prometheus + Grafana)
- ✅ Containerized deployment (Docker)

---

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│                 │      │                  │      │                 │
│  Next.js        │─────▶│  FastAPI         │─────▶│  PostgreSQL     │
│  Frontend       │      │  Backend         │      │  Database       │
│                 │      │                  │      │                 │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                │                           
                                │                           
                         ┌──────▼──────┐           
                         │             │           
                         │  Redis      │           
                         │  Cache      │           
                         │             │           
                         └──────┬──────┘           
                                │                           
                         ┌──────▼──────┐           
                         │             │           
                         │  Celery     │           
                         │  Workers    │           
                         │             │           
                         └─────────────┘           
```

### Tech Stack

**Backend:**
- FastAPI (Python 3.11)
- PostgreSQL 15
- Redis 7
- Celery
- SQLAlchemy
- Pydantic

**Frontend:**
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Recharts

**ML/AI:**
- Scikit-learn
- TensorFlow
- Pandas
- NumPy

**DevOps:**
- Docker & Docker Compose
- Prometheus
- Grafana
- Nginx (production)

---

## 📁 Project Structure

```
F:\flable.ai\
├── backend/                  # Backend API (FastAPI)
│   ├── api/                 
│   │   └── routes/          # API endpoints
│   ├── database/            # Models & DB connection
│   ├── integrations/        # Shopify, etc.
│   ├── schemas/             # Pydantic schemas
│   ├── utils/               # Utilities & config
│   ├── main.py              # App entry point
│   ├── celery_app.py        # Background tasks
│   └── requirements.txt     # Python dependencies
├── frontend/                # Frontend (Next.js)
│   └── src/
│       ├── app/             # Pages & routes
│       ├── components/      # React components
│       └── lib/             # Utilities
├── ml-engine/               # AI & ML models
│   ├── campaign_optimizer.py
│   └── models/              # Trained models
├── monitoring/              # Prometheus config
├── logs/                    # Application logs
├── docker-compose.yml       # Service orchestration
├── .env                     # Environment config
├── start.bat                # Windows launcher
├── QUICKSTART.md            # Quick start guide
└── README.md                # This file
```

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
```bash
# Register
POST /auth/register
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "John Doe"
}

# Login
POST /auth/login
{
  "email": "user@example.com",
  "password": "password123"
}

# Returns:
{
  "access_token": "eyJ0eXAiOiJ...",
  "refresh_token": "eyJ0eXAiOiJ...",
  "token_type": "bearer"
}
```

### Campaigns
```bash
# Create campaign
POST /campaigns
Headers: Authorization: Bearer <token>
{
  "name": "Summer Sale",
  "platform": "shopify",
  "daily_budget": 100,
  "target_roas": 3.0,
  "ai_enabled": true
}

# Get campaigns
GET /campaigns
Headers: Authorization: Bearer <token>

# Get campaign performance
GET /campaigns/{id}/performance
Headers: Authorization: Bearer <token>
```

### Shopify Integration
```bash
# Connect store
POST /integrations/shopify
Headers: Authorization: Bearer <token>
{
  "platform": "shopify",
  "shop_domain": "your-store.myshopify.com",
  "access_token": "shpat_..."
}

# Sync data
POST /integrations/{id}/sync
Headers: Authorization: Bearer <token>

# Get products
GET /integrations/shopify/{id}/products
Headers: Authorization: Bearer <token>

# Get orders
GET /integrations/shopify/{id}/orders
Headers: Authorization: Bearer <token>
```

### Analytics
```bash
# Get overview
GET /analytics/overview?days=30
Headers: Authorization: Bearer <token>

# Get campaign trends
GET /analytics/campaign/{id}/trends?days=30
Headers: Authorization: Bearer <token>
```

**Full API Docs**: http://localhost:8000/docs (Swagger UI)

---

## 🛠️ Development

### Backend Development
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

---

## 🔧 Configuration

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://flable:flable123@postgres:5432/flable_db

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
SECRET_KEY=your-secret-key-here

# Shopify
SHOPIFY_API_KEY=your_api_key
SHOPIFY_API_SECRET=your_api_secret
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## 📊 Monitoring

### Prometheus
Access: http://localhost:9090

Metrics available:
- API request rates
- Response times
- Error rates
- Database connections
- Celery task queue length

### Grafana
Access: http://localhost:3001
- Username: `admin`
- Password: `admin`

Pre-built dashboards for:
- Application performance
- Campaign metrics
- System resources

---

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose up -d --build

# View running containers
docker-compose ps

# Execute command in container
docker-compose exec backend python -c "from backend.database.connection import init_db; init_db()"
```

---

## 🚢 Production Deployment

### Prerequisites
- Server with Docker
- Domain name
- SSL certificate

### Steps
1. Update `.env` with production values
2. Set `ENVIRONMENT=production`
3. Use production `docker-compose.prod.yml`
4. Configure nginx reverse proxy
5. Set up SSL/TLS
6. Configure monitoring
7. Set up backups

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed guide.

---

## 🧪 Testing

```bash
# All tests
pytest

# Specific test file
pytest tests/test_campaigns.py

# With coverage
pytest --cov=backend tests/
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🆘 Troubleshooting

### Services won't start
```bash
docker-compose down
docker-compose up -d --build
```

### Database connection issues
```bash
docker-compose exec backend python -c "from backend.database.connection import init_db; init_db()"
```

### Frontend can't connect to backend
Check `frontend/.env.local` has correct API URL

### Port already in use
Edit `docker-compose.yml` and change port mappings

---

## 📞 Support

- 📧 Email: support@flable.ai
- 📖 Documentation: [/docs](/docs)
- 🐛 Issues: [GitHub Issues](https://github.com/yourorg/flable.ai/issues)

---

## 🎯 Roadmap

- [x] Core platform
- [x] Shopify integration
- [x] AI optimization
- [x] Real-time analytics
- [ ] Google Ads integration
- [ ] Facebook Ads integration
- [ ] Advanced ML models
- [ ] Mobile apps
- [ ] Multi-tenant support
- [ ] White-label solution

---

## 🙏 Acknowledgments

- FastAPI team
- Next.js team
- Shopify API
- All open-source contributors

---

<div align="center">

**Built with ❤️ for E-commerce Success**

[Get Started](#-quick-start) • [Documentation](#-api-documentation) • [Support](#-support)

</div>
