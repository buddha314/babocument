# Babocument Server# Babocument



**Multi-Agent AI System for Academic Paper Analysis****Multi-Agent AI System for Academic Paper Analysis and Research Assistance**



> **Status**: ✅ Production Ready (Nov 2025)  > **Status**: ✅ Agent Chat API Fully Functional (Nov 7, 2025)  

> **Client**: [beabodocl-godot](https://github.com/buddha314/beabodocl-godot) - Godot VR/XR client> **Latest**: LLM integration complete, all 4 models installed and working  

> **See**: `specs/HANDOFF_2025-11-07_AGENT_CHAT_WORKING.md` for details

## Overview

Babocument is a FastAPI-based backend server that provides AI-powered research assistance through a multi-agent system. It features semantic search, document analysis, and conversational AI for academic papers.

Babocument is a FastAPI-based research assistant server with multi-agent AI capabilities, semantic search, and conversational interfaces.

> **Client Repository:**  

**Key Features:**> - **Primary**: [beabodocl-godot](https://github.com/buddha314/beabodocl-godot) - Godot VR/XR client (active development)

- 🤖 Multi-agent AI system (Research, Analysis, Summary, Recommendation agents)

- 🔍 Semantic search with ChromaDB vector database## Overview

- 💬 Conversational interface via REST and WebSocket APIs

- 📄 PDF document processing and analysisBabocument serves as the backend engine for client applications. The primary client, **beabodocl-godot**, provides an immersive VR/XR research interface using the Godot Engine.

- 🧠 Local LLM integration via Ollama

### Architecture

## Quick Start

```

### Prerequisites   Client Applications    

- Python 3.11+   - beabodocl-godot (VR/XR)       

- [Ollama](https://ollama.com/download) for LLM hosting

- Redis (optional, for event bus)                REST API

               ↓

### Installation   Babocument (This Repo)             

   - FastAPI Server                   

```powershell   - Multi-Agent AI System            

# 1. Set up environment   - Vector Database (ChromaDB)       

.\setup.ps1  # Automated setup   - LLM Integration (Ollama)         

   - Document Processing              

# 2. Download LLM models```

ollama pull llama3.2:3b    # Fast (2GB)

ollama pull qwen2.5:7b     # Conversations (4.4GB)### Features

ollama pull mistral:7b     # Instructions (4.1GB)

- **Multi-Agent AI System** - Specialized agents for different research tasks

# 3. Start server- **Semantic Search** - Vector-based paper search with ChromaDB

.\start.ps1  # Simple start- **Document Analysis** - PDF processing and metadata extraction

# or- **Conversational Interface** - Natural language research assistance

.\start-dev.ps1  # Development mode with auto-reload- **RESTful API** - Client-agnostic HTTP API

```- **Real-time Updates** - WebSocket support (planned)



### Access### Current Database



- **API Docs**: http://localhost:8000/docsThe server includes 4 indexed research papers on 3D bioprinting:

- **Health Check**: http://localhost:8000/health- AI applications in bioprinting

- **Agent Chat**: `POST /api/v1/agent/chat`- Bioink formulation and manufacturing

- Bioengineering applications

## API Overview- Comprehensive bioinks overview



**Agent Chat:**See `data/papers/README.md` for details.

```bash

curl -X POST http://localhost:8000/api/v1/agent/chat \## Quick Start

  -H "Content-Type: application/json" \

  -d '{"message": "Find papers about bioprinting", "session_id": "test"}'### Starting the Server

```

Use the simple start script:

**Key Endpoints:**

- `/api/v1/agent/chat` - Conversational research assistant```powershell

- `/api/v1/documents` - Document management# Windows PowerShell

- `/api/v1/documents/search` - Semantic searchcd C:\Users\b\src\babocument

- `/api/v1/stats` - System statistics.\start.ps1           # Default port 8000

.\start.ps1 -Port 8001  # Custom port

Full API documentation available at `/docs` endpoint..\start.ps1 -Help       # Show help

```

## Project Structure

Or use the development launcher with network configuration:

```

babocument/```powershell

├── app/.\start-dev.ps1

│   ├── agents/          # AI agents (Research, Analysis, Summary, Recommendation)```

│   ├── api/             # REST API endpoints

│   ├── models/          # Pydantic data models### Manual Start

│   ├── services/        # LLM, vector DB, PDF processing

│   └── utils/           # Event bus, helpers```powershell

├── tests/               # Test suite (pytest)# Activate virtual environment

├── scripts/             # Utility scripts.\venv\Scripts\Activate.ps1

├── specs/               # Architecture & design docs

└── data/                # Document storage & vector DB# Start server

```python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

```

## Configuration

### Access Points

Edit `.env` file (copy from `.env.example`):

- **API Server:** http://localhost:8000

```bash- **API Documentation:** http://localhost:8000/docs

# LLM Configuration- **Health Check:** http://localhost:8000/health

OLLAMA_BASE_URL=http://localhost:11434

LLM_MODEL=ollama/qwen2.5:7b## API Endpoints



# Vector Database### Agent Chat

CHROMA_PERSIST_DIRECTORY=./data/chroma- `POST /api/v1/agent/chat` - Chat with research assistant

EMBEDDING_MODEL=all-MiniLM-L6-v2- `GET /api/v1/agent/conversations/{id}` - Get conversation history

- `DELETE /api/v1/agent/conversations/{id}` - Delete conversation

# Server

HOST=0.0.0.0### Documents

PORT=8000- `GET /api/v1/documents` - List all documents

```- `POST /api/v1/documents` - Upload new document

- `GET /api/v1/documents/{id}` - Get document details

## Documentation- `DELETE /api/v1/documents/{id}` - Delete document



- **Setup Guide**: `SETUP.md` - Detailed environment setup### Search

- **Scripts**: `SCRIPTS.md` - PowerShell script reference- `POST /api/v1/documents/search` - Semantic search

- **Architecture**: `specs/MULTI_AGENT_ARCHITECTURE.md`- `GET /api/v1/stats` - Database statistics

- **Handoffs**: `specs/HANDOFF_*.md` - Development history

- **API Specs**: `specs/` directorySee full API documentation at `/docs` when server is running.



## Development

```powershell
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/

# Start development server
.\start-dev.ps1

# Initialize vector database
python scripts/init_vector_db.py
```

## Client Integration

The primary client is [beabodocl-godot](https://github.com/buddha314/beabodocl-godot), a Godot Engine-based VR/XR application.

**Integration Points:**
- REST API for CRUD operations
- WebSocket for real-time chat: `ws://localhost:8000/ws/agent/{session_id}`
- CORS enabled for local development
- OpenAPI spec: http://localhost:8000/openapi.json

## Architecture

```
Client (Godot VR/XR)
        ↓
   REST + WebSocket
        ↓
Babocument Server
  ├── Agent Coordinator
  │   ├── Research Agent
  │   ├── Analysis Agent
  │   ├── Summary Agent
  │   └── Recommendation Agent
  ├── Vector Database (ChromaDB)
  ├── LLM Client (Ollama)
  └── Document Processing
```

## License

MIT License - See `LICENSE` file

## Links

- **Client Repository**: https://github.com/buddha314/beabodocl-godot
- **Server Repository**: https://github.com/buddha314/babocument
- **Issues**: https://github.com/buddha314/babocument/issues

---

**Last Updated**: November 11, 2025
