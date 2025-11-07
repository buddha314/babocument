# Project Task List - Babocument

**Last Updated:** 2025-11-06 (REPRIORITIZED)
**Current Phase:** Phase 1 Backend - 75% Complete
**GitHub Issues:** 18 open | 10 closed

**🎯 CRITICAL PATH:**
1. Issue #19: Event Bus (3-4 hrs) ← **DO FIRST**
2. Issue #10: Agents (6-8 hrs) ← **DO SECOND**
3. **Phase 1 Complete!** (100%)

**📊 See PRIORITY_ANALYSIS_2025-11-06.md for complete details**

---

## P0 - CRITICAL (Blocking Phase 1)

### Issue #19: Event Bus Implementation ⭐ **START HERE**
- **Time:** 3-4 hours
- **Status:** Not started
- **Blocks:** #10, #21, #22
- **Link:** https://github.com/buddha314/babocument/issues/19

Implement Redis pub/sub for agent coordination. Create event_bus.py, write tests, integrate with coordinator.

### Issue #10: Complete Agents ⭐ **DO NEXT**
- **Time:** 6-8 hours  
- **Status:** 25% (base classes only)
- **Depends on:** #19
- **Link:** https://github.com/buddha314/babocument/issues/10

**CRITICAL:** Create missing files (analysis.py, summary.py, recommendation.py), complete research.py, fix coordinator initialization.

---

## P1 - HIGH (Required for Production)

### Issue #27: Security Audit & Hardening
- **Time:** 2-3 hours
- **Link:** https://github.com/buddha314/babocument/issues/27

Input sanitization, CORS, rate limiting, file upload validation.

### Issue #23: Authentication & Authorization
- **Time:** 4-6 hours
- **Link:** https://github.com/buddha314/babocument/issues/23

JWT/API keys, middleware, protected endpoints.

### Issue #18: CI/CD Pipeline
- **Time:** 2-3 hours
- **Link:** https://github.com/buddha314/babocument/issues/18

GitHub Actions for server + client testing.

### Issue #20: Database Layer
- **Time:** 3-4 hours
- **Link:** https://github.com/buddha314/babocument/issues/20

SQLAlchemy models, migrations, persistent metadata.

---

## P2 - MEDIUM (Quality Improvements)

### Issue #21: WebSocket Handler
- **Time:** 2-3 hours
- **Depends on:** #19
- **Link:** https://github.com/buddha314/babocument/issues/21

Real-time updates for agent tasks.

### Issue #22: Background Task Processing
- **Time:** 2-3 hours
- **Depends on:** #19
- **Link:** https://github.com/buddha314/babocument/issues/22

Celery for async PDF processing.

### Issue #25: Error Handling Standardization
- **Time:** 2-3 hours
- **Link:** https://github.com/buddha314/babocument/issues/25

Consistent error responses across APIs.

### Issue #28: Resolve All TODOs
- **Time:** 2-3 hours
- **Link:** https://github.com/buddha314/babocument/issues/28

Clean up 19 TODO comments in codebase.

### Issue #24: API Documentation & Usage Guide
- **Time:** 2-3 hours
- **Link:** https://github.com/buddha314/babocument/issues/24

Create docs/API_USAGE_GUIDE.md with examples.

### Issue #14: Select Optimal LLM Models
- **Time:** Research + benchmarking
- **Link:** https://github.com/buddha314/babocument/issues/14

Benchmark models for each agent type.

---

## P3 - LOW (Future Work)

### Issue #29: Code Linting & Formatting
- **Time:** 1 hour
- **Link:** https://github.com/buddha314/babocument/issues/29

Black, flake8, mypy, pre-commit hooks.

### Issue #26: Documentation Cleanup
- **Time:** 1-2 hours
- **Link:** https://github.com/buddha314/babocument/issues/26

Consolidate SESSION_*.md files, remove duplicates.

### Issue #6: Plotly Integration Decision
- **Type:** Decision (Phase 3)
- **Link:** https://github.com/buddha314/babocument/issues/6

Canvas texture vs HTML overlay for 3D viz.

### Issue #7: Blender Asset Pipeline
- **Type:** Setup (Phase 3)
- **Link:** https://github.com/buddha314/babocument/issues/7

Blender → GLB export workflow.

### Issue #8: Keyword Trend Graphs
- **Type:** Feature (Phase 5)
- **Depends on:** #10
- **Link:** https://github.com/buddha314/babocument/issues/8

Plotly visualizations of keyword trends.

### Issue #11: Data Visualization UI
- **Type:** Epic (Phase 3)
- **Link:** https://github.com/buddha314/babocument/issues/11

Complete BabylonJS + Plotly integration.

---

## ✅ Completed

### Issue #15: Service Integration
- **Completed:** 2025-11-06
- 17 REST endpoints connected to Vector DB and LLM
- 92 tests passing, 84% coverage

### Issue #9: Vector DB Initialization
- **Completed:** 2025-11-06
- 4 papers indexed, semantic search working

### Issues #1-5: Phase 0 Decisions
- **Completed:** 2025-11-06
- All architectural decisions made

### Issue #12: Launch Scripts
- **Completed:** 2025-11-06
- PowerShell scripts for dev environment

---

## Quick Reference

**Total Issues:** 28 (18 open, 10 closed)

**Priority Distribution:**
- P0: 2 issues (9-12 hours)
- P1: 4 issues (11-16 hours)
- P2: 6 issues (12-18 hours)
- P3: 6 issues (future)

**Time to Phase 1:** 9-12 hours  
**Time to Production:** 20-28 hours

**Next Action:** Start Issue #19 (Event Bus)

---

For detailed dependency graph, risk assessment, and week-by-week plan, see:
**PRIORITY_ANALYSIS_2025-11-06.md**
