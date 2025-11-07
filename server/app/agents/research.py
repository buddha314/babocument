"""
Research Agent

Handles query understanding and multi-source document retrieval.
"""

from typing import Any

from app.agents.base import BaseAgent


class ResearchAgent(BaseAgent):
    """
    Research Agent - Query understanding and document retrieval.

    Responsibilities:
    - Parse and understand user research queries (natural language)
    - Extract search intent, keywords, filters from conversational input
    - Search vector database for relevant papers
    - Query MCP servers (arXiv, PubMed, bioRxiv) - Phase 2
    - Search ClinicalTrials.gov - Phase 2
    - Rank and filter results by relevance
    - Generate "why this matches" explanations for results
    """

    def __init__(self, event_bus=None, vector_db=None, llm_client=None):
        """
        Initialize Research Agent.

        Args:
            event_bus: Event bus for publishing updates
            vector_db: Vector database client for semantic search
            llm_client: LLM client for query understanding and explanations
        """
        super().__init__("research", event_bus)
        self.vector_db = vector_db
        self.llm_client = llm_client

    async def process_task(
        self, task_id: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Process a research query task.

        Args:
            task_id: Unique task identifier
            params: Task parameters including:
                - query: Search query string
                - filters: Optional filters (date_range, sources, max_results)
                - search_type: 'semantic' or 'keyword' (default: semantic)

        Returns:
            Search results with metadata and relevance explanations
        """
        query = params.get("query", "")
        filters = params.get("filters", {})
        search_type = params.get("search_type", "semantic")

        self.logger.info("starting_research", task_id=task_id, query=query)
        await self.publish_progress(task_id, 10, "Analyzing query...")

        if not query:
            error = "No search query provided"
            await self.publish_error(task_id, error)
            return {"error": error}

        try:
            # Parse query to extract keywords and filters
            parsed_query = await self._parse_query(query)
            await self.publish_progress(task_id, 30, "Searching databases...")

            # Search vector database
            search_results = await self._search_vector_db(
                parsed_query, filters, search_type
            )

            await self.publish_progress(task_id, 70, "Ranking results...")

            # Rank and explain results
            ranked_results = await self._rank_and_explain(
                search_results, query, filters
            )

            result = {
                "task_id": task_id,
                "query": query,
                "parsed_query": parsed_query,
                "search_type": search_type,
                "results": ranked_results,
                "total_found": len(ranked_results),
            }

            await self.publish_progress(task_id, 100, "Search complete")
            await self.publish_completion(task_id, result)

            return result

        except Exception as e:
            error_msg = f"Search failed: {str(e)}"
            self.logger.error("search_error", task_id=task_id, error=error_msg)
            await self.publish_error(task_id, error_msg)
            return {"error": error_msg}

    async def _parse_query(self, query: str) -> dict[str, Any]:
        """
        Parse natural language query to extract search intent.

        Args:
            query: Raw query string

        Returns:
            Parsed query with keywords, filters, and intent
        """
        # TODO: Use LLM to parse query
        # - Extract keywords and key phrases
        # - Identify author names
        # - Extract date ranges ("since 2020", "recent papers")
        # - Identify source preferences
        # - Extract topic focus

        # Placeholder: Simple keyword extraction
        return {
            "keywords": query.split(),
            "authors": [],
            "date_range": None,
            "topics": [],
        }

    async def _search_vector_db(
        self, parsed_query: dict[str, Any], filters: dict[str, Any], search_type: str
    ) -> list[dict[str, Any]]:
        """
        Search vector database for relevant documents.

        Args:
            parsed_query: Parsed query structure
            filters: Additional filters
            search_type: Type of search

        Returns:
            List of matching documents with scores
        """
        # TODO: Implement vector DB search
        # - Convert query to embedding
        # - Query vector DB with similarity search
        # - Apply filters (date, source, etc.)
        # - Return top K results with scores

        # Placeholder
        return []

    async def _rank_and_explain(
        self,
        search_results: list[dict[str, Any]],
        original_query: str,
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Rank results and generate explanations.

        Args:
            search_results: Raw search results
            original_query: User's original query
            filters: Applied filters

        Returns:
            Ranked results with "why this matches" explanations
        """
        # TODO: Implement ranking and explanation
        # - Re-rank by relevance (combine multiple signals)
        # - Use LLM to generate "why this matches" for each result
        # - Include relevance scores

        # Placeholder
        return search_results

    async def search_for_conversation(
        self, query: str, context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Process search query from conversational interface.

        Used by Issue #40: Conversational Agent Interface.

        Args:
            query: Natural language search query
            context: Conversation context including history and preferences

        Returns:
            Search results formatted for conversational response
        """
        # TODO: Extract search parameters from conversational context
        # - Consider previous conversation turns
        # - Apply user preferences from context
        # - Handle follow-up queries ("show me more", "refine that")

        self.logger.info("conversational_search", query=query)

        # Extract filters from context
        filters = context.get("search_filters", {})
        search_type = context.get("preferred_search_type", "semantic")

        # Generate task ID
        task_id = context.get("conversation_id", "conv_unknown")

        # Process search
        result = await self.process_task(
            task_id,
            {"query": query, "filters": filters, "search_type": search_type},
        )

        return {
            "response": self._format_search_response(result, query),
            "results": result.get("results", []),
            "total_found": result.get("total_found", 0),
        }

    def _format_search_response(
        self, search_result: dict[str, Any], original_query: str
    ) -> str:
        """
        Format search results for conversational response.

        Args:
            search_result: Raw search results
            original_query: User's original query

        Returns:
            Natural language response about search results
        """
        if "error" in search_result:
            return f"I encountered an issue while searching: {search_result['error']}"

        total = search_result.get("total_found", 0)

        if total == 0:
            return f"I couldn't find any papers matching '{original_query}'. Would you like to try different search terms?"

        if total == 1:
            return "I found 1 paper that matches your query."

        if total <= 5:
            return f"I found {total} papers matching your query. Here they are:"

        return f"I found {total} papers matching your query. Here are the most relevant ones:"

    async def extract_intent(self, query: str) -> dict[str, Any]:
        """
        Extract intent from natural language query.

        Used for routing to appropriate agent in conversational interface.

        Args:
            query: User's natural language input

        Returns:
            Extracted intent with confidence and parameters
        """
        # TODO: Use LLM to classify intent
        # Intents: search, summarize, analyze, recommend, explain, add_to_workspace

        query_lower = query.lower()

        # Simple rule-based classification (to be replaced with LLM)
        if any(word in query_lower for word in ["find", "search", "show me", "papers about"]):
            return {"intent": "search", "confidence": 0.8, "query": query}
        elif any(word in query_lower for word in ["summarize", "summary", "tldr"]):
            return {"intent": "summarize", "confidence": 0.8}
        elif any(word in query_lower for word in ["compare", "analyze", "difference"]):
            return {"intent": "analyze", "confidence": 0.8}
        elif any(word in query_lower for word in ["recommend", "suggest", "related"]):
            return {"intent": "recommend", "confidence": 0.8}
        else:
            return {"intent": "unknown", "confidence": 0.3, "query": query}
