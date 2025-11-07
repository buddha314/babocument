# Babocument Server

This is the server component of the Babocument project - a multi-agent AI system for academic paper analysis and research assistance.

> **Note:** The BabylonJS client has been moved to a separate repository: [beabodocl-babylon](https://github.com/buddha314/beabodocl-babylon)
> 
> **Local Development:** Client is located at `C:\Users\b\src\beabodocl-babylon`

## Configuration

This document explains how to configure the Babocument server for local development.

## LLM Model Storage Configuration

The server uses Ollama for local LLM hosting. By default, Ollama stores models in your user directory, but you can configure a custom storage location.

### Setting Custom Model Storage Path

**Current Configuration:** Models are stored at `d:\models`

To use this configuration:

1. **Environment Variable Method (Recommended):**
   - The `.env` file already sets `OLLAMA_MODELS=d:/models`
   - Ollama will read this environment variable when started

2. **System Environment Variable (Alternative):**
   ```powershell
   # Set permanently in PowerShell (requires restart)
   [System.Environment]::SetEnvironmentVariable('OLLAMA_MODELS', 'd:\models', 'User')
   ```

3. **Docker Method (Future):**
   ```yaml
   # docker-compose.yml (when created)
   services:
     ollama:
       environment:
         - OLLAMA_MODELS=d:/models
       volumes:
         - d:/models:/root/.ollama/models
   ```

### Verify Configuration

After setting up, verify the configuration:

```powershell
# Check if Ollama is using the correct path
ollama list

# Check where models are stored
dir d:\models
```

### Downloading Models

Once configured, download the recommended models:

```powershell
# For summaries (fast, 2GB)
ollama pull llama3.2:3b

# For conversations (Librarian, 4.4GB)
ollama pull qwen2.5:7b

# For instruction following (4.1GB)
ollama pull mistral:7b

# For best quality (4.7GB)
ollama pull llama3.1:8b
```

All models will be stored in `d:\models`.

## Environment Configuration

The server uses environment variables for configuration. Two files are provided:

- **`.env.example`** - Template with all available configuration options
- **`.env`** - Active configuration (gitignored, already configured)

### Key Configuration Options

#### LLM Settings
- `OLLAMA_BASE_URL` - Ollama API endpoint (default: http://localhost:11434)
- `OLLAMA_MODELS` - Model storage directory (set to: d:/models)
- `LLM_MODEL` - Default model to use (default: ollama/llama3.2:3b)
- `LLM_TEMPERATURE` - Generation temperature (default: 0.7)
- `LLM_MAX_TOKENS` - Maximum tokens per response (default: 500)

#### Vector Database Settings
- `CHROMA_PERSIST_DIRECTORY` - ChromaDB storage path (default: ./data/chroma)
- `EMBEDDING_MODEL` - Model for embeddings (default: all-MiniLM-L6-v2)

#### Application Settings
- `HOST` - Server bind address (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `ENVIRONMENT` - Environment type (default: development)
- `LOG_LEVEL` - Logging verbosity (default: INFO)

## Directory Structure

```
server/
├── .env                    # Active configuration (gitignored)
├── .env.example            # Configuration template
├── config/                 # Configuration files directory
├── data/                   # Data storage (gitignored)
│   └── chroma/             # Vector database storage
└── README.md               # This file
```

## Next Steps

After configuration:

1. **Install Ollama** (if not already installed):
   ```powershell
   # Download from: https://ollama.com/download
   # Or use winget
   winget install Ollama.Ollama
   ```

2. **Download Models** (see above section)

3. **Install Python Dependencies** (Phase 1):
   ```powershell
   pip install chromadb sentence-transformers litellm
   ```

4. **Initialize Vector Database** (Phase 1):
   ```powershell
   python scripts/init_vector_db.py
   ```

## References

- [LLM Hosting Decision](../specs/LLM_HOSTING_DECISION.md)
- [Vector Database Decision](../specs/VECTOR_DATABASE_DECISION.md)
- [Project Tasks](../specs/TASKS.md)
- [Ollama Documentation](https://ollama.com/)

## Troubleshooting

### Models not found in d:\models

If Ollama doesn't use the configured path:

1. Check environment variable:
   ```powershell
   $env:OLLAMA_MODELS
   ```

2. Restart Ollama service:
   ```powershell
   # Stop Ollama (if running)
   taskkill /F /IM ollama.exe
   
   # Start Ollama with environment variable
   $env:OLLAMA_MODELS="d:\models"; ollama serve
   ```

3. Verify storage location:
   ```powershell
   ollama list
   dir d:\models
   ```

### Permission Issues

Ensure the `d:\models` directory exists and is writable:

```powershell
# Create directory if it doesn't exist
New-Item -ItemType Directory -Force -Path d:\models

# Check permissions
icacls d:\models
```
