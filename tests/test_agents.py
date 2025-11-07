"""
Tests for Agent System

Tests for all specialized agents and coordinator.
"""

import pytest

from app.agents.analysis import AnalysisAgent
from app.agents.coordinator import AgentCoordinator
from app.agents.recommendation import RecommendationAgent
from app.agents.research import ResearchAgent
from app.agents.summary import SummaryAgent


class TestResearchAgent:
    """Tests for Research Agent."""

    @pytest.mark.asyncio
    async def test_research_agent_initialization(self):
        """Test that ResearchAgent initializes correctly."""
        agent = ResearchAgent()
        assert agent.agent_name == "research"
        assert agent.vector_db is None  # No vector DB provided
        assert agent.llm_client is None  # No LLM provided

    @pytest.mark.asyncio
    async def test_research_agent_with_dependencies(self):
        """Test ResearchAgent with mock dependencies."""
        mock_vector_db = object()
        mock_llm = object()
        agent = ResearchAgent(vector_db=mock_vector_db, llm_client=mock_llm)

        assert agent.vector_db is mock_vector_db
        assert agent.llm_client is mock_llm

    @pytest.mark.asyncio
    async def test_process_task_no_query(self):
        """Test that process_task returns error when no query provided."""
        agent = ResearchAgent()
        result = await agent.process_task("task_123", {})

        assert "error" in result
        assert "no search query" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_process_task_with_query(self):
        """Test basic query processing."""
        agent = ResearchAgent()
        result = await agent.process_task(
            "task_123", {"query": "bioink formulation"}
        )

        assert "task_id" in result
        assert "query" in result
        assert result["query"] == "bioink formulation"
        assert "results" in result

    @pytest.mark.asyncio
    async def test_extract_intent_search(self):
        """Test intent extraction for search queries."""
        agent = ResearchAgent()

        intents = [
            await agent.extract_intent("Find papers about CRISPR"),
            await agent.extract_intent("Search for bioink studies"),
            await agent.extract_intent("Show me papers about gene editing"),
        ]

        for intent_data in intents:
            assert intent_data["intent"] == "search"
            assert intent_data["confidence"] > 0.5

    @pytest.mark.asyncio
    async def test_extract_intent_summarize(self):
        """Test intent extraction for summarize queries."""
        agent = ResearchAgent()

        intent_data = await agent.extract_intent("Summarize this paper")
        assert intent_data["intent"] == "summarize"

    @pytest.mark.asyncio
    async def test_extract_intent_analyze(self):
        """Test intent extraction for analysis queries."""
        agent = ResearchAgent()

        intent_data = await agent.extract_intent("Compare these papers")
        assert intent_data["intent"] == "analyze"

    @pytest.mark.asyncio
    async def test_search_for_conversation(self):
        """Test conversational search interface."""
        agent = ResearchAgent()

        context = {"conversation_id": "conv_123", "search_filters": {}}
        result = await agent.search_for_conversation("Find papers about CRISPR", context)

        assert "response" in result
        assert "results" in result
        assert "total_found" in result


class TestAnalysisAgent:
    """Tests for Analysis Agent."""

    @pytest.mark.asyncio
    async def test_analysis_agent_initialization(self):
        """Test that AnalysisAgent initializes correctly."""
        agent = AnalysisAgent()
        assert agent.agent_name == "analysis"

    @pytest.mark.asyncio
    async def test_process_task_no_documents(self):
        """Test that process_task returns error when no documents provided."""
        agent = AnalysisAgent()
        result = await agent.process_task("task_123", {"operation": "compare"})

        assert "error" in result

    @pytest.mark.asyncio
    async def test_process_task_compare(self):
        """Test compare operation."""
        agent = AnalysisAgent()
        result = await agent.process_task(
            "task_123",
            {
                "operation": "compare",
                "document_ids": ["doc1", "doc2"],
            },
        )

        assert "operation" in result
        assert result["operation"] == "compare"
        assert "similarities" in result
        assert "differences" in result

    @pytest.mark.asyncio
    async def test_process_task_extract(self):
        """Test extract insights operation."""
        agent = AnalysisAgent()
        result = await agent.process_task(
            "task_123",
            {
                "operation": "extract",
                "document_ids": ["doc1"],
            },
        )

        assert result["operation"] == "extract"
        assert "key_findings" in result

    @pytest.mark.asyncio
    async def test_analyze_for_conversation(self):
        """Test conversational analysis interface."""
        agent = AnalysisAgent()

        context = {
            "conversation_id": "conv_123",
            "selected_documents": ["doc1", "doc2"],
        }
        result = await agent.analyze_for_conversation("Compare these papers", context)

        assert "response" in result
        assert "analysis_data" in result


