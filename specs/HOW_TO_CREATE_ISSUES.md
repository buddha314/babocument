# How to Create GitHub Issues

## Option 1: Manual Creation (Recommended)

1. Go to https://github.com/buddha314/babocument/issues/new
2. Copy content from `GITHUB_ISSUES_TO_CREATE.md` for each issue
3. Paste into GitHub's issue form
4. Add labels as specified
5. Click "Submit new issue"

## Option 2: Using GitHub CLI

### Prerequisites
```powershell
# Install GitHub CLI
winget install GitHub.cli

# Authenticate
gh auth login
```

### Create Issues One by One

```powershell
# Navigate to repo
cd c:\Users\b\src\babocument

# Issue #40: Conversational Agent Interface
gh issue create `
    --title "Conversational Agent Interface - Primary User Interaction" `
    --label "agent,conversation,P0,phase-2,critical" `
    --body "See GITHUB_ISSUES_TO_CREATE.md for full description"

# Issue #41: Agent Avatar & Spatial Presence  
gh issue create `
    --title "Agent Avatar & Spatial Presence in VR Library" `
    --label "agent,vr,avatar,P0,phase-2,critical" `
    --body "See GITHUB_ISSUES_TO_CREATE.md for full description"

# Issue #42: Ambient Context UI
gh issue create `
    --title "Ambient Context UI - Spatial Results Display" `
    --label "ui,vr,spatial,P0,phase-2" `
    --body "See GITHUB_ISSUES_TO_CREATE.md for full description"

# Issue #43: Voice Interaction System
gh issue create `
    --title "Voice Interaction System for VR" `
    --label "voice,vr,accessibility,P1,phase-2" `
    --body "See GITHUB_ISSUES_TO_CREATE.md for full description"

# Issue #44: Workspace Management
gh issue create `
    --title "Workspace Management via Conversation" `
    --label "agent,workspace,conversation,P1,phase-3" `
    --body "See GITHUB_ISSUES_TO_CREATE.md for full description"

# Issue #45: Proactive Agent Behaviors
gh issue create `
    --title "Proactive Agent Behaviors and Suggestions" `
    --label "agent,ai,proactive,P2,phase-3" `
    --body "See GITHUB_ISSUES_TO_CREATE.md for full description"
```

## Option 3: Web Interface (Fastest for Multiple Issues)

1. Open: https://github.com/buddha314/babocument/issues
2. Keep `GITHUB_ISSUES_TO_CREATE.md` open in VS Code
3. For each issue:
   - Click "New issue"
   - Copy/paste title and description
   - Add labels (comma-separated)
   - Submit
   - Repeat

## Issues to Create

From `GITHUB_ISSUES_TO_CREATE.md`:

- [ ] Issue #40: Conversational Agent Interface ⭐⭐⭐ (P0)
- [ ] Issue #41: Agent Avatar & Spatial Presence ⭐⭐⭐ (P0)
- [ ] Issue #42: Ambient Context UI ⭐⭐ (P0)
- [ ] Issue #43: Voice Interaction System ⭐⭐ (P1)
- [ ] Issue #44: Workspace Management via Conversation ⭐ (P1)
- [ ] Issue #45: Proactive Agent Behaviors ⭐ (P2)
- [ ] Issue #30: Client API Infrastructure Setup (P0)
- [ ] Issue #32: Document API Integration (P0)
- [ ] Issue #33: Search Integration (P1)
- [ ] Issue #34: WebSocket Real-time Updates (P1)
- [ ] Issue #35: 3D Timeline Visualization (P2)
- [ ] Issue #36: Statistics Dashboard (P2)
- [ ] Issue #37: Repository Management UI (P2)
- [ ] Issue #38: Agent-Assisted Paper Discovery (P1)
- [ ] Issue #39: DICOM Medical Imaging Support (P2)

## After Creating Issues

Update `ISSUES.md` to reflect the new issues and their GitHub URLs.

## Notes

- The full content for each issue is in `GITHUB_ISSUES_TO_CREATE.md`
- Copy the entire section for each issue (including all tasks, acceptance criteria, etc.)
- Don't forget to add the labels specified for each issue
- Priority labels: P0 (critical), P1 (high), P2 (medium), P3 (low)
