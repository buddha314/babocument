# PowerShell script to create GitHub issues for babocument
# Requires GitHub CLI (gh) to be installed and authenticated
# Install: winget install GitHub.cli
# Auth: gh auth login

$repo = "buddha314/babocument"

# Check if gh is installed
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI (gh) is not installed. Install with: winget install GitHub.cli"
    exit 1
}

# Check if authenticated
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Not authenticated with GitHub. Run: gh auth login"
    exit 1
}

Write-Host "Creating GitHub issues for $repo..." -ForegroundColor Green
Write-Host ""

# Issue #40: Conversational Agent Interface
Write-Host "Creating Issue #40: Conversational Agent Interface..." -ForegroundColor Cyan
$body40 = @"
## Summary

Implement conversational agent interface as THE primary way users interact with Babocument. User talks to agent (voice + text) like Claude Desktop, and agent performs research tasks on their behalf. This replaces traditional menu/form-based UI.

## Background

**Paradigm Shift:** User doesn't click through menus—they converse with an intelligent AI agent who understands research needs and proactively assists.

**User Experience:**
\`\`\`
User: "Show me recent papers about bioink formulation"
Agent: "I found 23 papers from 2023-2025. The most cited is 
        'Advanced Hydrogel Composites' by Kim et al. 
        Would you like me to show you the top 5 or filter by application?"
\`\`\`

## Tasks

### Backend: Agent Conversation Manager (8-12 hrs)
- [ ] Natural language query processing with LLM
- [ ] Intent classification (search, summarize, add, analyze, explain)
- [ ] Multi-turn conversation context and memory management
- [ ] Task planning and execution pipeline
- [ ] Response generation and streaming
- [ ] Session management (create, retrieve, persist)
- [ ] Error recovery and clarification questions

### Frontend: Chat Interface (8-12 hrs)
- [ ] Text input with conversation history
- [ ] Voice input integration (Web Speech API)
- [ ] Message bubbles (user and agent)
- [ ] Typing indicators for agent responses
- [ ] Response streaming display
- [ ] Voice output (Text-to-Speech)
- [ ] VR-optimized floating panel (billboard mode)
- [ ] Conversation history scrolling
- [ ] Quick action buttons (optional)

## API Endpoints

\`\`\`
POST   /api/v1/agent/chat              # Send message to agent
GET    /api/v1/agent/chat/{session_id} # Get conversation history
POST   /api/v1/agent/voice             # Voice input processing
WS     /ws/agent/{session_id}          # Real-time chat streaming
DELETE /api/v1/agent/chat/{session_id} # Clear conversation
\`\`\`

## Files to Create

### Backend
- \`server/app/agents/conversation_manager.py\`
- \`server/app/agents/intent_classifier.py\`
- \`server/app/api/routes/agent_chat.py\`
- \`server/app/models/conversation.py\`
- \`server/tests/test_conversation_manager.py\`

### Frontend
- \`client/src/components/agent/ChatInterface.tsx\`
- \`client/src/components/agent/MessageBubble.tsx\`
- \`client/src/components/agent/VoiceInput.tsx\`
- \`client/src/components/agent/TypingIndicator.tsx\`
- \`client/src/lib/api/agent.ts\`
- \`client/src/lib/hooks/useAgentChat.ts\`

## Acceptance Criteria

- [ ] User can send text messages to agent
- [ ] Agent responds with relevant, accurate information
- [ ] Multi-turn conversations maintain context
- [ ] Voice input works in VR (optional for MVP)
- [ ] Agent can search documents via natural language
- [ ] Agent can summarize documents
- [ ] Agent can perform workspace operations
- [ ] Conversation history persists in session
- [ ] WebSocket streaming shows responses in real-time
- [ ] VR UI is readable and accessible

## Dependencies

- Issue #10: Complete Agents (Research Agent with NLP)
- Issue #19: Event Bus (for agent task coordination) ✅
- LLM integration (Ollama/LiteLLM)

## Priority

**P0 (Critical)** - This is the PRIMARY interface, replaces traditional UI

## Estimated Time

**Total:** 16-24 hours
- Backend: 8-12 hours
- Frontend: 8-12 hours

## Documentation

See \`CLIENT_AGENT_FIRST_REDESIGN.md\` for complete paradigm analysis and implementation plan.
"@

gh issue create --repo $repo `
    --title "Conversational Agent Interface - Primary User Interaction" `
    --body $body40 `
    --label "agent,conversation,P0,phase-2,critical"

Write-Host "✓ Created Issue #40" -ForegroundColor Green
Start-Sleep -Seconds 2

# Issue #41: Agent Avatar & Spatial Presence
Write-Host "Creating Issue #41: Agent Avatar & Spatial Presence..." -ForegroundColor Cyan
$body41 = @"
## Summary

