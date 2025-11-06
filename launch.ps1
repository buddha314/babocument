#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Launch script for Babocument server and client
.DESCRIPTION
    Unified launch script to start both FastAgent server and Next.js client
    with proper dependency management and environment validation.
.PARAMETER ClientOnly
    Launch only the Next.js client (useful for Phase 0-3 work)
.PARAMETER ServerOnly
    Launch only the FastAgent server
.PARAMETER NoInstall
    Skip dependency installation checks
.PARAMETER ServerPort
    Port for the FastAgent server (default: 8000)
.PARAMETER ClientPort
    Port for the Next.js client (default: 3000)
.EXAMPLE
    .\launch.ps1
    Launch both server and client
.EXAMPLE
    .\launch.ps1 -ClientOnly
    Launch only the client (for current phase work)
.EXAMPLE
    .\launch.ps1 -NoInstall
    Launch without checking dependencies
#>

param(
    [switch]$ClientOnly,
    [switch]$ServerOnly,
    [switch]$NoInstall,
    [int]$ServerPort = 8000,
    [int]$ClientPort = 3000
)

# Script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ServerDir = Join-Path $ScriptDir "server"
$ClientDir = Join-Path $ScriptDir "client"

# Job tracking
$Jobs = [System.Collections.ArrayList]::new()

# Cleanup function
function Invoke-Cleanup {
    Write-Host "`n[INFO] Shutting down processes..." -ForegroundColor Cyan
    
    foreach ($Job in $Jobs) {
        if ($Job -and $Job.State -eq "Running") {
            Stop-Job $Job -ErrorAction SilentlyContinue
            Remove-Job $Job -ErrorAction SilentlyContinue
        }
    }
    
    Write-Host "[OK] Cleanup complete" -ForegroundColor Green
}

# Register cleanup on exit
$null = Register-EngineEvent PowerShell.Exiting -Action { Invoke-Cleanup }

# Handle Ctrl+C gracefully
try {
    $null = [Console]::TreatControlCAsInput = $false
} catch {
    # Ignore if console is not available
}

# Environment validation
Write-Host "[INFO] Validating environment..." -ForegroundColor Cyan

# Check Node.js
$NodeInstalled = Get-Command node -ErrorAction SilentlyContinue
if (-not $NodeInstalled) {
    Write-Host "[ERROR] Node.js is not installed. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}
$NodeVersion = node --version
Write-Host "[OK] Node.js $NodeVersion found" -ForegroundColor Green

# Check npm
$NpmInstalled = Get-Command npm -ErrorAction SilentlyContinue
if (-not $NpmInstalled) {
    Write-Host "[ERROR] npm is not installed. Please install npm." -ForegroundColor Red
    exit 1
}
$NpmVersion = npm --version
Write-Host "[OK] npm $NpmVersion found" -ForegroundColor Green

# Check Python (only if not client-only)
if (-not $ClientOnly) {
    $PythonInstalled = Get-Command python -ErrorAction SilentlyContinue
    if (-not $PythonInstalled) {
        Write-Host "[WARN] Python is not installed. Server launch will be skipped." -ForegroundColor Yellow
        Write-Host "[INFO] Install Python from https://www.python.org/ to enable server." -ForegroundColor Cyan
        $ClientOnly = $true
    } else {
        $PythonVersion = python --version
        Write-Host "[OK] $PythonVersion found" -ForegroundColor Green
        
        # Check pip
        $PipInstalled = Get-Command pip -ErrorAction SilentlyContinue
        if (-not $PipInstalled) {
            Write-Host "[WARN] pip is not installed. Server dependencies cannot be managed." -ForegroundColor Yellow
        } else {
            Write-Host "[OK] pip found" -ForegroundColor Green
        }
    }
}

# Check if server directory exists
$ServerExists = Test-Path $ServerDir
if (-not $ServerExists -and -not $ClientOnly) {
    Write-Host "[WARN] Server directory not found at $ServerDir" -ForegroundColor Yellow
    Write-Host "[INFO] Server is not yet implemented (Phase 1). Launching client only." -ForegroundColor Cyan
    $ClientOnly = $true
}

# Check if client directory exists
$ClientExists = Test-Path $ClientDir
if (-not $ClientExists) {
    Write-Host "[ERROR] Client directory not found at $ClientDir" -ForegroundColor Red
    exit 1
}

# Install dependencies
if (-not $NoInstall) {
    Write-Host "[INFO] Checking dependencies..." -ForegroundColor Cyan
    
    # Client dependencies
    if (-not $ServerOnly) {
        Write-Host "[INFO] Checking client dependencies..." -ForegroundColor Cyan
        Push-Location $ClientDir
        
        if (-not (Test-Path "node_modules")) {
            Write-Host "[WARN] Client node_modules not found. Installing..." -ForegroundColor Yellow
            npm install
            if ($LASTEXITCODE -ne 0) {
                Write-Host "[ERROR] Failed to install client dependencies" -ForegroundColor Red
                Pop-Location
                exit 1
            }
            Write-Host "[OK] Client dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "[OK] Client dependencies OK" -ForegroundColor Green
        }
        
        Pop-Location
    }
    
    # Server dependencies (if server exists and not client-only)
    if (-not $ClientOnly -and $ServerExists) {
        Write-Host "[INFO] Checking server dependencies..." -ForegroundColor Cyan
        Push-Location $ServerDir
        
        if (Test-Path "requirements.txt") {
            $VenvPath = Join-Path $ServerDir "venv"
            
            if (-not (Test-Path $VenvPath)) {
                Write-Host "[WARN] Python virtual environment not found. Creating..." -ForegroundColor Yellow
                python -m venv venv
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
                    Pop-Location
                    exit 1
                }
                Write-Host "[OK] Virtual environment created" -ForegroundColor Green
            }
            
            # Activate venv and install dependencies
            $ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
            if (Test-Path $ActivateScript) {
                & $ActivateScript
                
                Write-Host "[INFO] Installing Python dependencies..." -ForegroundColor Cyan
                pip install -r requirements.txt
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "[ERROR] Failed to install server dependencies" -ForegroundColor Red
                    deactivate
                    Pop-Location
                    exit 1
                }
                Write-Host "[OK] Server dependencies installed" -ForegroundColor Green
                deactivate
            }
        } else {
            Write-Host "[INFO] No requirements.txt found. Skipping server dependency installation." -ForegroundColor Cyan
        }
        
        Pop-Location
    }
} else {
    Write-Host "[INFO] Skipping dependency installation (--no-install flag)" -ForegroundColor Cyan
}

