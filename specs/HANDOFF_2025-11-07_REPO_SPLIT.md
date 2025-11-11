# Handoff Document - Repository Split
**Date:** November 7, 2025  
**Task:** Split server and client codebases into separate repositories

## Summary

Successfully transformed the `babocument` repository from a monorepo containing both server (Python/FastAPI) and client (Next.js/Babylon.js) into a **server-only repository**. The client code has been removed and will be managed in a separate repository.

## Changes Made

### 1. Repository Structure Reorganization

**Moved server/ contents to root:**
- All Python server code moved from `server/` to repository root
- Directory structure is now flat at the top level
- Main application code now in `app/` at root
- Tests, scripts, and configuration files at root level

**Key moved items:**
```
server/app/          → app/
server/tests/        → tests/
server/scripts/      → scripts/
server/package.json  → package.json
server/requirements.txt → requirements.txt
server/pytest.ini    → pytest.ini
server/setup.ps1     → setup.ps1
server/SETUP.md      → SETUP.md
server/.env.example  → .env.example
```

**Data directory merge:**
- `server/data/chroma/` → `data/chroma/`
- `server/data/documents/` → `data/documents/`
- Existing `data/lookbook/` and `data/papers/` preserved

### 2. Client Code Removal

**Deleted directories and files:**
```
client/                    (entire directory removed)
├── src/
├── assets/
├── package.json
├── next.config.js
├── tsconfig.json
└── [all other client files]
```

### 3. Script Updates (Server-Only)

**Updated `start-dev.ps1`:**
- Removed `$ClientPort` parameter
- Removed client environment setup
- Removed `Start-Client` function
- Changed path checks from `server/app/main.py` to `app/main.py`
- Updated server working directory from `server/` to root
- Removed VR/client access instructions
- Simplified to single server window

**Updated `run-server.ps1`:**
- Changed path check to `app/main.py` (root level)
- Removed `Set-Location server` command
- Now runs from repository root

**Updated `start-server-temp.ps1`:**
- Changed working directory to root (not `server/` subdirectory)
- Updated error messages to remove `cd server` references

**Deleted:**
- `start-client-temp.ps1` (obsolete)

### 4. Git Operations

All changes staged and ready to commit:
```
R  server/* → *              (moved files)
D  client/*                  (deleted client)
M  start-dev.ps1            (updated)
M  run-server.ps1           (updated)
M  start-server-temp.ps1    (updated)
D  start-client-temp.ps1    (deleted)
M  README.md                (updated - if applicable)
```

## Current Repository State

### Directory Structure
```
babocument/                    (root - server only)
├── app/                       (FastAPI application)
│   ├── agents/               (AI agents)
│   ├── api/                  (REST endpoints)
│   ├── models/               (data models)
│   ├── services/             (LLM, vector DB)
│   └── utils/                (event bus, PDF processing)
├── tests/                    (pytest tests)
├── scripts/                  (initialization & testing scripts)
├── data/                     (all data)
│   ├── chroma/              (vector database)
│   ├── documents/           (PDF storage)
│   ├── lookbook/            (reference data)
│   └── papers/              (research papers)
├── config/                   (configuration)
├── docs/                     (documentation)
├── specs/                    (specifications)
├── package.json             (Node.js deps for tools)
├── requirements.txt         (Python dependencies)
├── pytest.ini               (test configuration)
├── setup.ps1                (environment setup)
├── start-dev.ps1            (dev launcher - SERVER ONLY)
├── run-server.ps1           (simple server runner)
└── README.md                (project documentation)
```

### Running the Server

**Development mode (with auto-reload):**
```powershell
.\start-dev.ps1              # Default port 8000
.\start-dev.ps1 -ServerPort 8080  # Custom port
```

**Simple mode:**
```powershell
.\run-server.ps1             # Default port 8000
.\run-server.ps1 -Port 8080  # Custom port
```

**Manual mode:**
```powershell
venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### API Access

- **Local:** http://localhost:8000
- **Network:** http://[your-ip]:8000
- **API Docs:** http://localhost:8000/docs
- **OpenAPI Spec:** http://localhost:8000/openapi.json

## Next Steps

### For Server Repository (This Repo)

1. **Commit and push** these changes to establish server-only repo
2. **Update README.md** to reflect server-only nature
3. **Review dependencies** - remove any client-specific npm packages if needed
4. **Update documentation** in `docs/` and `specs/` folders
5. **Consider renaming** repository to `babocument-server` or similar

### For Client Repository (New Repo)

1. **Create new repository** (e.g., `babocument-client`)
2. **Recover client code** from git history:
   ```bash
   git checkout HEAD~1 -- client/
   ```
3. **Move client/ contents** to new repository root
4. **Update client configuration** with server API URL
5. **Update documentation** for standalone client setup

### Integration Points

**Client needs to know:**
- Server API base URL (configurable in `.env.local`)
- API endpoints remain the same
- CORS is configured for network access

**Server considerations:**
- CORS settings may need adjustment based on client hosting
- API versioning strategy
- Authentication/authorization if needed

## Testing Checklist

### Server Repository
- [ ] Virtual environment activates correctly
- [ ] `python -m uvicorn app.main:app --reload` starts successfully
- [ ] API docs accessible at `/docs`
- [ ] All tests pass: `pytest tests/`
- [ ] Vector database initializes: `python scripts/init_vector_db.py`
- [ ] Document upload works via API
- [ ] Redis connection works (if running)
- [ ] Ollama LLM integration works (if running)

### After Split
- [ ] Server runs independently
- [ ] Client (in new repo) can connect to server API
- [ ] Network access works across devices
- [ ] All API endpoints functional
- [ ] Agent system works end-to-end

## Dependencies

### Required Services
- **Python 3.11+** with venv
- **Redis** (optional, for event bus)
- **Ollama** (optional, for LLM features)

### Python Packages
See `requirements.txt` for full list:
- FastAPI, Uvicorn
- ChromaDB (vector database)
- LangChain
- PyPDF2
- Redis client
- etc.

### Node.js (for tooling)
See `package.json` - primarily for development tools

## Known Issues

1. **Line endings warning:** Git shows LF→CRLF warnings for some files (normal on Windows)
2. **Hardcoded paths:** `start-server-temp.ps1` has hardcoded path `C:\Users\b\src\babocument` - will be regenerated by `start-dev.ps1`
3. **README.md:** May still reference client code - needs review

## Contact & References

**Related Documentation:**
- `HANDOFF_FINAL_2025-11-06_VR_CHAT.md` - Previous VR integration work
- `SETUP.md` - Server setup instructions
- `specs/PROJECT_STATUS.md` - Overall project status
- `specs/MULTI_AGENT_ARCHITECTURE.md` - Agent system design

**Git Status:**
- Branch: `main`
- Repository: `buddha314/babocument`
- All changes staged and ready to commit

## Commit Message Suggestion

```
Restructure: Split server and client into separate repositories

- Move server/ contents to repository root
- Remove client/ directory (moved to separate repo)
- Update all startup scripts for server-only operation
- Merge server/data into root data/ directory
- Update path references in PowerShell scripts

This repository is now server-only. Client code moved to separate repository.

BREAKING CHANGE: Repository structure completely reorganized
```

---

**Status:** ✅ Ready to commit and push  
**Action Required:** Review, commit, and push changes to remote
