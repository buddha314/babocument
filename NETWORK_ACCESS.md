# Network Access Setup Guide

This guide helps you access Babocument from other devices on your network (phones, VR headsets, other computers).

## Quick Start

```powershell
.\start-dev.ps1
```

This launches both server and client with network access enabled.

## Access URLs

**From this computer:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

**From other devices on your network:**
- Frontend: http://YOUR_IP:3000
- Backend: http://YOUR_IP:8000

The script will display your IP address when it starts.

## VR Headset Access (Meta Quest)

1. Run `.\start-dev.ps1` on your development computer
2. Note the network IP displayed (e.g., `192.168.1.100`)
3. On your Meta Quest:
   - Open the built-in browser
   - Navigate to `http://YOUR_IP:3000`
   - Allow WebXR permissions when prompted
   - Enter VR mode from the scene

## Firewall Configuration

### Windows Firewall

You may need to allow the ports through Windows Firewall:

```powershell
# Allow Server Port (8000)
New-NetFirewallRule -DisplayName "Babocument Server" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow

# Allow Client Port (3000)
New-NetFirewallRule -DisplayName "Babocument Client" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
```

Or use the GUI:
1. Open "Windows Defender Firewall with Advanced Security"
2. Click "Inbound Rules" → "New Rule"
3. Select "Port" → "TCP" → Enter "8000, 3000"
4. Allow the connection
5. Apply to all profiles
6. Name it "Babocument Development"

## Network Requirements

### Same Network
All devices must be on the same WiFi network or local network.

### IP Address Discovery

Find your computer's IP address:

```powershell
# PowerShell
ipconfig | Select-String "IPv4"

# Or
(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi").IPAddress
```

Common IP ranges:
- `192.168.1.x` - Most home routers
- `192.168.0.x` - Some routers
- `10.0.0.x` - Some routers

## Manual Configuration

If you need to run services manually:

### Backend Server (Network Accessible)
```powershell
cd server
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The `--host 0.0.0.0` makes the server accessible from other devices.

### Frontend Client (Network Accessible)
```powershell
cd client
npm run dev -- --port 3000 --hostname 0.0.0.0
```

The `--hostname 0.0.0.0` makes Next.js accessible from other devices.

### Update API URL
Edit `client/.env.local`:
```
NEXT_PUBLIC_API_URL=http://YOUR_IP:8000
```

Replace `YOUR_IP` with your actual network IP (e.g., `192.168.1.100`).

## Testing Network Access

### From Another Computer

1. Open a browser on another computer on the same network
2. Navigate to `http://YOUR_IP:3000`
3. You should see the Babocument 3D library interface
4. The "Backend API Test" panel should show "Connected" status

### From a Phone

1. Connect phone to same WiFi network
2. Open browser
3. Navigate to `http://YOUR_IP:3000`
4. Should see responsive version of the app

### From VR Headset (Meta Quest)

1. Ensure Quest is on same WiFi as development computer
2. Open Quest browser
3. Navigate to `http://YOUR_IP:3000`
4. Grant WebXR permissions
5. Click "Enter VR" button to experience in immersive mode

## Troubleshooting

### "Can't connect" from other devices

**Check 1: Firewall**
```powershell
# Test if ports are open
Test-NetConnection -ComputerName localhost -Port 8000
Test-NetConnection -ComputerName localhost -Port 3000
```

**Check 2: Services Running**
- Verify both terminal windows are still running
- Check for error messages in the terminal output

**Check 3: IP Address**
- Ensure you're using the correct IP address
- IP should start with `192.168.` or `10.0.`
- NOT `127.0.0.1` (localhost only)
- NOT `169.254.` (network error)

**Check 4: Same Network**
- All devices must be on same WiFi network
- Corporate/school networks may block device-to-device communication
- Guest WiFi networks often isolate devices

### "Backend API disconnected" in UI

**Check CORS settings:**
The server should already allow all origins in development. Check `server/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be "*" for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Check .env.local:**
Ensure `client/.env.local` has your network IP:
```
NEXT_PUBLIC_API_URL=http://192.168.1.100:8000
```

### VR Mode Not Working

1. **WebXR Support:** Ensure your browser supports WebXR
   - Meta Quest Browser: ✅ Supported
   - Chrome/Edge on desktop: ✅ Supported (with VR headset)
   - Safari: ❌ Not supported

2. **HTTPS Required:** Some VR features may require HTTPS
   - For local development, HTTP is usually fine
   - For production, use HTTPS

3. **Permissions:** Grant all requested permissions when prompted

## Production Deployment

For production deployment (not localhost):

1. **Use HTTPS** - Required for WebXR and security
2. **Configure CORS** - Restrict to specific domains
3. **Environment Variables** - Use production API URLs
4. **Build Client** - Run `npm run build` in client directory
5. **Process Manager** - Use PM2 or similar for server

## Security Notes

⚠️ **Development Only**

The network-accessible configuration is for **development only**:
- Firewall rules expose your ports to local network
- CORS allows all origins (`*`)
- No authentication required
- Debug mode enabled

**Never** deploy this configuration to production or public networks.

## Additional Resources

- [Next.js Network Access](https://nextjs.org/docs/api-reference/cli#development)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [WebXR Device API](https://developer.mozilla.org/en-US/docs/Web/API/WebXR_Device_API)
- [BabylonJS VR](https://doc.babylonjs.com/features/featuresDeepDive/webXR)
