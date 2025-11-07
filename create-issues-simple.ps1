# Simple script to create critical GitHub issues
# Run this after: gh auth login

$repo = "buddha314/babocument"

Write-Host "Creating GitHub issues for $repo..." -ForegroundColor Green

# Issue 40
Write-Host "Creating Issue 40..." -ForegroundColor Cyan
gh issue create --repo $repo `
    --title "Conversational Agent Interface - Primary User Interaction" `
    --body-file ".\issue-templates\issue-40-body.md" `
    --label "agent,conversation,P0,phase-2,critical" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Created Issue 40" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create Issue 40 - it may already exist or there's an auth issue" -ForegroundColor Yellow
}

# Issue 41
Write-Host "Creating Issue 41..." -ForegroundColor Cyan
gh issue create --repo $repo `
    --title "Agent Avatar & Spatial Presence in VR Library" `
    --body-file ".\issue-templates\issue-41-body.md" `
    --label "agent,vr,avatar,P0,phase-2,critical" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Created Issue 41" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create Issue 41" -ForegroundColor Yellow
}

# Issue 42
Write-Host "Creating Issue 42..." -ForegroundColor Cyan
gh issue create --repo $repo `
    --title "Ambient Context UI - Spatial Results Display" `
    --body-file ".\issue-templates\issue-42-body.md" `
    --label "ui,vr,spatial,P0,phase-2" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Created Issue 42" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create Issue 42" -ForegroundColor Yellow
}

# Issue 43
Write-Host "Creating Issue 43..." -ForegroundColor Cyan
gh issue create --repo $repo `
    --title "Voice Interaction System for VR" `
    --body-file ".\issue-templates\issue-43-body.md" `
    --label "voice,vr,accessibility,P1,phase-2" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Created Issue 43" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create Issue 43" -ForegroundColor Yellow
}

# Issue 44
Write-Host "Creating Issue 44..." -ForegroundColor Cyan
gh issue create --repo $repo `
    --title "Workspace Management via Conversation" `
    --body-file ".\issue-templates\issue-44-body.md" `
    --label "agent,workspace,conversation,P1,phase-3" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Created Issue 44" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create Issue 44" -ForegroundColor Yellow
}

# Issue 45
Write-Host "Creating Issue 45..." -ForegroundColor Cyan
gh issue create --repo $repo `
    --title "Proactive Agent Behaviors and Suggestions" `
    --body-file ".\issue-templates\issue-45-body.md" `
    --label "agent,ai,proactive,P2,phase-3" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Created Issue 45" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create Issue 45" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Done! View issues at: https://github.com/$repo/issues" -ForegroundColor Cyan
Write-Host ""
Write-Host "Note: If you see errors, you may need to:" -ForegroundColor Yellow
Write-Host "  1. Install GitHub CLI: winget install GitHub.cli" -ForegroundColor Yellow
Write-Host "  2. Authenticate: gh auth login" -ForegroundColor Yellow
Write-Host "  3. Check if issues already exist" -ForegroundColor Yellow
