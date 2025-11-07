# GitHub Issues - Ready to Create

**⚠️ PARADIGM SHIFT:** Agent-first conversational interface (like Claude Desktop)  
**Updated:** 2025-11-06 - Added Issues #40-#45 for agent-first model  
**See:** CLIENT_AGENT_FIRST_REDESIGN.md for complete analysis

These are the GitHub issues ready to be created. Copy each section into GitHub's "New Issue" form.

---

## Issue #40: Conversational Agent Interface ⭐⭐⭐

**Labels:** `agent`, `conversation`, `P0`, `phase-2`, `critical`

**Title:** Conversational Agent Interface - Primary User Interaction

**Description:**

## Summary

Implement conversational agent interface as THE primary way users interact with Babocument. User talks to agent (voice + text) like Claude Desktop, and agent performs research tasks on their behalf. This replaces traditional menu/form-based UI.

## Background

**Paradigm Shift:** User doesn't click through menus—they converse with an intelligent AI agent who understands research needs and proactively assists.

**User Experience:**
```
User: "Show me recent papers about bioink formulation"
Agent: "I found 23 papers from 2023-2025. The most cited is 
        'Advanced Hydrogel Composites' by Kim et al. 
        Would you like me to show you the top 5 or filter by application?"
```

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

```
POST   /api/v1/agent/chat              # Send message to agent
GET    /api/v1/agent/chat/{session_id} # Get conversation history
POST   /api/v1/agent/voice             # Voice input processing
WS     /ws/agent/{session_id}          # Real-time chat streaming
DELETE /api/v1/agent/chat/{session_id} # Clear conversation
```

## Files to Create

### Backend
- `server/app/agents/conversation_manager.py`
- `server/app/agents/intent_classifier.py`
- `server/app/api/routes/agent_chat.py`
- `server/app/models/conversation.py`
- `server/tests/test_conversation_manager.py`

### Frontend
- `client/src/components/agent/ChatInterface.tsx`
- `client/src/components/agent/MessageBubble.tsx`
- `client/src/components/agent/VoiceInput.tsx`
- `client/src/components/agent/TypingIndicator.tsx`
- `client/src/lib/api/agent.ts`
- `client/src/lib/hooks/useAgentChat.ts`

## Example Interactions

**Search:**
```
User: "Find papers about bioink formulation published after 2020"
Agent: "I found 23 papers on bioink formulation from 2021-2025. 
        The most cited is 'Advanced Hydrogel Composites' by Kim et al. 
        Would you like me to show you the top 5?"
```

**Summarization:**
```
User: "Summarize the top 3"
Agent: [Generates summaries] "Paper 1 introduces a novel alginate blend..."
```

**Workspace Management:**
```
User: "Add that Kim paper to my workspace"
Agent: "Done! I've added 'Advanced Hydrogel Composites' to your current workspace."
```

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

## Success Metrics

- Conversation success rate >80% (agent understands query)
- Average response time <2 seconds
- Multi-turn conversation depth (avg 3-5 turns)
- User satisfaction "helpful" rating >4/5

## Priority

**P0 (Critical)** - This is the PRIMARY interface, replaces traditional UI

## Estimated Time

**Total:** 16-24 hours
- Backend: 8-12 hours
- Frontend: 8-12 hours

## Related Issues

- Issue #41: Agent Avatar & Spatial Presence
- Issue #43: Voice Interaction System
- Issue #38: Agent-Assisted Paper Discovery

## Documentation

See `CLIENT_AGENT_FIRST_REDESIGN.md` for complete paradigm analysis and implementation plan.

---

## Issue #41: Agent Avatar & Spatial Presence ⭐⭐⭐

**Labels:** `agent`, `vr`, `avatar`, `P0`, `phase-2`, `critical`

**Title:** Agent Avatar & Spatial Presence in VR Library

**Description:**

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

## Technical Details

**BabylonJS Components:**
- AnimationGroups for state machine
- TransformNode for avatar root
- Mesh or particle system for visual
- Sound with spatialSound=true for audio
- Ray casting for eye contact

**Avatar Design Options:**
- A) Realistic human (high uncanny valley risk)
- B) Stylized humanoid (Pixar-style, recommended)
- C) Abstract orb/presence (easiest, lowest risk)
- D) Holographic effect (sci-fi aesthetic)