# Launch processes
Write-Host "[INFO] Starting services..." -ForegroundColor Cyan

# Launch server
if (-not $ClientOnly -and $ServerExists) {
    Write-Host "[INFO] Starting FastAgent server on port $ServerPort..." -ForegroundColor Cyan
    
    $ServerJob = Start-Job -ScriptBlock {
        param($ServerDir, $ServerPort)
        Set-Location $ServerDir
        
        # Activate venv if it exists
        $VenvActivate = Join-Path $ServerDir "venv\Scripts\Activate.ps1"
        if (Test-Path $VenvActivate) {
            & $VenvActivate
        }
        
        # Start FastAgent server (adjust command as needed when implemented)
        # For now, this is a placeholder
        python -m fastagent.app --port $ServerPort
        
    } -ArgumentList $ServerDir, $ServerPort
    
    $null = $Jobs.Add($ServerJob)
    Write-Host "[OK] Server job started (ID: $($ServerJob.Id))" -ForegroundColor Green
    Start-Sleep -Seconds 2
}

# Launch client
if (-not $ServerOnly) {
    Write-Host "[INFO] Starting Next.js client on port $ClientPort..." -ForegroundColor Cyan
    
    $ClientJob = Start-Job -ScriptBlock {
        param($ClientDir, $ClientPort)
        Set-Location $ClientDir
        
        # Set port via environment variable
        $env:PORT = $ClientPort
        
        # Start Next.js dev server
        npm run dev
        
    } -ArgumentList $ClientDir, $ClientPort
    
    $null = $Jobs.Add($ClientJob)
    Write-Host "[OK] Client job started (ID: $($ClientJob.Id))" -ForegroundColor Green
    Start-Sleep -Seconds 3
}

# Display status
Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "   Babocument Launch Status" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta

if (-not $ClientOnly -and $ServerExists) {
    Write-Host "[OK] Server: http://localhost:$ServerPort" -ForegroundColor Green
}

if (-not $ServerOnly) {
    Write-Host "[OK] Client: http://localhost:$ClientPort" -ForegroundColor Green
}

Write-Host "`nPress Ctrl+C to stop all processes" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Magenta

# Monitor jobs and keep script running
try {
    while ($true) {
        Start-Sleep -Seconds 1
        
        # Check if any job has failed
        foreach ($Job in $Jobs) {
            if ($Job.State -eq "Failed") {
                Write-Host "[ERROR] A service has failed. Check logs above." -ForegroundColor Red
                Invoke-Cleanup
                exit 1
            }
        }
    }
} catch {
    # Ctrl+C or other interruption
    Invoke-Cleanup
} finally {
    Invoke-Cleanup
}
