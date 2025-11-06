# LLM Hosting Solution Decision

**Decision Status:** ✅ RECOMMENDED - Ollama + LiteLLM Gateway
**Date:** 2025-11-06
**Context:** Issue #3

## Executive Summary

**Recommendation:** Use **Ollama for local LLM hosting** with **LiteLLM as an abstraction layer**, providing flexibility to switch between local and cloud models as needed.

## Analysis

### Requirements

Based on project needs:

1. **Summary Agent** - Article summarization, insight extraction
2. **Query Understanding** - Parse complex research queries
3. **Conversation** - Chat with Librarian character
4. **Analysis** - Natural language generation for trends and findings
5. **Privacy** - Keep research queries and documents private
6. **Cost** - Minimize cloud API costs for development
7. **Flexibility** - Ability to upgrade models as needed

### Option A: Ollama (RECOMMENDED)

**Architecture:**
```
Summary Agent → LiteLLM Gateway → Ollama (localhost:11434)
                                ↓
                        Llama 3.2, Mistral, etc.
```

**Pros:**
- ✅ **Zero cloud costs** - Fully local inference
- ✅ **Privacy** - All data stays on local machine
- ✅ **Easy setup** - Single command installation
- ✅ **Model flexibility** - Easy model switching (llama3.2, mistral, qwen, etc.)
- ✅ **Fast iteration** - No API rate limits
- ✅ **Docker support** - Easy deployment
- ✅ **REST API** - OpenAI-compatible endpoints
- ✅ **Hardware efficient** - Works on CPU or GPU

**Cons:**
- ⚠️ **Model size limits** - Constrained by available RAM/VRAM
- ⚠️ **Quality varies** - Smaller models less capable than GPT-4
- ⚠️ **Local compute** - Requires decent hardware

**Best Models for Babocument:**

| Task | Recommended Model | Size | Justification |
|------|-------------------|------|---------------|
| Summarization | `llama3.2:3b` | 2GB | Fast, good quality summaries |
| Query Understanding | `mistral:7b` | 4.1GB | Excellent instruction following |
| Conversation (Librarian) | `qwen2.5:7b` | 4.4GB | Natural dialogue, character consistency |
| Analysis/Reports | `llama3.1:8b` | 4.7GB | Structured output, factual |

**Installation:**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull llama3.2:3b
ollama pull mistral:7b
ollama pull qwen2.5:7b

# Start server (auto-starts on install)
ollama serve
```

**Integration:**
```python
# requirements.txt
litellm==1.17.0

# app/services/llm_client.py
from litellm import completion

async def generate_summary(text: str) -> str:
    response = completion(
        model="ollama/llama3.2:3b",
        messages=[{
            "role": "user",
            "content": f"Summarize this research paper:\n\n{text}"
        }],
        api_base="http://localhost:11434"
    )
    return response.choices[0].message.content
```

### Option B: HuggingFace Transformers

**Architecture:**
```
Summary Agent → Transformers Pipeline → Local Model
                                       ↓
                                GPU/CPU Inference
```

**Pros:**
- ✅ **Model variety** - Thousands of models on HF Hub
- ✅ **Research grade** - Access to cutting-edge models
- ✅ **Fine-tuning** - Can train custom models
- ✅ **Open source** - Full control over inference

**Cons:**
- ❌ **Complex setup** - Requires CUDA, PyTorch configuration
- ❌ **Memory hungry** - Models loaded into Python process
- ❌ **Slower** - No optimized inference engine
- ❌ **More code** - Manual tokenization, generation params
- ❌ **Deployment** - Harder to containerize

**Example:**
```python
from transformers import pipeline

# Heavy initialization
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=0  # GPU required
)