**Recommended:** Option B or C

## Files to Create

- `client/src/components/babylon/LibrarianCharacter.tsx`
- `client/src/components/babylon/SpatialAudio.tsx`
- `client/src/lib/animations/AgentAnimations.ts`
- `client/assets/models/librarian.[glb|gltf]`

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

## Related Issues

- Issue #40: Conversational Agent Interface
- Issue #43: Voice Interaction System

---

## Issue #42: Ambient Context UI ⭐⭐

**Labels:** `ui`, `vr`, `spatial`, `P0`, `phase-2`

**Title:** Ambient Context UI - Spatial Results Display

**Description:**

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

## Technical Details

**Card Rendering:**
- Plane mesh with GUI Texture
- AdvancedDynamicTexture for text
- Billboard mode (always faces user)
- Distance-based LOD

**Interaction:**
- WebXR controller ray casting
- Hand tracking gestures
- Proximity triggers

## Files to Create

- `client/src/components/ambient/ResultCard.tsx`
- `client/src/components/ambient/Timeline.tsx`
- `client/src/components/ambient/CardStack.tsx`
- `client/src/lib/babylon/SpatialLayout.ts`
- `client/src/lib/interactions/GrabGesture.ts`

## Example Interactions

```
User: "Show me papers about bioink"
Agent: "I found 23 papers. Here are the top 5."
[5 cards appear in arc in front of user]

User: [Grabs card with controller]
Agent: "This paper by Kim et al introduces a novel alginate blend..."

User: "Show timeline"
[Cards rearrange chronologically along corridor]
Agent: "I've arranged them by year. Most recent papers are ahead."
```

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

## Performance Requirements

- Maximum 50 cards rendered simultaneously
- Billboard shader for efficient orientation
- Texture atlasing for card content
- Culling for off-screen cards

## Priority

**P0 (Critical)** - Replaces traditional UI completely

## Estimated Time

**Total:** 10-14 hours
- Floating cards: 6-8 hours
- Spatial timeline: 4-6 hours

## Related Issues

- Issue #35: 3D Timeline Visualization (builds on this)
- Issue #38: Agent-Assisted Paper Discovery

---

## Issue #43: Voice Interaction System ⭐⭐

**Labels:** `voice`, `vr`, `accessibility`, `P1`, `phase-2`

**Title:** Voice Interaction System for VR

**Description:**

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

## Technical Details

**Voice Input Options:**
- Web Speech API (browser native, free, decent accuracy)
- Azure Speech Services (best accuracy, cloud-based)
- Whisper (local, very good, requires GPU)

**Recommended:** Start with Web Speech API, upgrade to Azure if needed

**Voice Output Options:**
- Browser TTS (free, robotic)
- Coqui TTS (local, free, good quality) **Recommended for MVP**
- ElevenLabs (cloud, best quality, $29/mo) **Recommended for production**
- Azure Cognitive Services (cloud, good, pay-per-use)

**VR Controller Mapping:**
- Quest: Grip button = push-to-talk
- Index: System button long-press
- Generic: Configurable in settings

## Files to Create

- `client/src/components/agent/VoiceInput.tsx`
- `client/src/components/agent/VoiceOutput.tsx`
- `client/src/lib/speech/SpeechToText.ts`
- `client/src/lib/speech/TextToSpeech.ts`
- `client/src/lib/speech/WakeWordDetector.ts`

## Example Flow

```
1. User presses VR controller grip button
2. Visual indicator shows recording (waveform)
3. User: "Show me papers about bioink"
4. Speech-to-text converts to text
5. Sent to agent API (Issue #40)
6. Agent response streamed back
7. TTS converts response to audio
8. Audio plays from avatar position (spatial)
9. User sees avatar "talking" animation
```

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

## Performance Requirements

- Speech-to-text latency <1 second
- TTS synthesis latency <500ms
- No dropped audio frames
- Smooth integration with VR rendering (60 FPS maintained)

## Priority

**P1 (High)** - Essential for hands-free VR interaction

## Estimated Time

**Total:** 8-12 hours
- Voice input: 4-6 hours
- Voice output: 4-6 hours

## Related Issues

- Issue #40: Conversational Agent Interface
- Issue #41: Agent Avatar & Spatial Presence

---

## Issue #44: Workspace Management via Conversation ⭐