Create physical embodiment of the AI agent in the VR library environment. The agent appears as a 3D character (stylized humanoid or abstract orb) with animations and spatial audio, making it feel like a real research assistant.

## User Experience

Agent has physical presence in the library. When user enters VR:
- Agent greets them from a desk or central location
- Agent's voice comes from their position (spatial audio)
- Agent makes eye contact and gestures when talking
- Agent points to documents when referencing them
- Agent follows user or stays at station (configurable)

## Tasks

### Librarian Avatar (8-12 hrs)
- [ ] Choose avatar style (stylized humanoid or abstract orb)
- [ ] Create or source 3D model (low-poly, VR-optimized)
- [ ] Import model into BabylonJS
- [ ] Set up skeleton and rigging (if humanoid)
- [ ] Create idle animations (breathing, looking around)
- [ ] Create talking animations (lip sync or particle effects)
- [ ] Create pointing/gesture animations
- [ ] Implement eye gaze tracking (look at user)
- [ ] Position avatar in library scene
- [ ] Add proximity detection (greet when user approaches)

### Spatial Audio (4 hrs)
- [ ] Integrate Web Audio API with BabylonJS
- [ ] Create positional audio source at avatar
- [ ] Connect TTS output to spatial audio
- [ ] Test 3D audio perception in VR
- [ ] Add ambient library sounds (optional)
- [ ] Tune audio falloff and volume

## Files to Create

- \`client/src/components/babylon/LibrarianCharacter.tsx\`
- \`client/src/components/babylon/SpatialAudio.tsx\`
- \`client/src/lib/animations/AgentAnimations.ts\`
- \`client/assets/models/librarian.[glb|gltf]\`

## Acceptance Criteria

- [ ] Avatar appears in VR library scene
- [ ] Avatar has idle animation (breathing, subtle movement)
- [ ] Avatar responds to agent speech with animation
- [ ] Spatial audio works (voice comes from avatar position)
- [ ] User can see avatar from any angle
- [ ] Avatar performs at 60+ FPS in VR
- [ ] Avatar scales appropriately (human-sized or configurable)
- [ ] Eye contact tracking works (optional)

## Dependencies

- Issue #40: Conversational Agent Interface (needs TTS output)
- BabylonJS scene setup
- 3D model asset (create or source)

## Performance Requirements

- Triangles: <10,000 for avatar mesh
- Texture: <1024x1024 resolution
- Animations: <30 bones (if rigged)
- 60 FPS in VR headset

## Priority

**P0 (Critical)** - Core VR experience, makes agent tangible

## Estimated Time

**Total:** 12-16 hours
- Avatar setup: 8-12 hours
- Spatial audio: 4 hours
"@

gh issue create --repo $repo `
    --title "Agent Avatar & Spatial Presence in VR Library" `
    --body $body41 `
    --label "agent,vr,avatar,P0,phase-2,critical"

Write-Host "✓ Created Issue #41" -ForegroundColor Green
Start-Sleep -Seconds 2

# Issue #42: Ambient Context UI
Write-Host "Creating Issue #42: Ambient Context UI..." -ForegroundColor Cyan
$body42 = @"
## Summary

Results and context appear spatially in VR, not in traditional menus/panels. When agent finds documents, they appear as floating cards near the avatar. Timeline arranges documents chronologically in 3D space. User can grab, examine, and organize in space.

## User Experience

**No traditional UI panels.** Instead:
- Agent mentions a paper → Card appears floating nearby
- Agent finds 5 papers → 5 cards appear in arc around user
- User says "show timeline" → Documents arrange by year
- Agent highlights relevant papers → They glow/pulse
- User can grab cards, bring closer, dismiss with gesture

**Replaces:** DocumentList, SearchBar, traditional CRUD components

## Tasks

### Floating Result Cards (6-8 hrs)
- [ ] Create DocumentCard component (3D mesh in BabylonJS)
- [ ] Display title, authors, year on card face
- [ ] Hover interaction (shows summary)
- [ ] Grab interaction (user can move card)
- [ ] Dismiss gesture (swipe away)
- [ ] Stack/organize multiple cards
- [ ] Link to full document view
- [ ] Glow/highlight effect for relevance
- [ ] Scale animation on appear
- [ ] Position cards relative to avatar

### Spatial Timeline (4-6 hrs)
- [ ] Arrange documents by year in corridor
- [ ] Year labels (floating text)
- [ ] Walk-through navigation
- [ ] Agent-guided highlights
- [ ] Search result filtering (hide non-matches)
- [ ] Density visualization (more papers = tighter spacing)
- [ ] Jump-to-year functionality
- [ ] VR controller navigation

## Files to Create

