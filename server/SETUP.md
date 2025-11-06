# Babocument Server - Phase 1 Backend Setup

## Quick Start

### 1. Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Install Dependencies

```powershell
# Install all requirements
pip install -r requirements.txt

# Or install specific groups
pip install -r requirements.txt --no-deps  # Install without dependencies
```

### 3. Configure Environment

```powershell
# Copy example configuration
Copy-Item .env.example .env

# Edit .env to match your setup
# Already configured with OLLAMA_MODELS=d:/models
```

### 4. Install Ollama (if not already installed)

```powershell
# Using winget
winget install Ollama.Ollama

# Or download from: https://ollama.com/download
```

### 5. Download LLM Models

```powershell
# For summaries (fast, 2GB)
ollama pull llama3.2:3b

# For conversations (4.4GB) - Librarian
ollama pull qwen2.5:7b

# For instruction following (4.1GB)
ollama pull mistral:7b

# Check downloaded models
ollama list
```

### 6. Install and Start Redis (required for event bus)

```powershell
# Option 1: Docker (recommended)
docker run -d -p 6379:6379 --name babocument-redis redis:7-alpine

# Option 2: Windows Redis port
# Download from: https://github.com/tporadowski/redis/releases
```

### 7. Run the Server

```powershell
# Development mode (with auto-reload)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the shortcut
python app/main.py
```

### 8. Test the Server

```powershell
# Check health endpoint
curl http://localhost:8000/health

# View API docs
# Open browser: http://localhost:8000/docs
```

## Project Structure

```
server/
├── app/
│   ├── __init__.py             # Package initialization
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── agents/                 # Multi-agent system
│   │   ├── __init__.py
│   │   ├── base.py             # Base agent class
│   │   ├── coordinator.py      # Agent coordinator
│   │   └── research.py         # Research agent (skeleton)
│   ├── api/                    # REST and WebSocket endpoints
│   │   └── __init__.py
│   ├── models/                 # Pydantic models
│   │   └── __init__.py
│   ├── services/               # External service clients
│   │   └── __init__.py
│   └── utils/                  # Utility functions
│       └── __init__.py
├── config/                     # Additional config files
├── data/                       # Data storage (gitignored)
│   └── chroma/                 # Vector database storage
├── tests/                      # Test files
├── .env                        # Environment variables (gitignored)
├── .env.example                # Example environment config
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Configuration

See [Configuration Documentation](README.md) for detailed configuration options.

Key settings in `.env`:
- `OLLAMA_MODELS=d:/models` - LLM model storage location
- `OLLAMA_BASE_URL=http://localhost:11434` - Ollama API endpoint
- `CHROMA_PERSIST_DIRECTORY=./data/chroma` - Vector DB storage

## Development

### Running Tests

```powershell
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

### Code Quality

```powershell
# Format code with Black
black app/

# Lint with Ruff
ruff check app/

# Type checking with mypy
mypy app/
```

## Phase 1 Status

### ✅ Completed
- [x] Project structure created
- [x] Configuration management (Pydantic Settings)
- [x] FastAPI application skeleton
- [x] Base agent class
- [x] Agent coordinator skeleton
- [x] Research agent skeleton
- [x] Logging with structlog
- [x] Environment configuration

### 🚧 In Progress
- [ ] Install dependencies in virtual environment
- [ ] Test basic server startup
- [ ] Implement vector database client
- [ ] Implement LLM client wrapper
- [ ] Complete REST API endpoints
- [ ] Implement WebSocket handlers

### 📋 Next Steps (Phase 1)
1. Install dependencies: `pip install -r requirements.txt`
2. Start Redis: `docker run -d -p 6379:6379 redis:7-alpine`
3. Test server: `python app/main.py`
4. Implement Vector Database client (ChromaDB)
5. Implement LLM client (LiteLLM + Ollama)
6. Create REST API endpoints
7. Add WebSocket support for real-time updates

## Troubleshooting

### Import Errors
If you see import errors, ensure:
1. Virtual environment is activated
2. Dependencies are installed: `pip install -r requirements.txt`
3. You're in the correct directory: `cd server`

### Ollama Not Running
```powershell
# Check if Ollama is running
ollama list

# If not, start it
ollama serve
```

### Redis Connection Error
```powershell
# Check if Redis is running
docker ps | Select-String redis

# Start Redis if not running
docker start babocument-redis
```

### Port Already in Use
```powershell
# Find process using port 8000
netstat -ano | Select-String ":8000"

# Kill the process (replace PID)
taskkill /F /PID <PID>
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Ollama Documentation](https://ollama.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Project Specifications](../specs/)
  - [Multi-Agent Architecture](../specs/MULTI_AGENT_ARCHITECTURE.md)
  - [Communication Protocol](../specs/COMMUNICATION_PROTOCOL_DECISION.md)
  - [LLM Hosting Decision](../specs/LLM_HOSTING_DECISION.md)
  - [Vector Database Decision](../specs/VECTOR_DATABASE_DECISION.md)
