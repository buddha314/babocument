# Babocument Server - Phase 1 Backend Setup

## Quick Reference

**Essential Configuration Files:**
- `.env` - Environment variables and configuration
- `app/config.py` - Configuration class (reads from `.env`)
- `app/services/llm_client.py` - Model assignments and LLM settings

**Model Storage Location:**
- Environment Variable: `OLLAMA_MODELS` (set to `d:\models`)
- Configuration: `.env` file, `OLLAMA_MODELS=d:/models`
- Verify: Run `$env:OLLAMA_MODELS` in PowerShell

**Required Models (16 GB total):**
- `llama3.2:3b` (2.0 GB) - Summarization
- `qwen2.5:7b` (4.7 GB) - Chat/Conversation
- `mistral:7b` (4.4 GB) - Instructions/Parsing
- `llama3.1:8b` (4.9 GB) - Analysis

---

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

### 5. Configure Ollama Model Storage Location

**Important**: By default, Ollama stores models in your user profile. To use a custom location (recommended for larger drives):

```powershell
# Set the models directory to D:\models (or your preferred location)
# This sets it for the current session and permanently for your user account
$env:OLLAMA_MODELS = "d:\models"
[System.Environment]::SetEnvironmentVariable("OLLAMA_MODELS", "d:\models", "User")

# Create the directory if it doesn't exist
New-Item -Path "d:\models" -ItemType Directory -Force

# Verify the setting
Write-Host "Ollama models will be stored in: $env:OLLAMA_MODELS"
```

**Note**: You need to restart Ollama after changing the `OLLAMA_MODELS` environment variable:
```powershell
# Stop Ollama (if running as a service)
taskkill /IM ollama.exe /F

# Start Ollama again (it will auto-start, or run)
ollama serve
```

The model storage location is also configured in the `.env` file:
```
OLLAMA_MODELS=d:/models
```

### 6. Download Required LLM Models

Download all four models required by the agent system (~16 GB total):

```powershell
# For summarization (2.0 GB) - Fast, efficient summaries
ollama pull llama3.2:3b

# For conversations (4.7 GB) - Natural dialogue, chat interface
ollama pull qwen2.5:7b

# For instruction following (4.4 GB) - Query parsing, structured output
ollama pull mistral:7b

# For analysis tasks (4.9 GB) - Factual analysis, comparisons
ollama pull llama3.1:8b

# Verify all models are downloaded
ollama list
```

Expected output:
```
NAME           ID              SIZE      MODIFIED
llama3.1:8b    46e0c10c039e    4.9 GB    X minutes ago
mistral:7b     6577803aa9a0    4.4 GB    X minutes ago
qwen2.5:7b     845dbda0ea48    4.7 GB    X minutes ago
llama3.2:3b    a80c4f17acd5    2.0 GB    X minutes ago
```

**Model Usage**:
- `llama3.2:3b` - Summary agent (fast, efficient)
- `qwen2.5:7b` - Chat agent (natural conversation)
- `mistral:7b` - Research agent (query understanding, keyword extraction)
- `llama3.1:8b` - Analysis agent (structured output, factual)

**Note**: Downloads may take 10-30 minutes depending on your internet connection. Models are stored in `d:\models` (or your configured location).

### 6. Install and Start Redis (optional - for event bus)

**Note**: The server will run without Redis, but some real-time features may be limited.

```powershell
# Option 1: Docker (recommended)
docker run -d -p 6379:6379 --name babocument-redis redis:7-alpine

# Option 2: Windows Redis port
# Download from: https://github.com/tporadowski/redis/releases

# Option 3: Skip Redis - Server will continue without it
# You'll see a warning but the agent API will work
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

# Test agent chat API
$body = @{ message = "What papers do you have about bioprinting?" } | ConvertTo-Json
curl -Method POST -Uri "http://localhost:8000/api/v1/agent/chat" -ContentType "application/json" -Body $body

# You should see a response with paper summaries
```

**Successful Test Results:**
- Health endpoint returns `{"status":"healthy","environment":"development"}`
- Agent chat returns paper summaries with structured content
- No Redis errors (or warning that server continues without Redis)
- LLM responses include bullet points and key findings

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

```bash
# LLM Configuration (Ollama)
OLLAMA_MODELS=d:/models              # Where Ollama stores downloaded models
OLLAMA_BASE_URL=http://localhost:11434  # Ollama API endpoint
LLM_MODEL=ollama/llama3.2:3b         # Default model (for backward compatibility)
LLM_TEMPERATURE=0.7                   # Sampling temperature (0.0-1.0)
LLM_MAX_TOKENS=500                    # Maximum tokens per response
LLM_TIMEOUT=30                        # Request timeout in seconds

# Vector Database (ChromaDB)
CHROMA_PERSIST_DIRECTORY=./data/chroma  # Vector DB storage location
EMBEDDING_MODEL=all-MiniLM-L6-v2        # Sentence transformer model

# Server Configuration
HOST=0.0.0.0                          # Server host
PORT=8000                             # Server port
DEBUG=True                            # Debug mode
ENVIRONMENT=development               # Environment name

# Redis (Optional - for event bus)
REDIS_HOST=localhost                  # Redis host
REDIS_PORT=6379                       # Redis port
```

**Important Configuration Notes**:

1. **`OLLAMA_MODELS`** - This must match your system environment variable:
   ```powershell
   # Check current setting
   $env:OLLAMA_MODELS
   
   # If not set, configure it (see step 5 above)
   [System.Environment]::SetEnvironmentVariable("OLLAMA_MODELS", "d:\models", "User")
   ```

2. **Model Selection** - The system uses different models for different tasks (configured in `app/services/llm_client.py`):
   - Summarization: `llama3.2:3b`
   - Chat: `qwen2.5:7b`
   - Instructions: `mistral:7b`
   - Analysis: `llama3.1:8b`

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

# Test Ollama API
curl http://localhost:11434/api/tags
```

### Models Not Found / LLM Errors
```powershell
# Verify models are installed
ollama list

# Check model storage location matches environment variable
Write-Host "OLLAMA_MODELS: $env:OLLAMA_MODELS"
Get-ChildItem $env:OLLAMA_MODELS -Directory | Select Name

# Re-download a model if needed
ollama pull llama3.2:3b

# Verify model works
ollama run llama3.2:3b "Hello"
```

### Wrong Model Storage Location
If models are downloading to the wrong location:

```powershell
# 1. Stop Ollama completely
taskkill /IM ollama.exe /F

# 2. Set the environment variable for your user account
[System.Environment]::SetEnvironmentVariable("OLLAMA_MODELS", "d:\models", "User")

# 3. Verify it's set (you may need to restart PowerShell)
[System.Environment]::GetEnvironmentVariable("OLLAMA_MODELS", "User")

# 4. Start a new PowerShell window and verify
$env:OLLAMA_MODELS  # Should show d:\models

# 5. Pull models again
ollama pull llama3.2:3b
```

### Redis Connection Error
```powershell
# The server will continue without Redis - this is normal
# If you want to enable Redis:

# Check if Redis is running
docker ps | Select-String redis

# Start Redis if not running
docker start babocument-redis

# Test Redis connection
docker exec -it babocument-redis redis-cli ping
# Should return: PONG
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