- \`client/src/components/ambient/ResultCard.tsx\`
- \`client/src/components/ambient/Timeline.tsx\`
- \`client/src/components/ambient/CardStack.tsx\`
- \`client/src/lib/babylon/SpatialLayout.ts\`
- \`client/src/lib/interactions/GrabGesture.ts\`

## Acceptance Criteria

- [ ] Cards appear when agent finds results
- [ ] Cards are readable from 1-2 meters distance
- [ ] User can grab and move cards with VR controllers
- [ ] User can dismiss cards with gesture
- [ ] Timeline arranges documents by year
- [ ] Agent can highlight specific papers (glow effect)
- [ ] Performance: 60 FPS with 20+ cards visible
- [ ] Cards scale/position appropriately in VR
- [ ] No traditional scrolling menus needed

## Dependencies

- Issue #40: Conversational Agent Interface (triggers card display)
- Issue #41: Agent Avatar (cards appear near avatar)
- BabylonJS GUI system

## Priority

**P0 (Critical)** - Replaces traditional UI completely

## Estimated Time

**Total:** 10-14 hours
- Floating cards: 6-8 hours
- Spatial timeline: 4-6 hours
"@

gh issue create --repo $repo `
    --title "Ambient Context UI - Spatial Results Display" `
    --body $body42 `
    --label "ui,vr,spatial,P0,phase-2"

Write-Host "✓ Created Issue #42" -ForegroundColor Green
Start-Sleep -Seconds 2

# Issue #43: Voice Interaction System
Write-Host "Creating Issue #43: Voice Interaction System..." -ForegroundColor Cyan
$body43 = @"
## Summary

Implement hands-free voice interaction for VR environment. Users can talk to the agent without using keyboard/controllers. Essential for immersive VR experience.

## User Experience

- User enters VR
- Says "Hey Assistant" (wake word) OR holds controller button
- Speaks query: "Find papers about bioink"
- Agent voice responds from avatar position
- Conversation continues hands-free

## Tasks

### Voice Input (4-6 hrs)
- [ ] Integrate Web Speech API
- [ ] Implement wake word detection ("Hey Assistant")
- [ ] Push-to-talk button on VR controller
- [ ] Visual feedback (waveform on avatar or UI)
- [ ] Noise cancellation preprocessing
- [ ] Speech-to-text streaming
- [ ] Handle interruptions (user speaks during agent response)
- [ ] Fallback to text input if voice fails

