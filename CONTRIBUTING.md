# Contributing to Anjoman

Thank you for your interest in contributing to Anjoman! This is an early-stage open-source project, and we welcome contributions of all kinds.

## Ways to Contribute

- **Bug Reports**: Found a bug? Open an issue with details
- **Feature Requests**: Have an idea? Share it in an issue
- **Code Contributions**: Fix bugs or add features via pull requests
- **Documentation**: Improve docs, add examples, or write guides
- **Feedback**: Share your experience using Anjoman

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file with your API keys (see `.env.example`).

### Frontend

```bash
cd frontend
npm install
```

Create a `.env.local` file if needed (see `.env.local.example`).

## Project Structure

```
anjoman/
├── backend/          # FastAPI backend
│   ├── main.py       # API endpoints
│   ├── models.py     # Data models
│   ├── orchestrator.py  # Dana & Ray logic
│   └── session_manager.py  # File-based persistence
├── frontend/         # Next.js frontend
│   ├── app/          # Pages and layouts
│   ├── components/   # React components
│   └── lib/          # API client
└── data/            # Session storage
    └── sessions/
```

## Code Style

- **Python**: Follow PEP 8, use type hints
- **TypeScript/React**: Follow standard TypeScript conventions
- **Formatting**: Use built-in linters (eslint, etc.)

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push and open a pull request

## Design Principles

Anjoman favors:
- **Clarity over speed**: Readable, maintainable code
- **Structure over creativity**: Follow established patterns
- **Transparency over confidence**: Explicit over implicit

## Questions?

Open an issue or reach out to maintainers. We're here to help!

## Code of Conduct

Be respectful, inclusive, and constructive. We're building something useful together.

