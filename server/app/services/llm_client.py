"""
LLM Client Service

LiteLLM wrapper for local LLM inference via Ollama.
Supports multiple models for different tasks (summarization, chat, analysis).
"""

import structlog
from typing import Any, Literal

from litellm import completion, acompletion
from litellm.exceptions import (
    APIError,
    Timeout,
    RateLimitError,
    ServiceUnavailableError,
)

from app.config import settings

logger = structlog.get_logger(__name__)


class LLMClient:
    """
    LLM client for inference using LiteLLM + Ollama.
    
    Provides specialized methods for different agent tasks:
    - Summarization (llama3.2:3b)
    - Chat/conversation (qwen2.5:7b)
    - Instruction following (mistral:7b)
    - Query understanding (mistral:7b)
    """

    # Model assignments by task (from LLM_HOSTING_DECISION.md)
    MODELS = {
        "summarization": "ollama/llama3.2:3b",      # Fast, good quality summaries
        "chat": "ollama/qwen2.5:7b",                 # Natural dialogue
        "instruction": "ollama/mistral:7b",          # Excellent instruction following
        "query": "ollama/mistral:7b",                # Query understanding
        "analysis": "ollama/llama3.1:8b",            # Structured output, factual
    }

    def __init__(
        self,
        base_url: str | None = None,
        default_model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        timeout: int | None = None,
    ):
        """
        Initialize LLM client.
        
        Args:
            base_url: Ollama API base URL (defaults to config)
            default_model: Default model to use (defaults to config)
            temperature: Sampling temperature 0-1 (defaults to config)
            max_tokens: Maximum tokens to generate (defaults to config)
            timeout: Request timeout in seconds (defaults to config)
        """
        self.base_url = base_url or settings.ollama_base_url
        self.default_model = default_model or settings.llm_model
        self.temperature = temperature or settings.llm_temperature
        self.max_tokens = max_tokens or settings.llm_max_tokens
        self.timeout = timeout or settings.llm_timeout

        logger.info(
            "initializing_llm_client",
            base_url=self.base_url,
            default_model=self.default_model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

    async def complete(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        stream: bool = False,
    ) -> str | None:
        """
        Generic completion method.
        
        Args:
            messages: Chat messages in OpenAI format
            model: Model to use (overrides default)
            temperature: Sampling temperature (overrides default)
            max_tokens: Max tokens to generate (overrides default)
            stream: Whether to stream response (not implemented yet)
            
        Returns:
            Generated text or None on error
            
        Example:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is 2+2?"}
            ]
            response = await client.complete(messages)
        """
        model = model or self.default_model
        temperature = temperature or self.temperature
        max_tokens = max_tokens or self.max_tokens

        logger.debug(
            "llm_completion_request",
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            message_count=len(messages),
        )

        try:
            response = await acompletion(
                model=model,
                messages=messages,
                api_base=self.base_url,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=self.timeout,
            )

            # Extract content from response (type: ignore due to dynamic LiteLLM types)
            content = response.choices[0].message.content  # type: ignore
            
            logger.info(
                "llm_completion_success",
                model=model,
                input_messages=len(messages),
                output_length=len(content) if content else 0,
            )

            return content

        except Timeout as e:
            logger.error(
                "llm_timeout",
                model=model,
                timeout=self.timeout,
                error=str(e),
            )
            return None

        except RateLimitError as e:
            logger.error(
                "llm_rate_limit",
                model=model,
                error=str(e),
            )
            return None

        except ServiceUnavailableError as e:
            logger.error(
                "llm_service_unavailable",
                model=model,
                base_url=self.base_url,
                error=str(e),
            )
            return None

        except APIError as e:
            logger.error(
                "llm_api_error",
                model=model,
                error=str(e),
            )
            return None

        except Exception as e:
            logger.exception(
                "llm_unexpected_error",
                model=model,
                error=str(e),
            )
            return None

    async def summarize(
        self,
        text: str,
        max_length: int = 200,
        style: Literal["concise", "detailed", "bullet"] = "concise",
    ) -> str | None:
        """
        Summarize research paper or document.
        
        Optimized for scientific paper summarization using llama3.2:3b.
        
        Args:
            text: Text to summarize (title, abstract, full text)
            max_length: Target word count for summary
            style: Summary style (concise/detailed/bullet points)
            
        Returns:
            Summary text or None on error
            
        Example:
            summary = await client.summarize(
                abstract_text,
                max_length=100,
                style="concise"
            )
        """
        # Style-specific prompts
        style_prompts = {
            "concise": f"Provide a concise {max_length}-word summary focusing on key findings.",
            "detailed": f"Provide a detailed {max_length}-word summary covering methodology, findings, and implications.",
            "bullet": f"Provide a {max_length}-word summary as bullet points highlighting:\n- Main objective\n- Key methods\n- Primary findings\n- Significance",
        }

        system_prompt = """You are a scientific paper summarizer specializing in biomanufacturing and synthetic biology.
Your summaries are accurate, concise, and preserve technical terminology.
Focus on research objectives, methods, key findings, and significance."""

        user_prompt = f"""{style_prompts[style]}

Text to summarize:
{text}

Provide the summary:"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        logger.info(
            "llm_summarize_request",
            text_length=len(text),
            max_length=max_length,
            style=style,
        )

        # Use summarization model (llama3.2:3b - fast)
        return await self.complete(
            messages,
            model=self.MODELS["summarization"],
            temperature=0.7,  # Balance creativity and factuality
        )

    async def chat(
        self,
        user_message: str,
        conversation_history: list[dict[str, str]] | None = None,
        character: Literal["librarian", "assistant"] = "librarian",
    ) -> str | None:
        """
        Chat/conversation interface for Librarian character.
        
        Optimized for natural dialogue using qwen2.5:7b.
        
        Args:
            user_message: User's message
            conversation_history: Previous messages in conversation
            character: Character personality (librarian/assistant)
            
        Returns:
            Response message or None on error
            
        Example:
            response = await client.chat(
                "Can you help me find papers on bioinks?",
                conversation_history=previous_messages,
                character="librarian"
            )
        """
        # Character-specific system prompts
        character_prompts = {
            "librarian": """You are the Librarian, a knowledgeable and friendly guide in a virtual research library.
You help researchers navigate biomanufacturing and synthetic biology literature.
You are professional, concise, and encouraging.
You remember context from the conversation and provide relevant suggestions.""",
            "assistant": """You are a helpful research assistant specializing in biomanufacturing and synthetic biology.
You provide clear, accurate information and help users find relevant research papers.
You are friendly, professional, and concise.""",
        }

        system_message = {
            "role": "system",
            "content": character_prompts[character],
        }

        # Build message history
        messages = [system_message]
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})

        logger.info(
            "llm_chat_request",
            character=character,
            message_length=len(user_message),
            history_length=len(conversation_history) if conversation_history else 0,
        )

        # Use chat model (qwen2.5:7b - natural dialogue)
        return await self.complete(
            messages,
            model=self.MODELS["chat"],
            temperature=0.8,  # More creative for natural conversation
        )

    async def extract_keywords(
        self,
        text: str,
        max_keywords: int = 10,
    ) -> list[str] | None:
        """
        Extract keywords/topics from research text.
        
        Uses instruction-following model (mistral:7b) for structured output.
        
        Args:
            text: Text to analyze
            max_keywords: Maximum number of keywords to extract
            
        Returns:
            List of keywords or None on error
            
        Example:
            keywords = await client.extract_keywords(abstract_text, max_keywords=5)
        """
        system_prompt = """You are a research paper analyzer.
Extract the most important keywords and technical terms from the text.
Return ONLY a comma-separated list of keywords, nothing else."""

        user_prompt = f"""Extract the {max_keywords} most important keywords from this research text.
Return only the comma-separated list.

Text:
{text}

Keywords:"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        logger.info(
            "llm_extract_keywords",
            text_length=len(text),
            max_keywords=max_keywords,
        )

        # Use instruction model (mistral:7b - excellent structured output)
        response = await self.complete(
            messages,
            model=self.MODELS["instruction"],
            temperature=0.5,  # Lower temperature for consistent extraction
            max_tokens=200,
        )

        if not response:
            return None

        # Parse comma-separated keywords
        keywords = [k.strip() for k in response.split(",") if k.strip()]
        return keywords[:max_keywords]

    async def parse_query(
        self,
        user_query: str,
    ) -> dict[str, Any] | None:
        """
        Parse user search query into structured parameters.
        
        Extracts keywords, time ranges, filters from natural language query.
        
        Args:
            user_query: Natural language search query
            
        Returns:
            Structured query parameters or None on error
            
        Example:
            params = await client.parse_query(
                "Find papers about bioinks published after 2020"
            )
            # Returns: {"keywords": ["bioinks"], "year_min": 2020}
        """
        system_prompt = """You are a search query parser.
Convert natural language research queries into structured parameters.
Return a JSON object with these fields (only include if specified):
- keywords: array of search terms
- year_min: minimum publication year (integer)
- year_max: maximum publication year (integer)
- authors: array of author names
- topics: array of research topics

Return ONLY valid JSON, nothing else."""

        user_prompt = f"""Parse this search query into structured parameters:

Query: {user_query}

JSON:"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        logger.info(
            "llm_parse_query",
            query_length=len(user_query),
        )

        # Use instruction model (mistral:7b - structured output)
        response = await self.complete(
            messages,
            model=self.MODELS["instruction"],
            temperature=0.3,  # Very low for consistent parsing
            max_tokens=300,
        )

        if not response:
            return None

        # Parse JSON response
        try:
            import json
            # Extract JSON from response (in case of markdown code blocks)
            json_str = response.strip()
            if json_str.startswith("```"):
                json_str = json_str.split("```")[1]
                if json_str.startswith("json"):
                    json_str = json_str[4:]
            json_str = json_str.strip()
            
            return json.loads(json_str)
        except Exception as e:
            logger.error(
                "llm_parse_query_failed",
                response=response,
                error=str(e),
            )
            return None


# Singleton instance for app-wide use
_llm_client: LLMClient | None = None


def get_llm_client() -> LLMClient:
    """
    Get singleton LLM client instance.
    
    Returns:
        Shared LLMClient instance
        
    Example:
        from app.services.llm_client import get_llm_client
        
        client = get_llm_client()
        summary = await client.summarize(text)
    """
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
