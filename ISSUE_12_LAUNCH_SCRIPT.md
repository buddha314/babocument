# Issue #12: Launch Script Implementation Guide

**Created:** 2025-11-06
**Priority:** Critical (DevOps)
**Status:** Ready for Implementation
**Estimated Time:** 1-2 hours

## Overview

Create a unified launch script that starts both the server (when implemented) and client with a single command. This is a **critical priority** DevOps improvement that provides immediate value and streamlines development across all project phases.

## Why Critical Priority?

1. **Immediate Value**: Client development is active now (Phase 0-3)
2. **Developer Experience**: Single command replaces manual multi-step process
3. **Onboarding**: New developers get running in seconds
4. **Phase 1+ Essential**: When FastAgent server is implemented, seamless integration
5. **No Dependencies**: Can implement immediately - no blocking issues

## Current Manual Process (Pain Points)

### Starting Client
```powershell
cd c:\Users\b\src\babocument\client
npm install  # First time or after package updates
npm run dev  # Starts on http://localhost:3000
```

### Starting Server (Future)
```powershell
cd c:\Users\b\src\babocument\server
pip install -r requirements.txt  # First time or updates
python -m uvicorn main:app --reload  # Starts on http://localhost:8000
```

**Problems:**
- Manual navigation between directories
- Forgetting to install dependencies
- Managing multiple terminal windows
- No automated environment validation

## Proposed Solution: `launch.ps1`

### Features

1. **Environment Validation**
   - Check Python installation (for server)
   - Check Node.js installation (for client)
   - Verify package managers (pip, npm)

2. **Dependency Management**
   - Prompt to install dependencies if missing
   - Skip with `--no-install` flag

3. **Process Management**
   - Start both server and client in background
   - Colorized console output
   - Process status indicators
   - Graceful shutdown on Ctrl+C

4. **Flexible Execution**
   - `.\launch.ps1` - Start both (default)
   - `.\launch.ps1 --client-only` - Client only (current phase)
   - `.\launch.ps1 --server-only` - Server only (testing)
   - `.\launch.ps1 --no-install` - Skip dependency checks

### Implementation Plan

#### File: `launch.ps1`