**Labels:** `agent`, `workspace`, `conversation`, `P1`, `phase-3`

**Title:** Workspace Management via Conversation

**Description:**

## Summary

Users manage workspaces through conversational commands to the agent, not through traditional menus. Agent handles creation, organization, and navigation of research workspaces.

## User Experience

**No workspace management UI.** Instead:
```
User: "Create a new workspace for cancer immunotherapy research"
Agent: "Done! I've created 'Cancer Immunotherapy 2025'. 
        Would you like me to search for relevant papers?"

User: "Move these papers to my bioprinting workspace"
Agent: "I've moved 3 papers to 'Bioprinting Research'. 
        That workspace now has 47 papers."

User: "Show me what's in my Q4 2024 workspace"
Agent: "Your Q4 2024 workspace has 23 papers. 
        Top topics are: gene editing, CAR-T therapy, and biomanufacturing."
```

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

## API Enhancements

```
POST   /api/v1/workspaces                    # Create workspace
GET    /api/v1/workspaces                    # List workspaces
PUT    /api/v1/workspaces/{id}/documents     # Add documents
DELETE /api/v1/workspaces/{id}               # Delete workspace
```

**Agent understands:**
- "Create workspace [name]"
- "Add [document] to [workspace]"
- "Show me [workspace]"
- "Move [these/this] to [workspace]"
- "What's in [workspace]?"
- "Archive [workspace]"

## Files to Create

- `server/app/agents/workspace_manager.py`
- `client/src/components/ambient/WorkspaceVisual.tsx`
- `client/src/lib/api/workspaces.ts`

## Example Interactions

```
User: "I want to organize my papers by topic"
Agent: "I can create workspaces for you. What topics are you working on?"

User: "Cancer research and bioprinting"
Agent: "I've created 'Cancer Research' and 'Bioprinting' workspaces. 
        Would you like me to categorize your existing papers?"

User: "Yes"
Agent: "I've organized 47 papers into these workspaces based on their content. 
        Cancer Research has 23 papers, Bioprinting has 24."
```

## Acceptance Criteria

- [ ] User can create workspaces via voice command
- [ ] User can add documents to workspaces conversationally
- [ ] User can query workspace contents via agent
- [ ] Agent suggests appropriate workspace names
- [ ] Workspaces visible in VR space (minimal visualization)
- [ ] Drag-and-drop works as secondary interaction
- [ ] Agent can auto-categorize papers into workspaces
- [ ] Multi-document operations work ("move these 5 papers")

## Dependencies

- Issue #40: Conversational Agent Interface
- Issue #42: Ambient Context UI (for spatial folders)

## Priority

**P1 (High)** - Essential workspace organization

## Estimated Time

**Total:** 6-8 hours
- Backend: 4-5 hours
- Frontend: 2-3 hours

## Related Issues

- Issue #40: Conversational Agent Interface
- Issue #38: Agent-Assisted Paper Discovery

---

## Issue #45: Proactive Agent Behaviors ⭐

**Labels:** `agent`, `ai`, `proactive`, `P2`, `phase-3`

**Title:** Proactive Agent Behaviors and Suggestions

**Description:**

## Summary

Agent doesn't just respond to queries—it anticipates user needs and proactively offers suggestions based on activity patterns, new content, and research context.

## User Experience

**Agent notices patterns and proactively assists:**

```
[User has been reading CAR-T therapy papers for 30 minutes]
Agent: "I noticed you've been reading about CAR-T therapy. 
        There are 3 new papers published this week. 
        Would you like me to show them?"

[User searching for a topic repeatedly]
Agent: "You've searched for 'bioink formulation' several times. 
        Would you like me to create a workspace and monitor 
        for new papers on this topic?"

[Agent detects contradiction]
Agent: "This paper by Smith et al contradicts your earlier 
        findings from the Kim paper. The cell viability 
        results differ by 30%. Shall I explain the differences?"

[New related content]
Agent: "I found 5 new papers that cite the papers you saved 
        last week. Would you like to review them?"
```

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

## Technical Details

**Pattern Recognition:**
- Vector similarity between viewed papers
- Keyword frequency analysis
- Citation graph traversal
- Temporal patterns (user active times)
- Engagement metrics (time on paper)

**Notification Triggers:**
- New papers matching topics (daily check)
- Repeated searches (after 3 searches for same topic)
- Contradictions detected (semantic analysis)
- Citing papers found (citation monitoring)
- User appears stuck (10 min on same query)

