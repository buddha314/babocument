# Development Scripts Quick Reference

## Main Scripts

### `start-dev.ps1` ⭐ **Recommended**
**Launch both server and client with network access**

```powershell
.\start-dev.ps1
```

**What it does:**
- Starts backend server on port 8000 (network accessible)
- Starts frontend client on port 3000 (network accessible)
- Auto-detects your network IP
- Updates `.env.local` with correct API URL
- Opens both in separate terminal windows
- Displays all access URLs

**Access URLs shown:**
- `http://localhost:3000` - This computer
- `http://192.168.1.x:3000` - From other devices
- `http://localhost:8000/docs` - API documentation

**When to use:**
- Starting development session
- Testing from VR headset
- Accessing from phone/tablet
- Demonstrating to others on network

---

### `check-network.ps1`
**Check network configuration and service status**

```powershell
.\check-network.ps1
```

**What it does:**
- Shows your network IP addresses
- Checks if services are running
- Verifies firewall rules
- Checks Redis and Ollama status
- Displays access URLs

**When to use:**
- Services won't connect from other devices
- Need to find your network IP
- Troubleshooting network issues
- Verify everything is configured correctly

---

### `run-server.ps1`
**Start only the backend server**

```powershell
.\run-server.ps1
```

**Options:**
```powershell
.\run-server.ps1 -Port 8080  # Custom port
```

**When to use:**
- Backend development only
- Running server separately
- Custom port needed

---

## Individual Services

### Backend Only
```powershell
cd server
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Only
```powershell
cd client
npm run dev -- --port 3000 --hostname 0.0.0.0
```

---

## Common Tasks

### Full Development Session
```powershell
# 1. Start all services
.\start-dev.ps1

# 2. Wait ~10 seconds for startup
# 3. Open http://localhost:3000
# 4. Check "Backend API Test" panel shows "Connected"
```

### Testing from VR Headset
```powershell
# 1. Start services
.\start-dev.ps1

# 2. Note the network IP (e.g., 192.168.1.200)
# 3. On Quest: Open browser
# 4. Navigate to http://192.168.1.200:3000
# 5. Grant WebXR permissions
# 6. Enter VR mode
```

### Finding Your Network IP
```powershell
# Option 1: Check network script
.\check-network.ps1

# Option 2: PowerShell command
ipconfig | Select-String "IPv4"

# Option 3: Get primary WiFi IP
(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi").IPAddress
```

### Checking Service Status
```powershell
# Quick check
.\check-network.ps1

# Manual checks
Test-NetConnection localhost -Port 8000  # Server
Test-NetConnection localhost -Port 3000  # Client
```

### Firewall Setup (Run as Administrator)
```powershell
# Allow both ports
New-NetFirewallRule -DisplayName "Babocument Dev" `
    -Direction Inbound `
    -LocalPort 8000,3000 `
    -Protocol TCP `
    -Action Allow
```

---

## Port Reference

| Service | Port | Access |
|---------|------|--------|
| Backend Server | 8000 | http://localhost:8000 |
| API Documentation | 8000 | http://localhost:8000/docs |
| Frontend Client | 3000 | http://localhost:3000 |
| Redis (if running) | 6379 | localhost only |
| Ollama (if running) | 11434 | localhost only |

---

## Troubleshooting

### "Can't connect from other device"

1. **Check firewall:**
   ```powershell
   .\check-network.ps1
   ```

2. **Verify services running:**
   - Look for the terminal windows
   - Check for error messages

3. **Check same network:**
   - Both devices on same WiFi
   - Not using guest network

4. **Try URL with IP:**
   - Use `http://192.168.1.x:3000`
   - NOT `http://localhost:3000`

### "Backend API disconnected"

1. **Check .env.local:**
   ```powershell
   cat client\.env.local
   # Should show: NEXT_PUBLIC_API_URL=http://YOUR_IP:8000
   ```

2. **Restart with start-dev.ps1:**
   - It auto-updates .env.local with correct IP

3. **Verify CORS enabled:**
   - Server should allow all origins in dev mode

### Services won't start

1. **Check ports available:**
   ```powershell
   Test-NetConnection localhost -Port 8000
   Test-NetConnection localhost -Port 3000
   ```

2. **Kill existing processes:**
   ```powershell
   # Find processes using ports
   Get-Process -Name python | Stop-Process
   Get-Process -Name node | Stop-Process
   ```

3. **Check Python venv:**
   ```powershell
   cd server
   Test-Path venv\Scripts\Activate.ps1
   ```

---

## Development Workflow

### Standard Session
```
1. .\start-dev.ps1                  # Start services
2. Open http://localhost:3000       # Test locally
3. Make code changes                # Services auto-reload
4. Close terminal windows           # Stop services
```

### VR Development Session
```
1. .\start-dev.ps1                  # Start services
2. Note network IP from output      # e.g., 192.168.1.200
3. Put on VR headset               # Meta Quest
4. Open browser in VR               
5. Navigate to http://YOUR_IP:3000  
6. Develop and test in VR
```

### Multi-Device Testing
```
1. .\start-dev.ps1                  # On dev computer
2. .\check-network.ps1              # Get URLs
3. Test on desktop: localhost:3000
4. Test on phone: YOUR_IP:3000
5. Test on VR: YOUR_IP:3000
```

---

## Additional Resources

- **Network Setup Guide:** [NETWORK_ACCESS.md](NETWORK_ACCESS.md)
- **Project Status:** [HANDOFF_FINAL_2025-11-06.md](HANDOFF_FINAL_2025-11-06.md)
- **API Documentation:** http://localhost:8000/docs (when running)
- **Task List:** [specs/TASKS.md](specs/TASKS.md)