```powershell
#Requires -Version 5.1

<#
.SYNOPSIS
    Launch Babocument development environment
.DESCRIPTION
    Starts server (FastAgent) and/or client (Next.js) with dependency management
.PARAMETER ClientOnly
    Start only the Next.js client
.PARAMETER ServerOnly
    Start only the FastAgent server
.PARAMETER NoInstall
    Skip dependency installation checks
.EXAMPLE
    .\launch.ps1
    Start both server and client
.EXAMPLE
    .\launch.ps1 -ClientOnly
    Start only the client (useful during Phase 0-3)
#>

param(
    [switch]$ClientOnly,
    [switch]$ServerOnly,
    [switch]$NoInstall
)

# Configuration
$ServerPath = Join-Path $PSScriptRoot "server"
$ClientPath = Join-Path $PSScriptRoot "client"
$ServerPort = 8000
$ClientPort = 3000

# Color output helpers
function Write-Status($message) { Write-Host "✓ $message" -ForegroundColor Green }
function Write-Info($message) { Write-Host "→ $message" -ForegroundColor Cyan }
function Write-Error($message) { Write-Host "✗ $message" -ForegroundColor Red }

# Track background jobs
$jobs = @()

# Cleanup function
function Stop-Services {
    Write-Info "Shutting down services..."
    $jobs | ForEach-Object { Stop-Process -Id $_.Id -ErrorAction SilentlyContinue }
    Write-Status "All services stopped"
}

# Register cleanup on Ctrl+C
Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action { Stop-Services }

try {
    Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║   Babocument Development Launcher      ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""

    # Determine what to start
    $startServer = -not $ClientOnly
    $startClient = -not $ServerOnly

    # Validate Server
    if ($startServer) {
        Write-Info "Validating server environment..."
        
        # Check if server directory exists and has content
        if (-not (Test-Path $ServerPath) -or -not (Get-ChildItem $ServerPath -ErrorAction SilentlyContinue)) {
            Write-Host "⚠ Server not yet implemented - skipping" -ForegroundColor Yellow
            $startServer = $false
        }
        else {
            # Check Python
            if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
                Write-Error "Python not found. Install Python 3.10+"
                exit 1
            }
            
            # Install dependencies
            if (-not $NoInstall) {
                Write-Info "Installing server dependencies..."
                Push-Location $ServerPath
                python -m pip install -r requirements.txt --quiet
                Pop-Location
                Write-Status "Server dependencies ready"
            }
        }
    }

    # Validate Client
    if ($startClient) {
        Write-Info "Validating client environment..."
        
        # Check Node.js
        if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
            Write-Error "Node.js not found. Install Node.js 18+"
            exit 1
        }
        
        # Install dependencies
        if (-not $NoInstall) {
            Write-Info "Installing client dependencies..."
            Push-Location $ClientPath
            npm install --silent
            Pop-Location
            Write-Status "Client dependencies ready"
        }
    }

    Write-Host ""
    Write-Host "Starting services..." -ForegroundColor Magenta
    Write-Host ""

    # Start Server
    if ($startServer) {
        Write-Info "Starting FastAgent server on http://localhost:$ServerPort"
        Push-Location $ServerPath
        $serverJob = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "main:app", "--reload", "--port", $ServerPort -PassThru -NoNewWindow
        $jobs += $serverJob
        Pop-Location
        Write-Status "Server started (PID: $($serverJob.Id))"
    }

    # Start Client
    if ($startClient) {
        Write-Info "Starting Next.js client on http://localhost:$ClientPort"
        Push-Location $ClientPath
        $clientJob = Start-Process -FilePath "npm" -ArgumentList "run", "dev" -PassThru -NoNewWindow
        $jobs += $clientJob
        Pop-Location
        Write-Status "Client started (PID: $($clientJob.Id))"
    }

    Write-Host ""
    Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║          Services Running              ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
    
    if ($startServer) {
        Write-Host "  Server: http://localhost:$ServerPort" -ForegroundColor Cyan
    }
    if ($startClient) {
        Write-Host "  Client: http://localhost:$ClientPort" -ForegroundColor Cyan
    }
    
    Write-Host ""
    Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow
    Write-Host ""

    # Wait for user interrupt
    while ($true) {
        Start-Sleep -Seconds 1
        
        # Check if processes are still running
        foreach ($job in $jobs) {
            if ($job.HasExited) {
                Write-Error "Service stopped unexpectedly (PID: $($job.Id))"
                exit 1
            }
        }
    }
}
catch {
    Write-Error "Launch failed: $_"
    Stop-Services
    exit 1
}
finally {
    Stop-Services
}
```

### Testing Checklist

- [ ] `.\launch.ps1 --client-only` starts Next.js successfully
- [ ] Client accessible at http://localhost:3000
- [ ] Ctrl+C stops client gracefully
- [ ] `.\launch.ps1 --no-install` skips npm install
- [ ] Script detects missing Node.js
- [ ] Script detects empty server directory (current state)
- [ ] Color output displays correctly in PowerShell

### Documentation Update

Update `README.md` with:

```markdown
## Quick Start

### Launch Development Environment

```powershell
# Start client (during Phase 0-3)
.\launch.ps1 --client-only

# Start both server and client (Phase 1+)
.\launch.ps1

# Skip dependency installation
.\launch.ps1 --no-install
```

### Manual Start (Alternative)

**Client:**
```powershell
cd client
npm install
npm run dev
```

**Server (when implemented):**
```powershell
cd server
pip install -r requirements.txt
python -m uvicorn main:app --reload
```
```

## Implementation Steps

1. **Create `launch.ps1`** in repository root
2. **Test with client-only mode** (current phase)
3. **Update README.md** with usage instructions
4. **Commit changes**
5. **Test with new contributors** to validate onboarding experience

## Future Enhancements

After server implementation (Phase 1+):
- [ ] Health check endpoints before marking "ready"
- [ ] Log file management
- [ ] Environment variable configuration
- [ ] Docker support (optional)
- [ ] Linux/macOS bash script equivalent

## Success Criteria

- ✅ Single command starts development environment
- ✅ Works on Windows PowerShell 5.1+
- ✅ Handles missing dependencies gracefully
- ✅ Graceful shutdown on Ctrl+C
- ✅ Clear console output with status indicators
- ✅ Reduces onboarding time from 10 minutes to 30 seconds

## Related Issues

- **Unblocks:** All development work (improves DX)
- **Related:** Issue #10 (Phase 1 Backend) - will benefit when server implemented
- **Dependencies:** None

---

**Status:** Ready for implementation
**Assignable:** Any contributor
**Time Investment:** 1-2 hours
**Impact:** High - affects all developers, all phases