## Files to Create

- `server/app/agents/activity_tracker.py`
- `server/app/agents/pattern_recognizer.py`
- `server/app/agents/proactive_suggester.py`
- `client/src/components/ambient/NotificationToast.tsx`

## Example Proactive Behaviors

**1. New Content Alert:**
```
Agent: "Good morning! While you were away, 12 new papers 
        were added to your monitored topics. 3 are highly 
        relevant to your cancer research."
```

**2. Research Gap Identification:**
```
Agent: "I notice your bioprinting workspace doesn't have 
        papers about regulatory considerations. Would you 
        like me to find some?"
```

**3. Citation Network:**
```
Agent: "These 5 papers you saved all cite the same foundational 
        work by Johnson et al. Would you like me to show you 
        that paper?"
```

**4. Trend Detection:**
```
Agent: "I've noticed increasing mentions of 'CRISPR base editing' 
        in papers from the last 3 months. This seems to be an 
        emerging trend in your field."
```

## Acceptance Criteria

- [ ] Agent tracks user activity patterns
- [ ] Agent identifies recurring research topics
- [ ] Agent suggests new papers proactively
- [ ] Agent detects contradictions between papers
- [ ] Notifications are non-intrusive (ambient)
- [ ] User can dismiss or snooze suggestions
- [ ] Agent learns from user feedback (accept/reject suggestions)
- [ ] Suggestions are relevant >70% of the time
- [ ] Agent doesn't overwhelm with too many notifications

## Dependencies

- Issue #40: Conversational Agent Interface
- Issue #10: Complete Agents (analytics capabilities)
- User activity logging

## Privacy Considerations

- User activity tracked locally or with consent
- Option to disable tracking
- Clear data retention policy
- Anonymized analytics

## Priority

**P2 (Medium)** - Enhances intelligence, not essential for MVP

## Estimated Time

**Total:** 8-12 hours
- Activity tracking: 3-4 hours
- Pattern recognition: 4-6 hours
- Notification system: 2-3 hours

## Related Issues

- Issue #40: Conversational Agent Interface
- Issue #38: Agent-Assisted Paper Discovery

---

## Issue #30: Client API Infrastructure Setup

**Labels:** `client`, `api`, `P0`, `phase-2`

**Title:** Client API Infrastructure Setup

**Description:**

## Summary

Set up API client infrastructure for the BabylonJS/Next.js client to communicate with the FastAPI server. This is the foundation for all client-server communication.

## Background

The server exposes 17 REST API endpoints for document management, search, and statistics. The client needs a type-safe, robust API client to consume these endpoints.

**Server API:** http://localhost:8000/docs (OpenAPI documentation)

## Tasks

- [ ] Install dependencies (axios, @tanstack/react-query, zod)
- [ ] Create base API client with interceptors
- [ ] Define TypeScript types (from OpenAPI or manual)
- [ ] Set up React Query provider
- [ ] Configure environment variables
- [ ] Test server connectivity

## Files to Create

- `client/src/lib/api/client.ts`
- `client/src/lib/api/types.ts`
- `client/src/app/providers.tsx`
- `client/.env.local`

## Acceptance Criteria

- [ ] API client can successfully connect to server
- [ ] Types are defined for all server responses
- [ ] React Query is set up and working
- [ ] Environment variables are configured
- [ ] Error handling works
- [ ] CORS allows client requests

## Dependencies

None - can start immediately

## Estimated Time

4-6 hours

## Documentation

- See `CLIENT_API_INTEGRATION_PLAN.md` for full architecture
- See `HANDOFF_2025-11-06_CLIENT_API.md` for implementation details

---

## Issue #32: Document API Integration (Client)

**Labels:** `client`, `api`, `documents`, `P0`, `phase-2`

**Title:** Document API Integration (Client)

**Description:**

## Summary

Implement document management features in the BabylonJS client using the server's REST API. This includes listing, viewing, uploading, deleting, and searching documents.

## Tasks

- [ ] Create `lib/api/documents.ts` with all document API methods
- [ ] Create `lib/hooks/useDocuments.ts` with React Query hooks
- [ ] Build DocumentList component
- [ ] Build DocumentViewer component
- [ ] Build DocumentUploader component
- [ ] Test all CRUD operations

