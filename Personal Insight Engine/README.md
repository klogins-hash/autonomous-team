```markdown
# Personal Insight Engine

An adaptive system that captures, analyzes, and synthesizes personal patterns across multiple domains (thoughts, activities, decisions, creative work) to surface meaningful insights and support intuitive decision-making.

## Project Overview

The Personal Insight Engine is designed to:
- **Capture** multi-modal data (text, voice, activity logs)
- **Analyze** patterns across personal domains
- **Synthesize** meaningful insights
- **Visualize** patterns intuitively
- **Protect** privacy through end-to-end encryption

## Architecture

### Core Components
- **Data Ingestion Layer**: Multi-modal data collection (voice, text, activity)
- **Pattern Recognition Engine**: ML-based pattern detection and clustering
- **Insight Synthesis Engine**: Contextual insight generation
- **Visualization Interface**: React-based intuitive UI
- **Privacy Layer**: End-to-end encryption and data anonymization

### Tech Stack
- **Backend**: Python (FastAPI, SQLAlchemy)
- **Frontend**: React with TypeScript
- **Database**: PostgreSQL
- **Caching**: Redis
- **Voice Processing**: Whisper API + custom voice handlers
- **ML/Analytics**: scikit-learn, pandas, numpy
- **Infrastructure**: Docker, Kubernetes-ready

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose

### Installation

```bash
# Clone and setup
cd /root/CascadeProjects/Personal\ Insight\ Engine

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Infrastructure setup
cd ../infrastructure
docker-compose up -d
```

### Running the Application

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm start

# Terminal 3: Pattern processor (async tasks)
cd backend
celery -A app.tasks worker --loglevel=info
```

## Project Structure

```
Personal Insight Engine/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── config.py          # Configuration management
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── api/               # API routes
│   │   ├── services/          # Business logic
│   │   ├── engines/           # Core engines
│   │   ├── utils/             # Utilities
│   │   └── middleware/        # Custom middleware
│   ├── tests/                 # Test suite
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment template
│   └── Dockerfile             # Container configuration
├── frontend/                  # React TypeScript frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   ├── hooks/             # Custom hooks
│   │   ├── types/             # TypeScript types
│   │   ├── utils/             # Utilities
│   │   ├── styles/            # Global styles
│   │   └── App.tsx            # Root component
│   ├── public/                # Static assets
│   ├── package.json           # Dependencies
│   └── Dockerfile             # Container configuration
├── infrastructure/            # Infrastructure as Code
│   ├── docker-compose.yml     # Local development
│   ├── kubernetes/            # K8s manifests
│   ├── terraform/             # IaC for cloud
│   └── monitoring/            # Monitoring configs
├── docs/                      # Documentation
│   ├── API.md                 # API documentation
│   ├── ARCHITECTURE.md        # Architecture details
│   ├── PRIVACY.md             # Privacy & security
│   └── DEPLOYMENT.md          # Deployment guide
└── scripts/                   # Utility scripts
```

## Key Features

### 1. Multi-Modal Data Capture
- Text journaling and notes
- Voice recording and transcription
- Activity tracking integration
- Automatic data collection

### 2. Pattern Recognition
- Temporal pattern detection
- Cross-domain correlation
- Behavioral clustering
- Anomaly detection

### 3. Insight Synthesis
- Contextual insight generation
- Trend analysis
- Decision support
- Creative pattern surfacing

### 4. Intuitive Visualization
- Interactive dashboards
- Pattern timelines
- Correlation networks
- Insight cards

### 5. Privacy-First Design
- End-to-end encryption
- Local processing options
- Data anonymization
- User-controlled retention

## Configuration

See `.env.example` for all configuration options:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/insight_engine
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# Services
OPENAI_API_KEY=your-openai-key
VOICE_PROVIDER=openai  # or local

# Features
ENABLE_VOICE_CAPTURE=true
ENABLE_ACTIVITY_TRACKING=true
PATTERN_ANALYSIS_INTERVAL=3600
```

## API Documentation

Full API documentation available at `/docs` when running the backend.

Key endpoints:
- `POST /api/v1/entries` - Create new entry
- `GET /api/v1/entries` - List entries
- `POST /api/v1/voice/transcribe` - Transcribe voice
- `GET /api/v1/patterns` - Get detected patterns
- `GET /api/v1/insights` - Get synthesized insights
- `GET /api/v1/dashboard` - Get dashboard data

## Development

### Running Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Code Quality

```bash
# Linting
black app/
flake8 app/
mypy app/

# Frontend
cd frontend
npm run lint
npm run type-check
```

## Deployment

### Docker Compose (Development)
```bash
cd infrastructure
docker-compose up -d
```

### Kubernetes (Production)
```bash
cd infrastructure/kubernetes
kubectl apply -f namespace.yaml
kubectl apply -f postgres/
kubectl apply -f redis/
kubectl apply -f backend/
kubectl apply -f frontend/
```

### Terraform (Cloud Infrastructure)
```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

## Monitoring

- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **ELK Stack**: Log aggregation
- **Sentry**: Error tracking

Access at:
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

## Security

- All data encrypted at rest and in transit
- JWT-based authentication
- Role-based access control
- Regular security audits
- GDPR/CCPA compliant

See `docs/PRIVACY.md` for detailed security information.

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit pull request

## License

Proprietary - All rights reserved

## Support

For issues and questions, contact the development team.

---

**Last Updated**: 2024
**Status**: Production Ready
**Version**: 1.0.0
```