summary = summarizer(text, max_length=200)[0]['summary_text']
```

**When to use:**
- Custom model fine-tuning needed
- Research experimentation
- Specific model requirements

### Option C: LangGraph

**Note:** LangGraph is NOT an LLM hosting solution - it's an agentic workflow framework.

**What it actually does:**
- Graph-based agent orchestration
- State management for multi-step workflows
- Agent coordination patterns

**Confusion clarification:**
- ❌ LangGraph does NOT host LLMs
- ✅ LangGraph coordinates agents that CALL LLMs
- ✅ Works with Ollama, OpenAI, Anthropic, etc.

**Verdict:** Not applicable for this decision. However, we could use LangGraph for agent coordination if needed (separate decision).

### Option D: Cloud APIs (OpenAI, Anthropic)

**Pros:**
- ✅ Highest quality (GPT-4, Claude)
- ✅ Zero local compute
- ✅ Reliable uptime

**Cons:**
- ❌ **Costs** - $0.01-0.10 per request
- ❌ **Privacy** - Data sent to cloud
- ❌ **Rate limits** - API quotas
- ❌ **Network dependency** - Requires internet

**Use case:** Production upgrade path, not for development

## Decision Matrix

| Criterion | Ollama | HuggingFace | Cloud APIs | Weight |
|-----------|--------|-------------|------------|--------|
| Setup Ease | ✅ Excellent | ❌ Complex | ✅ Simple | HIGH |
| Cost (Dev) | ✅ Free | ✅ Free | ❌ Expensive | HIGH |
| Privacy | ✅ Full | ✅ Full | ❌ Limited | MEDIUM |
| Model Quality | ⚠️ Good | ⚠️ Good | ✅ Excellent | MEDIUM |
| Deployment | ✅ Easy | ❌ Hard | ✅ Easy | HIGH |
| Flexibility | ✅ High | ✅ Very High | ⚠️ Limited | MEDIUM |
| Integration | ✅ Simple API | ❌ Manual | ✅ Simple API | HIGH |
| Performance | ✅ Fast | ⚠️ Moderate | ✅ Fast | LOW |

**Winner:** Ollama for development and local deployment

## Recommended Architecture

### Phase 1: Local Development (Ollama)

```python
# app/services/llm_client.py
from litellm import completion
import os

class LLMClient:
    def __init__(self):
        self.default_model = os.getenv("LLM_MODEL", "ollama/llama3.2:3b")
        self.api_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    async def complete(self, messages: list, model: str = None):
        """Generic completion wrapper"""
        model = model or self.default_model

        response = completion(
            model=model,
            messages=messages,
            api_base=self.api_base,
            temperature=0.7
        )

        return response.choices[0].message.content

    async def summarize(self, text: str, max_length: int = 200):
        """Specialized summarization"""
        messages = [{
            "role": "system",
            "content": "You are a scientific paper summarizer. Provide concise, accurate summaries."
        }, {
            "role": "user",
            "content": f"Summarize this research paper in {max_length} words:\n\n{text}"
        }]

        return await self.complete(messages, model="ollama/llama3.2:3b")

    async def chat(self, user_message: str, conversation_history: list):
        """Librarian character chat"""
        system_prompt = {
            "role": "system",
            "content": """You are the Librarian, a knowledgeable guide in a virtual research library.
            You help researchers navigate biomanufacturing and synthetic biology literature.
            Be friendly, professional, and concise."""
        }

        messages = [system_prompt] + conversation_history + [{
            "role": "user",
            "content": user_message
        }]

        return await self.complete(messages, model="ollama/qwen2.5:7b")
```

### Phase 2: Production (Hybrid)

Use **LiteLLM Gateway** to switch between local and cloud:

```python
# .env
LLM_MODEL=ollama/llama3.2:3b  # Development
# LLM_MODEL=gpt-4o-mini         # Production (if needed)
# LLM_MODEL=claude-3-haiku      # Production alternative

OLLAMA_BASE_URL=http://localhost:11434
OPENAI_API_KEY=sk-...  # Only if using cloud
```

**LiteLLM benefits:**
- Unified interface for all LLM providers
- Easy switching without code changes
- Load balancing and fallbacks
- Cost tracking and budgets

## Hardware Requirements

### Minimum (Development)
- **CPU:** 4+ cores
- **RAM:** 8GB
- **Storage:** 10GB for models
- **Model:** llama3.2:3b (2GB)

### Recommended (Development)
- **CPU:** 8+ cores OR **GPU:** 8GB+ VRAM
- **RAM:** 16GB
- **Storage:** 20GB for models
- **Models:** mistral:7b, qwen2.5:7b

### Production (Self-hosted)
- **GPU:** 24GB+ VRAM (RTX 4090, A5000)
- **RAM:** 32GB+
- **Storage:** 50GB for multiple models
- **Models:** llama3.1:70b for best quality

## Model Selection Guide

| Use Case | Model | Size | Speed | Quality | Command |
|----------|-------|------|-------|---------|---------|
| **Fast Summaries** | llama3.2:3b | 2GB | ⚡⚡⚡ | ⭐⭐⭐ | `ollama pull llama3.2:3b` |
| **Quality Summaries** | llama3.1:8b | 4.7GB | ⚡⚡ | ⭐⭐⭐⭐ | `ollama pull llama3.1:8b` |
| **Conversation** | qwen2.5:7b | 4.4GB | ⚡⚡ | ⭐⭐⭐⭐ | `ollama pull qwen2.5:7b` |
| **Instruction Following** | mistral:7b | 4.1GB | ⚡⚡ | ⭐⭐⭐⭐ | `ollama pull mistral:7b` |
| **Best Quality** | llama3.1:70b | 40GB | ⚡ | ⭐⭐⭐⭐⭐ | `ollama pull llama3.1:70b` |
| **Coding (if needed)** | deepseek-coder-v2:16b | 9GB | ⚡⚡ | ⭐⭐⭐⭐ | `ollama pull deepseek-coder-v2:16b` |

## Configuration

### Server Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_MODELS=/root/.ollama/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]  # If GPU available

  babocument-server:
    build: ./server
    depends_on:
      - ollama
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - LLM_MODEL=ollama/llama3.2:3b

volumes:
  ollama_data:
```