## Files to Create

- `client/src/lib/api/documents.ts`
- `client/src/lib/hooks/useDocuments.ts`
- `client/src/components/documents/DocumentList.tsx`
- `client/src/components/documents/DocumentViewer.tsx`
- `client/src/components/documents/DocumentUploader.tsx`

## Acceptance Criteria

- [ ] Can list all documents with pagination
- [ ] Can view document details
- [ ] Can upload new PDF documents
- [ ] Can delete documents
- [ ] Can search documents (semantic & keyword)
- [ ] Can generate AI summaries
- [ ] Loading states show during API calls
- [ ] Errors are handled gracefully

## Dependencies

- **Depends on:** Issue #30 (Client API Infrastructure)

## Estimated Time

8-12 hours

## Documentation

- Server API: http://localhost:8000/docs
- See `CLIENT_API_INTEGRATION_PLAN.md` for code examples

---

## Issue #33: Search Integration (Client)

**Labels:** `client`, `search`, `P1`, `phase-2`

**Title:** Search Integration (Client)

**Description:**

## Summary

Implement semantic and keyword search functionality in the BabylonJS client with UI components for search input, results display, and filtering.

## Tasks

- [ ] Create `lib/hooks/useSearch.ts` with debounced search
- [ ] Build SearchBar component
- [ ] Build SearchResults component
- [ ] Build SearchFilters component (year, source)
- [ ] Integrate with 3D scene (highlight results - optional)

## Files to Create

- `client/src/lib/hooks/useSearch.ts`
- `client/src/components/search/SearchBar.tsx`
- `client/src/components/search/SearchResults.tsx`
- `client/src/components/search/SearchFilters.tsx`

## Acceptance Criteria

- [ ] Can search documents using text input
- [ ] Can toggle between semantic and keyword search
- [ ] Search is debounced
- [ ] Results show relevance scores
- [ ] Can filter by year and source
- [ ] Loading states work
- [ ] Error handling works

## Dependencies

- **Depends on:** Issue #32 (Document API Integration)

## Estimated Time

6-8 hours

---

## Issue #34: WebSocket Real-time Updates (Client)

**Labels:** `client`, `websocket`, `realtime`, `P1`, `phase-2`

**Title:** WebSocket Real-time Updates (Client)

**Description:**

## Summary

Implement WebSocket connection in the BabylonJS client to receive real-time updates from the server for agent tasks, document processing, and search completion events.

## Tasks

- [ ] Create `lib/api/websocket.ts` with auto-reconnect
- [ ] Create `lib/hooks/useWebSocket.ts`
- [ ] Create Notification component
- [ ] Integrate with DocumentUploader (show upload progress)
- [ ] Subscribe to all event types
- [ ] Test event flow

## Files to Create

- `client/src/lib/api/websocket.ts`
- `client/src/lib/hooks/useWebSocket.ts`
- `client/src/components/common/Notification.tsx`
- `client/src/components/agents/AgentActivity.tsx`

## Acceptance Criteria

- [ ] WebSocket connects on page load
- [ ] Auto-reconnects on disconnect
- [ ] Receives and parses events correctly
- [ ] UI updates in real-time
- [ ] Notifications show for events
- [ ] Connection status visible
- [ ] Proper cleanup on unmount

## Dependencies

- **Depends on:** Issue #30 (Client API Infrastructure)
- **Depends on:** Server Issue #21 (WebSocket Handler - must be implemented first)

## Estimated Time

4-6 hours

**Note:** Server Issue #21 must be completed before this can be fully tested.

---

## Issue #38: Agent-Assisted Paper Discovery

**Labels:** `agent`, `search`, `nlp`, `P1`, `feature`

**Title:** Agent-Assisted Paper Discovery

**Description:**

## User Story

> **As Beabadoo**, I want to ask the agent to find scientific papers for me using natural language, so I can quickly discover relevant research without manually searching through databases.

## Summary

Enable natural language queries for finding scientific papers using the Research Agent with LLM capabilities. Users can ask questions like "Find papers about bioink formulation" and receive ranked, relevant results with AI-generated explanations.

## Example Queries

- "Find papers about bioink formulation for 3D printing"
- "Show me recent advances in CRISPR gene editing"
- "Papers by George Church about synthetic biology"
- "Compare different methods for tissue scaffolding"
- "What's new in biomanufacturing since 2023?"