### Voice Output (4-6 hrs)
- [ ] Choose TTS solution (Coqui TTS local or ElevenLabs cloud)
- [ ] Integrate TTS with agent responses
- [ ] Natural prosody and pacing
- [ ] Speed/pitch controls
- [ ] Queue management (don't overlap responses)
- [ ] Interrupt detection (stop talking when user speaks)
- [ ] Connect to spatial audio (Issue #41)
- [ ] Cache common responses

## Files to Create

- \`client/src/components/agent/VoiceInput.tsx\`
- \`client/src/components/agent/VoiceOutput.tsx\`
- \`client/src/lib/speech/SpeechToText.ts\`
- \`client/src/lib/speech/TextToSpeech.ts\`
- \`client/src/lib/speech/WakeWordDetector.ts\`

## Acceptance Criteria

- [ ] Push-to-talk works on VR controllers
- [ ] Wake word detection works (optional for MVP)
- [ ] Speech-to-text accuracy >85% in quiet environment
- [ ] TTS output sounds natural and clear
- [ ] Audio plays from avatar position (spatial)
- [ ] Visual feedback shows recording/processing state
- [ ] Can interrupt agent mid-response
- [ ] Fallback to text input if voice fails
- [ ] Works offline (if local TTS chosen)

## Dependencies

- Issue #40: Conversational Agent Interface
- Issue #41: Agent Avatar (for spatial audio)
- Web Speech API (browser support)

## Priority

**P1 (High)** - Essential for hands-free VR interaction

## Estimated Time

**Total:** 8-12 hours
- Voice input: 4-6 hours
- Voice output: 4-6 hours
"@

gh issue create --repo $repo `
    --title "Voice Interaction System for VR" `
    --body $body43 `
    --label "voice,vr,accessibility,P1,phase-2"

Write-Host "✓ Created Issue #43" -ForegroundColor Green
Start-Sleep -Seconds 2

# Issue #44: Workspace Management via Conversation
Write-Host "Creating Issue #44: Workspace Management via Conversation..." -ForegroundColor Cyan
$body44 = @"
## Summary

Users manage workspaces through conversational commands to the agent, not through traditional menus. Agent handles creation, organization, and navigation of research workspaces.

## Tasks

### Backend: Workspace Commands (4-5 hrs)
- [ ] Extend agent to handle workspace intents
- [ ] Parse workspace names from natural language
- [ ] Create workspace via agent command
- [ ] Move documents between workspaces
- [ ] List workspace contents
- [ ] Delete/archive workspaces
- [ ] Suggest workspace names based on content
- [ ] Auto-tag papers when adding to workspace

### Frontend: Spatial Workspace Visualization (2-3 hrs)
- [ ] Show workspaces as spatial "folders" or areas in VR
- [ ] Drag-and-drop papers to workspaces (secondary interaction)
- [ ] Visual indicator of current active workspace
- [ ] Workspace list accessible via voice or gesture
- [ ] Minimal UI (workspace labels in space)

## Files to Create

- \`server/app/agents/workspace_manager.py\`
- \`client/src/components/ambient/WorkspaceVisual.tsx\`
- \`client/src/lib/api/workspaces.ts\`

## Acceptance Criteria

- [ ] User can create workspaces via voice command
- [ ] User can add documents to workspaces conversationally
- [ ] User can query workspace contents via agent
- [ ] Agent suggests appropriate workspace names
- [ ] Workspaces visible in VR space (minimal visualization)
- [ ] Drag-and-drop works as secondary interaction
- [ ] Agent can auto-categorize papers into workspaces
- [ ] Multi-document operations work

## Dependencies

- Issue #40: Conversational Agent Interface
- Issue #42: Ambient Context UI (for spatial folders)

## Priority

**P1 (High)** - Essential workspace organization

## Estimated Time

**Total:** 6-8 hours
- Backend: 4-5 hours
- Frontend: 2-3 hours
"@

gh issue create --repo $repo `
    --title "Workspace Management via Conversation" `
    --body $body44 `
    --label "agent,workspace,conversation,P1,phase-3"

Write-Host "✓ Created Issue #44" -ForegroundColor Green
Start-Sleep -Seconds 2

# Issue #45: Proactive Agent Behaviors
Write-Host "Creating Issue #45: Proactive Agent Behaviors..." -ForegroundColor Cyan
$body45 = @"
## Summary

Agent doesn't just respond to queries—it anticipates user needs and proactively offers suggestions based on activity patterns, new content, and research context.

## Tasks

### Activity Tracking (4-6 hrs)
- [ ] Track user document viewing patterns
- [ ] Track search query history and frequency
- [ ] Track workspace activity
- [ ] Identify repeated queries or topics
- [ ] Detect when user is stuck (repeated searches, no saves)
- [ ] Track time spent on papers (engagement)

### Pattern Recognition (4-6 hrs)
- [ ] Identify research topics user is interested in
- [ ] Detect citation relationships
- [ ] Find contradictions or conflicting results
- [ ] Recognize when new content is relevant
- [ ] Identify gaps in user's corpus
- [ ] Suggest related papers proactively

### Notification System (2-3 hrs)
- [ ] Non-intrusive notification display (ambient)
- [ ] Agent verbal suggestions
- [ ] Notification prioritization (don't overwhelm)
- [ ] User preferences (notification frequency)
- [ ] "Remind me later" functionality
- [ ] Snooze/dismiss options

## Files to Create

- \`server/app/agents/activity_tracker.py\`
- \`server/app/agents/pattern_recognizer.py\`
- \`server/app/agents/proactive_suggester.py\`
- \`client/src/components/ambient/NotificationToast.tsx\`

## Acceptance Criteria

- [ ] Agent tracks user activity patterns
- [ ] Agent identifies recurring research topics
- [ ] Agent suggests new papers proactively
- [ ] Agent detects contradictions between papers
- [ ] Notifications are non-intrusive (ambient)
- [ ] User can dismiss or snooze suggestions
- [ ] Agent learns from user feedback
- [ ] Suggestions are relevant >70% of the time

## Dependencies

- Issue #40: Conversational Agent Interface
- Issue #10: Complete Agents (analytics capabilities)

## Priority

**P2 (Medium)** - Enhances intelligence, not essential for MVP

## Estimated Time

**Total:** 8-12 hours
"@

gh issue create --repo $repo `
    --title "Proactive Agent Behaviors and Suggestions" `
    --body $body45 `
    --label "agent,ai,proactive,P2,phase-3"

Write-Host "✓ Created Issue #45" -ForegroundColor Green
Start-Sleep -Seconds 2

# Continue with remaining issues...
Write-Host ""
Write-Host "Creating remaining issues..." -ForegroundColor Yellow
Write-Host ""

# Issue #46: 3D Chat Screen (already exists from earlier work)
Write-Host "Note: Issue #46 (3D Chat Screen) content is in GITHUB_ISSUE_46_VR_CHAT.md" -ForegroundColor Yellow
Write-Host "      You may want to create this one manually with the full content." -ForegroundColor Yellow
Write-Host ""

Write-Host "✓ All issues created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "View issues at: https://github.com/$repo/issues" -ForegroundColor Cyan
