```markdown
# Insight Connector

Integration layer between Creative Collaboration Hub and Personal Insight Engine to deliver personalized creative collaboration experiences.

## Project Overview

**Mission**: Leverage existing user understanding from the Personal Insight Engine to personalize and enhance the creative collaboration experience.

**Core Values**: Intuition, creativity, autonomy, meaning, innovation

## Architecture

### Components

1. **Insight Integration Service** - Bridges collaboration hub with insight engine
2. **User Context Manager** - Maintains real-time user understanding
3. **Personalization Engine** - Applies insights to collaboration features
4. **Real-time Sync Layer** - Keeps insights current during sessions
5. **Analytics & Feedback Loop** - Improves personalization over time

## Tech Stack

- **Backend**: Python (FastAPI, SQLAlchemy)
- **Frontend**: React with TypeScript
- **Database**: PostgreSQL
- **Caching**: Redis
- **Real-time**: WebSockets
- **Voice**: Integration-ready interfaces

## Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database
alembic upgrade head

# Run
python -m uvicorn app.main:app --reload
```

## Documentation

- [Architecture](./docs/ARCHITECTURE.md)
- [API Reference](./docs/API.md)
- [Database Schema](./docs/DATABASE.md)
- [Integration Guide](./docs/INTEGRATION.md)
- [Deployment](./docs/DEPLOYMENT.md)

## Project Structure

```
insight-connector/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── api/
│   │   └── utils/
│   ├── tests/
│   ├── migrations/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── types/
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
├── infrastructure/
│   ├── docker-compose.yml
│   ├── kubernetes/
│   └── terraform/
├── docs/
└── .env.example
```

## Key Features

- **Contextual Awareness**: Real-time user understanding integration
- **Adaptive Personalization**: Insights-driven feature recommendations
- **Seamless Sync**: Bi-directional data flow with insight engine
- **Privacy-First**: Secure, encrypted insight handling
- **Performance Optimized**: Redis caching for instant personalization
- **Voice-Ready**: Integration points for voice interfaces

## Development

```bash
# Run tests
pytest

# Format code
black . && isort .

# Type checking
mypy app/

# Linting
flake8 app/
```

## Deployment

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for comprehensive deployment instructions.

## Contributing

Follow the architecture guidelines and ensure all tests pass before submitting.

## License

Proprietary - Internal Use Only
```