## Tasks

**Backend (8-12 hours):**
- [ ] Enhance Research Agent with NLP query processing
- [ ] Add query intent extraction (keywords, authors, time ranges)
- [ ] Create `/api/v1/agents/search` endpoint
- [ ] Generate AI explanations for results ("why this matches")
- [ ] Integrate with existing semantic search
- [ ] Add result ranking algorithm

**Frontend (6-8 hours):**
- [ ] Create `lib/api/agents.ts` API methods
- [ ] Create `lib/hooks/useAgentSearch.ts` hook
- [ ] Build AgentSearchBar component
- [ ] Build AgentSearchResults component with explanations
- [ ] Add agent avatar with "thinking" animation
- [ ] Support voice input in VR mode

## Acceptance Criteria

- [ ] Can input natural language queries
- [ ] Agent processes query and returns ranked results
- [ ] Results show relevance scores and AI summaries
- [ ] Each result has "why this matches" explanation
- [ ] Can view full paper or add to workspace
- [ ] Voice input works in VR mode
- [ ] Real-time progress updates via WebSocket

## Dependencies

- **Depends on:** Issue #10 (Complete Agents)
- **Depends on:** Client Issue #32 (Document API)
- **Related to:** Issue #5 (MCP Integration - for external sources)

## Estimated Time

14-20 hours (Backend: 8-12, Frontend: 6-8)

## Documentation

- See `specs/VISUALIZATION_REQUIREMENTS.md` - Section 3
- See `.github/ISSUE_TEMPLATE/agent-paper-discovery.md` for full details

---

## Issue #35: 3D Timeline Visualization (Client)

**Labels:** `client`, `babylonjs`, `3d`, `visualization`, `P2`, `phase-3`

**Title:** 3D Timeline Visualization (Client)

**Description:**

## Summary

Create an immersive 3D timeline corridor in BabylonJS that visualizes documents from the API sorted by year, with interactive selection and search result highlighting.

## Tasks

- [ ] Create Timeline3D component
- [ ] Generate document meshes from API data
- [ ] Position documents by year
- [ ] Add interactive selection (click/hover)
- [ ] Integrate search result highlighting
- [ ] Add VR/XR controller support
- [ ] Optimize performance (60+ FPS)

## Files to Create

- `client/src/components/babylon/Timeline3D.tsx`
- `client/src/components/babylon/DocumentMesh.tsx`
- `client/src/components/babylon/YearPartition.tsx`
- `client/src/components/babylon/utils/meshGeneration.ts`
- `client/src/components/babylon/utils/positioning.ts`

## Acceptance Criteria

- [ ] Documents load from API and render in 3D
- [ ] Documents sorted by year along timeline
- [ ] Can navigate through timeline
- [ ] Can select documents
- [ ] Search results are highlighted
- [ ] Works in desktop and VR modes
- [ ] Maintains 60+ FPS with 100+ documents

## Dependencies

- **Depends on:** Issue #32 (Document API Integration)
- **Related to:** Issue #33 (Search - for highlighting)

## Estimated Time

12-16 hours

---

## Issue #36: Statistics Dashboard (Client)

**Labels:** `client`, `stats`, `dashboard`, `P2`, `phase-3`

**Title:** Statistics Dashboard (Client)

**Description:**

## Summary

Create statistics dashboard showing system metrics and document analytics.

## Tasks

- [ ] Create `lib/api/stats.ts` API methods
- [ ] Create `lib/hooks/useStats.ts`
- [ ] Build StatsPanel component
- [ ] Build charts (documents by year, source trends)
- [ ] Add real-time updates via WebSocket

## Files to Create

- `client/src/lib/api/stats.ts`
- `client/src/lib/hooks/useStats.ts`
- `client/src/components/stats/StatsPanel.tsx`
- `client/src/components/stats/StatsChart.tsx`

## Acceptance Criteria

- [ ] Shows system statistics
- [ ] Shows document analytics
- [ ] Charts are interactive
- [ ] Real-time updates work

## Dependencies

- **Depends on:** Issue #30 (Client API Infrastructure)

## Estimated Time

6-8 hours

---

## Issue #37: Repository Management UI (Client)

**Labels:** `client`, `repository`, `admin`, `P2`, `phase-3`

**Title:** Repository Management UI (Client)

