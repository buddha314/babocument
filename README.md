# Babocument

**Multi-Agent AI System for Academic Paper Analysis and Research Assistance**

Babocument is a FastAPI-based backend server that provides AI-powered research assistance through a multi-agent system. It features semantic search, document analysis, and conversational AI for academic papers.

> **Client Repositories:**  
> - **[beabodocl-babylon](https://github.com/buddha314/beabodocl-babylon)** - 3D VR/WebXR client (active development)
> - Additional clients (mobile, desktop, CLI) - planned
>
> **Local Development:** Primary client is located at `C:\Users\b\src\beabodocl-babylon`

## Overview

Babocument serves as the backend engine for multiple client applications. The first client, **beabodocl-babylon**, provides an immersive 3D/VR research interface using Babylon.js and WebXR.

### Architecture

```

   Client Applications (Multiple)    
   - beabodocl-babylon (3D/VR)       
   - Mobile apps (planned)            
   - Desktop apps (planned)           
   - CLI tools (planned)              

                REST API
               

   Babocument (This Repo)             
   - FastAPI Server                   
   - Multi-Agent AI System            
   - Vector Database (ChromaDB)       
   - LLM Integration (Ollama)         
   - Document Processing              
-
```

### Features

- **Multi-Agent AI System** - Specialized agents for different research tasks
- **Semantic Search** - Vector-based paper search with ChromaDB
- **Document Analysis** - PDF processing and metadata extraction
- **Conversational Interface** - Natural language research assistance
- **RESTful API** - Client-agnostic HTTP API
- **Real-time Updates** - WebSocket support (planned)

### Current Database

The server includes 4 indexed research papers on 3D bioprinting:
- AI applications in bioprinting
- Bioink formulation and manufacturing
- Bioengineering applications
- Comprehensive bioinks overview

See `data/papers/README.md` for details.

## Quick Start

### Starting the Server

Use the simple start script:

```powershell
# Windows PowerShell
cd C:\Users\b\src\babocument
.\start.ps1           # Default port 8000
.\start.ps1 -Port 8001  # Custom port
.\start.ps1 -Help       # Show help
```

Or use the development launcher with network configuration:

```powershell
.\start-dev.ps1
```

### Manual Start

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access Points

- **API Server:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## API Endpoints

### Agent Chat
- `POST /api/v1/agent/chat` - Chat with research assistant
- `GET /api/v1/agent/conversations/{id}` - Get conversation history
- `DELETE /api/v1/agent/conversations/{id}` - Delete conversation

### Documents
- `GET /api/v1/documents` - List all documents
- `POST /api/v1/documents` - Upload new document
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete document

### Search
- `POST /api/v1/documents/search` - Semantic search
- `GET /api/v1/stats` - Database statistics

See full API documentation at `/docs` when server is running.