### Environment Variables

```bash
# .env
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=ollama/llama3.2:3b
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=500
LLM_TIMEOUT=30

# Optional: Fallback to cloud
OPENAI_API_KEY=sk-...
FALLBACK_MODEL=gpt-4o-mini
```

## Migration Path

### Development → Production

**Option 1: Stay Local (Privacy-focused)**
```
Ollama (3b/7b models) → Ollama (70b model on GPU server)
```

**Option 2: Hybrid (Cost-optimized)**
```
Ollama (local dev) → LiteLLM Gateway → {
    Ollama (self-hosted) for summaries
    GPT-4o-mini for complex queries
}
```

**Option 3: Full Cloud (Simplicity)**
```
Ollama (local dev) → OpenAI API (production)
```

## Testing & Benchmarks

### Evaluation Script

```python
# tests/llm_benchmark.py
import time
from app.services.llm_client import LLMClient

async def benchmark_model(model: str, test_text: str):
    client = LLMClient()

    start = time.time()
    summary = await client.complete([{
        "role": "user",
        "content": f"Summarize: {test_text}"
    }], model=model)
    duration = time.time() - start

    return {
        "model": model,
        "duration_ms": duration * 1000,
        "output_length": len(summary),
        "tokens_per_sec": len(summary.split()) / duration
    }

# Test multiple models
models = [
    "ollama/llama3.2:3b",
    "ollama/mistral:7b",
    "ollama/qwen2.5:7b"
]

for model in models:
    result = await benchmark_model(model, test_abstract)
    print(f"{model}: {result['tokens_per_sec']:.1f} tokens/sec")
```

## Cost Analysis

### Local (Ollama)

| Component | Cost | Notes |
|-----------|------|-------|
| Hardware | $0-1500 | One-time (dev machine or GPU server) |
| Electricity | ~$10/mo | Running 24/7 |
| **Total Year 1** | **$120-1620** | Includes hardware depreciation |

### Cloud (OpenAI)

| Usage Level | Requests/Day | Cost/Month | Cost/Year |
|-------------|--------------|------------|-----------|
| Light | 100 | $30 | $360 |
| Medium | 500 | $150 | $1,800 |
| Heavy | 2000 | $600 | $7,200 |

**Break-even:** Cloud becomes more expensive after ~6 months at medium usage

## Decision Rationale

**Why Ollama:**

1. **Zero cloud costs** - Important for development and bootstrapping
2. **Privacy** - Research queries stay local
3. **Fast iteration** - No API rate limits or quotas
4. **Easy setup** - Single command installation
5. **Production ready** - Docker support, GPU acceleration
6. **Flexibility** - Can upgrade to cloud later via LiteLLM
7. **Good enough quality** - Modern 7b models are surprisingly capable

**Why NOT HuggingFace Transformers:**
- Complex setup and deployment
- Requires deep ML knowledge
- Harder to maintain
- No advantage over Ollama for our use case

**Why NOT LangGraph:**
- Not an LLM hosting solution (framework confusion)
- Can consider later for complex workflows

## Implementation Plan

### Week 1: Setup
- [ ] Install Ollama on dev machines
- [ ] Pull recommended models (llama3.2:3b, mistral:7b, qwen2.5:7b)
- [ ] Implement LLMClient wrapper with LiteLLM
- [ ] Create environment configuration

### Week 2: Integration
- [ ] Integrate LLMClient with Summary Agent
- [ ] Add query understanding to Research Agent
- [ ] Implement Librarian chat system
- [ ] Add conversation state management

### Week 3: Optimization
- [ ] Benchmark different models for each task
- [ ] Tune generation parameters (temperature, max_tokens)
- [ ] Implement caching for repeated queries
- [ ] Add fallback logic

### Week 4: Documentation
- [ ] Document model selection guide
- [ ] Create setup instructions for developers
- [ ] Write prompt engineering best practices
- [ ] Add monitoring and logging

## References

- Ollama: https://ollama.com/
- LiteLLM: https://docs.litellm.ai/
- Model benchmarks: https://ollama.com/library
- specs/MULTI_AGENT_ARCHITECTURE.md (Summary Agent)
- specs/TASKS.md (Phase 5: Agent Intelligence)

## Next Steps

1. ✅ Document decision (this file)
2. Install Ollama on development machines
3. Implement LLMClient wrapper
4. Integrate with Summary Agent
5. Test model quality and performance
6. Update GitHub issue #3 with decision