**Description:**

## Summary

Create UI for managing document repositories and MCP server connections.

## Tasks

- [ ] Create `lib/api/repositories.ts` API methods
- [ ] Create `lib/hooks/useRepositories.ts`
- [ ] Build RepositoryManager component
- [ ] Show connection status and health
- [ ] Add sync functionality

## Files to Create

- `client/src/lib/api/repositories.ts`
- `client/src/lib/hooks/useRepositories.ts`
- `client/src/components/repositories/RepositoryManager.tsx`
- `client/src/components/repositories/RepositoryCard.tsx`

## Acceptance Criteria

- [ ] Shows all repositories
- [ ] Shows connection status
- [ ] Can trigger sync
- [ ] Shows document counts

## Dependencies

- **Depends on:** Issue #30 (Client API Infrastructure)

## Estimated Time

4-6 hours

---

## Issue #39: DICOM Medical Imaging Support

**Labels:** `client`, `backend`, `feature`, `medical-imaging`, `P2`, `phase-3`

**Title:** DICOM Medical Imaging Support

**Description:**

## Summary

Enable viewing DICOM medical imaging files and searching open-source medical imaging repositories like The Cancer Imaging Archive (TCIA). This allows Beabadoo to analyze diagnostic images alongside scientific papers for comprehensive medical research.

## User Story

> **As Beabadoo**, I want to view DICOM medical imaging files in 3D/VR and ask agents to search medical imaging repositories, so I can analyze diagnostic images alongside scientific papers.

## Example Use Cases

### Viewing DICOM Files
- "Load this CT scan and show it in 3D"
- "Display this MRI series with volume rendering"
- "Show me slice-by-slice view of this brain scan"
- "Compare these two X-rays side by side"

### Searching Medical Imaging Repositories
- "Find CT scans of lung cancer patients"
- "Show me brain MRIs with glioblastoma"
- "Search for breast cancer mammography images"
- "Get PET scans from melanoma studies"

## Tasks

### Phase 1: DICOM File Support (8-12 hrs)
- [ ] Install pydicom and SimpleITK
- [ ] Create DICOM parser service
- [ ] Implement DICOM upload endpoint
- [ ] Extract metadata and anonymize patient data
- [ ] Convert DICOM to PNG/JPG for preview
- [ ] Support multi-slice series (CT, MRI)
- [ ] Create REST endpoints for DICOM operations
- [ ] Add tests for DICOM parsing

### Phase 2: DICOM Visualization (12-16 hrs)
- [ ] Research and integrate DICOM viewer library (Cornerstone.js or AMI.js)
- [ ] Create DicomViewer component (2D slices)
- [ ] Implement windowing/leveling controls
- [ ] Add measurement tools (distance, angle, area)
- [ ] Create Volume3D component (3D rendering)
- [ ] Implement VR controls for navigation
- [ ] Add multi-planar reconstruction (MPR)
- [ ] Test with sample DICOM files

### Phase 3: TCIA Integration (10-14 hrs)
- [ ] Create TCIA REST API client (v4)
- [ ] Implement search by collection/modality/body part
- [ ] Enhance Research Agent for imaging queries
- [ ] Add NLP processing for imaging-related queries
- [ ] Create endpoints for imaging search
- [ ] Implement background download of DICOM series
- [ ] Link imaging data to papers in database
- [ ] **Index Awesome DICOM repository into vector DB for RAG**
- [ ] **Enable agent to query DICOM knowledge base** (tools, libraries, best practices)
- [ ] Add tests for TCIA integration

### Phase 4: Imaging Search UI (8-12 hrs)
- [ ] Create ImagingSearchBar component
- [ ] Add modality/body part/disease filters
- [ ] Create ImagingResults component with previews
- [ ] Display DICOM metadata
- [ ] Implement download/view workflow
- [ ] Integrate with 3D scene
- [ ] Add VR voice search for imaging
- [ ] Test end-to-end workflow

## Files to Create

### Backend
- `server/app/services/dicom_service.py`
- `server/app/services/tcia_client.py` (TCIA API v4)
- `server/app/agents/imaging_agent.py` (with RAG support)
- `server/app/api/routes/dicom.py`
- `server/app/api/routes/imaging_search.py`
- `server/app/models/dicom.py`
- `server/data/knowledge_bases/awesome_dicom.md` (indexed for RAG)
- `server/tests/test_dicom_service.py`
- `server/tests/test_tcia_integration.py`