class TestSummaryAgent:
    """Tests for Summary Agent."""

    @pytest.mark.asyncio
    async def test_summary_agent_initialization(self):
        """Test that SummaryAgent initializes correctly."""
        agent = SummaryAgent()
        assert agent.agent_name == "summary"

    @pytest.mark.asyncio
    async def test_process_task_no_documents(self):
        """Test that process_task returns error when no documents provided."""
        agent = SummaryAgent()
        result = await agent.process_task("task_123", {})

        assert "error" in result

    @pytest.mark.asyncio
    async def test_process_task_single_document(self):
        """Test single document summarization."""
        agent = SummaryAgent()
        result = await agent.process_task(
            "task_123",
            {
                "document_ids": ["doc1"],
                "summary_type": "concise",
            },
        )

        assert "summary" in result
        assert result["document_id"] == "doc1"

    @pytest.mark.asyncio
    async def test_process_task_multiple_documents(self):
        """Test multiple document summarization."""
        agent = SummaryAgent()
        result = await agent.process_task(
            "task_123",
            {
                "document_ids": ["doc1", "doc2", "doc3"],
                "summary_type": "detailed",
            },
        )

        assert "meta_summary" in result
        assert len(result["document_ids"]) == 3

    @pytest.mark.asyncio
    async def test_extract_summary_type(self):
        """Test summary type extraction from query."""
        agent = SummaryAgent()

        assert agent._extract_summary_type("Give me a detailed summary") == "detailed"
        assert agent._extract_summary_type("Explain in simple terms") == "eli5"
        assert agent._extract_summary_type("Technical summary") == "technical"
        assert agent._extract_summary_type("Quick summary") == "concise"

    @pytest.mark.asyncio
    async def test_extract_focus(self):
        """Test focus area extraction from query."""
        agent = SummaryAgent()

        assert agent._extract_focus("Summarize the methodology") == "methodology"
        assert agent._extract_focus("What are the results?") == "results"
        assert agent._extract_focus("Show me the conclusions") == "conclusions"
        assert agent._extract_focus("Just summarize it") is None


class TestRecommendationAgent:
    """Tests for Recommendation Agent."""

    @pytest.mark.asyncio
    async def test_recommendation_agent_initialization(self):
        """Test that RecommendationAgent initializes correctly."""
        agent = RecommendationAgent()
        assert agent.agent_name == "recommendation"

    @pytest.mark.asyncio
    async def test_process_task_similar(self):
        """Test similar paper recommendations."""
        agent = RecommendationAgent()
        result = await agent.process_task(
            "task_123",
            {
                "strategy": "similar",
                "seed_documents": ["doc1"],
            },
        )

        assert result["strategy"] == "similar"
        assert "recommendations" in result

    @pytest.mark.asyncio
    async def test_process_task_trending(self):
        """Test trending paper recommendations."""
        agent = RecommendationAgent()
        result = await agent.process_task(
            "task_123",
            {
                "strategy": "trending",
                "seed_documents": ["doc1"],
            },
        )

        assert result["strategy"] == "trending"
        assert "identified_topics" in result

    @pytest.mark.asyncio
    async def test_extract_strategy(self):
        """Test strategy extraction from query."""
        agent = RecommendationAgent()

        assert agent._extract_strategy("What's trending?") == "trending"
        assert agent._extract_strategy("Show me similar papers") == "similar"
        assert agent._extract_strategy("Who cites this?") == "citations"
        assert agent._extract_strategy("Am I missing something?") == "gaps"