### Frontend
- `client/src/components/dicom/DicomViewer.tsx`
- `client/src/components/dicom/Volume3D.tsx`
- `client/src/components/dicom/DicomControls.tsx`
- `client/src/components/imaging/ImagingSearchBar.tsx`
- `client/src/components/imaging/ImagingResults.tsx`
- `client/src/components/imaging/ImagingPreview.tsx`
- `client/src/lib/dicom/dicomLoader.ts`
- `client/src/lib/dicom/volumeRenderer.ts`
- `client/src/lib/api/imaging.ts`
- `client/src/lib/hooks/useImagingSearch.ts`

## API Endpoints

```
POST   /api/v1/dicom/upload                    # Upload DICOM files
GET    /api/v1/dicom/{id}                      # Get DICOM metadata
GET    /api/v1/dicom/{id}/image                # Get image data
GET    /api/v1/dicom/{id}/series               # Get series information
GET    /api/v1/dicom/studies                   # List all studies
POST   /api/v1/dicom/anonymize                 # Anonymize DICOM data
POST   /api/v1/agents/search/imaging           # Search medical images
GET    /api/v1/agents/search/imaging/{task_id} # Get search results
POST   /api/v1/agents/download/imaging         # Download image series
GET    /api/v1/imaging/collections             # List available collections
```

## Dependencies

- **pydicom:** DICOM file parsing
- **SimpleITK:** Medical image processing
- **Cornerstone.js or AMI.js:** Web-based DICOM viewer
- Issue #10: Agents (Research Agent enhancement with RAG)
- Issue #32: Document API Integration (similar patterns)
- Issue #38: Agent-Assisted Paper Discovery (search infrastructure)

## Technical References

- **DICOM Standard:** https://www.dicomstandard.org/
- **The Cancer Imaging Archive (TCIA):** https://www.cancerimagingarchive.net/
- **TCIA REST API Documentation:** https://wiki.cancerimagingarchive.net/display/Public/TCIA+Programmatic+Interface+REST+API+Guides
- **Awesome DICOM Resources:** https://github.com/open-dicom/awesome-dicom (for RAG knowledge base)
- **Cornerstone.js:** https://cornerstonejs.org/
- **AMI Medical Imaging Toolkit:** https://github.com/FNNDSC/ami
- **Cornerstone.js:** https://cornerstonejs.org/
- **AMI Medical Imaging Toolkit:** https://github.com/FNNDSC/ami

## Acceptance Criteria

- [ ] Can upload and parse DICOM files
- [ ] DICOM metadata is extracted and stored
- [ ] Patient data is properly anonymized
- [ ] 2D slice viewer displays images with windowing controls
- [ ] 3D volume rendering works in VR
- [ ] Can search TCIA by modality and body part
- [ ] Agent understands natural language imaging queries
- [ ] VR volume viewing maintains 60+ FPS
- [ ] Measurement tools are accurate
- [ ] Can link images to related papers
- [ ] End-to-end workflow tested

## Success Metrics

- DICOM files load within 2 seconds
- 3D rendering at 60+ FPS in VR
- TCIA searches return results within 5 seconds
- Natural language query accuracy >80%
- All medical data properly anonymized

## Privacy & Compliance

⚠️ **Important:** This feature handles medical imaging data. Ensure:
- All DICOM files are anonymized (remove PHI)
- HIPAA compliance if using patient data
- Secure storage with encryption
- Proper access controls
- Data retention policies

## Related Issues

- Issue #10: Complete Agents (Research Agent)
- Issue #32: Document API Integration
- Issue #38: Agent-Assisted Paper Discovery

## Estimated Time

**Total:** 38-54 hours
- Backend: 18-26 hours
- Frontend: 20-28 hours

## Priority

**P2 (Medium)** - Advanced feature for Phase 3

## Documentation

See `USER_STORY_DICOM_VISUALIZATION.md` for complete specification, examples, and implementation details.

---

## How to Create These Issues

1. Go to: https://github.com/buddha314/babocument/issues/new
2. Copy the content from each issue above
3. Set labels as indicated
4. Assign to yourself if needed
5. Create issue

**Note:** The issue templates are also available in `.github/ISSUE_TEMPLATE/` for reference.