class TestAgentCoordinator:
    """Tests for Agent Coordinator."""

    @pytest.mark.asyncio
    async def test_coordinator_initialization(self):
        """Test that AgentCoordinator initializes with all agents."""
        coordinator = AgentCoordinator()

        # Check all agents are initialized
        assert "research" in coordinator.agents
        assert "analysis" in coordinator.agents
        assert "summary" in coordinator.agents
        assert "recommendation" in coordinator.agents

        # Check agents are correct types
        assert isinstance(coordinator.agents["research"], ResearchAgent)
        assert isinstance(coordinator.agents["analysis"], AnalysisAgent)
        assert isinstance(coordinator.agents["summary"], SummaryAgent)
        assert isinstance(coordinator.agents["recommendation"], RecommendationAgent)

    @pytest.mark.asyncio
    async def test_get_agent_status(self):
        """Test getting status of all agents."""
        coordinator = AgentCoordinator()
        status = coordinator.get_agent_status()

        assert "agents" in status
        assert "total_agents" in status
        assert status["total_agents"] == 4
        assert "research" in status["agents"]

    @pytest.mark.asyncio
    async def test_handle_request_search(self):
        """Test handling search request."""
        coordinator = AgentCoordinator()
        result = await coordinator.handle_request(
            "search", {"query": "CRISPR gene editing"}
        )

        assert "query" in result or "error" in result

    @pytest.mark.asyncio
    async def test_handle_request_analyze(self):
        """Test handling analysis request."""
        coordinator = AgentCoordinator()
        result = await coordinator.handle_request(
            "analyze",
            {
                "operation": "compare",
                "document_ids": ["doc1", "doc2"],
            },
        )

        assert "operation" in result or "error" in result

    @pytest.mark.asyncio
    async def test_handle_request_summarize(self):
        """Test handling summarize request."""
        coordinator = AgentCoordinator()
        result = await coordinator.handle_request(
            "summarize",
            {
                "document_ids": ["doc1"],
            },
        )

        assert "summary" in result or "meta_summary" in result or "error" in result

    @pytest.mark.asyncio
    async def test_handle_request_recommend(self):
        """Test handling recommend request."""
        coordinator = AgentCoordinator()
        result = await coordinator.handle_request(
            "recommend",
            {
                "strategy": "similar",
                "seed_documents": ["doc1"],
            },
        )

        assert "recommendations" in result or "error" in result

    @pytest.mark.asyncio
    async def test_handle_request_unknown(self):
        """Test handling unknown request type."""
        coordinator = AgentCoordinator()
        result = await coordinator.handle_request("unknown_type", {})

        assert "error" in result
        assert "unknown" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_handle_conversation_search(self):
        """Test conversational search request."""
        coordinator = AgentCoordinator()

        context = {"conversation_id": "conv_123"}
        result = await coordinator.handle_conversation(
            "Find papers about bioink formulation", context
        )

        assert "response" in result

    @pytest.mark.asyncio
    async def test_handle_conversation_summarize(self):
        """Test conversational summarize request."""
        coordinator = AgentCoordinator()

        context = {
            "conversation_id": "conv_123",
            "selected_documents": ["doc1"],
        }
        result = await coordinator.handle_conversation("Summarize this paper", context)

        assert "response" in result

    @pytest.mark.asyncio
    async def test_handle_conversation_unknown_intent(self):
        """Test handling conversation with unknown intent."""
        coordinator = AgentCoordinator()

        context = {"conversation_id": "conv_123"}
        result = await coordinator.handle_conversation(
            "Do something unclear", context
        )

        assert "response" in result
        assert "requires_clarification" in result or "help" in result["response"].lower()
