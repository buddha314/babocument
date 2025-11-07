"""
Agent Coordinator

Central coordinator for managing specialized agents and routing tasks.
"""

from typing import Any
from uuid import uuid4

import structlog

from app.agents.analysis import AnalysisAgent
from app.agents.recommendation import RecommendationAgent
from app.agents.research import ResearchAgent
from app.agents.summary import SummaryAgent

logger = structlog.get_logger()


class AgentCoordinator:
    """
    Agent Coordinator - Central orchestrator for multi-agent system.

    Responsibilities:
    - Accept incoming requests from API/WebSocket
    - Route requests to appropriate specialized agents
    - Manage agent lifecycle and health
    - Coordinate multi-agent workflows
    - Publish events to WebSocket clients
    - Handle conversational requests and intent routing
    """

    def __init__(self, event_bus=None, vector_db=None, llm_client=None):
        """
        Initialize Agent Coordinator.

        Args:
            event_bus: Event bus for agent communication
            vector_db: Vector database client
            llm_client: LLM client for text generation
        """
        self.event_bus = event_bus
        self.vector_db = vector_db
        self.llm_client = llm_client
        self.agents = {}
        self.logger = logger.bind(component="coordinator")

        # Initialize all agents
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize all specialized agents."""
        try:
            self.agents["research"] = ResearchAgent(
                event_bus=self.event_bus,
                vector_db=self.vector_db,
                llm_client=self.llm_client,
            )
            self.logger.info("agent_initialized", agent="research")
        except Exception as e:
            self.logger.warning("agent_init_failed", agent="research", error=str(e))

        try:
            self.agents["analysis"] = AnalysisAgent(
                event_bus=self.event_bus,
                vector_db=self.vector_db,
                llm_client=self.llm_client,
            )
            self.logger.info("agent_initialized", agent="analysis")
        except Exception as e:
            self.logger.warning("agent_init_failed", agent="analysis", error=str(e))

        try:
            self.agents["summary"] = SummaryAgent(
                event_bus=self.event_bus,
                llm_client=self.llm_client,
                vector_db=self.vector_db,
            )
            self.logger.info("agent_initialized", agent="summary")
        except Exception as e:
            self.logger.warning("agent_init_failed", agent="summary", error=str(e))

        try:
            self.agents["recommendation"] = RecommendationAgent(
                event_bus=self.event_bus,
                vector_db=self.vector_db,
                llm_client=self.llm_client,
            )
            self.logger.info("agent_initialized", agent="recommendation")
        except Exception as e:
            self.logger.warning("agent_init_failed", agent="recommendation", error=str(e))

        self.logger.info("coordinator_initialized", agent_count=len(self.agents))

    async def handle_request(self, request_type: str, params: dict[str, Any]) -> dict[str, Any]:
        """
        Handle incoming request and route to appropriate agent.

        Args:
            request_type: Type of request ('search', 'analyze', 'summarize', 'recommend')
            params: Request parameters

        Returns:
            Task result dictionary with task_id
        """
        task_id = str(uuid4())

        self.logger.info(
            "handling_request",
            task_id=task_id,
            request_type=request_type,
        )

        # Publish task started event
        if self.event_bus:
            await self.event_bus.publish(
                "task.started",
                {
                    "task_id": task_id,
                    "type": request_type,
                    "params": params,
                },
            )

        # Route to appropriate agent
        try:
            if request_type == "search":
                agent = self.agents.get("research")
                if agent:
                    result = await agent.process_task(task_id, params)
                else:
                    result = {"error": "Research agent not initialized"}

            elif request_type == "analyze":
                agent = self.agents.get("analysis")
                if agent:
                    result = await agent.process_task(task_id, params)
                else:
                    result = {"error": "Analysis agent not initialized"}

            elif request_type == "summarize":
                agent = self.agents.get("summary")
                if agent:
                    result = await agent.process_task(task_id, params)
                else:
                    result = {"error": "Summary agent not initialized"}

            elif request_type == "recommend":
                agent = self.agents.get("recommendation")
                if agent:
                    result = await agent.process_task(task_id, params)
                else:
                    result = {"error": "Recommendation agent not initialized"}

            else:
                result = {"error": f"Unknown request type: {request_type}"}

        except Exception as e:
            self.logger.error("task_error", task_id=task_id, error=str(e))
            result = {"error": str(e)}

            # Publish error event
            if self.event_bus:
                await self.event_bus.publish(
                    f"task.failed.{task_id}",
                    {"task_id": task_id, "error": str(e)},
                )

        return result

    async def handle_conversation(
        self, message: str, context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Handle conversational request with natural language understanding.

        Used by Issue #40: Conversational Agent Interface.

        Args:
            message: User's natural language message
            context: Conversation context including history and state

        Returns:
            Agent response with action results
        """
        self.logger.info("handling_conversation", message=message[:100])

        try:
            # Extract intent using Research Agent
            research_agent = self.agents.get("research")
            if not research_agent:
                return {
                    "response": "I'm not fully initialized yet. Please try again in a moment.",
                    "error": "Research agent not available",
                }

            intent_data = await research_agent.extract_intent(message)
            intent = intent_data.get("intent", "unknown")

            self.logger.info("intent_extracted", intent=intent)

            # Route to appropriate agent based on intent
            if intent == "search":
                agent = self.agents.get("research")
                if agent:
                    result = await agent.search_for_conversation(message, context)
                else:
                    result = {"response": "Search capability not available"}

            elif intent == "summarize":
                agent = self.agents.get("summary")
                if agent:
                    result = await agent.summarize_for_conversation(message, context)
                else:
                    result = {"response": "Summary capability not available"}

            elif intent == "analyze":
                agent = self.agents.get("analysis")
                if agent:
                    result = await agent.analyze_for_conversation(message, context)
                else:
                    result = {"response": "Analysis capability not available"}

            elif intent == "recommend":
                agent = self.agents.get("recommendation")
                if agent:
                    result = await agent.recommend_for_conversation(message, context)
                else:
                    result = {"response": "Recommendation capability not available"}

            else:
                # Unknown intent - provide helpful response
                result = {
                    "response": "I'm not sure I understand. I can help you search for papers, "
                    "summarize documents, analyze research, or recommend related work. "
                    "What would you like to do?",
                    "requires_clarification": True,
                }

            return result

        except Exception as e:
            self.logger.error("conversation_error", error=str(e))
            return {
                "response": "I encountered an error processing your request. Could you try rephrasing?",
                "error": str(e),
            }

    def get_agent_status(self) -> dict[str, Any]:
        """
        Get status of all agents.

        Returns:
            Dictionary of agent statuses
        """
        return {
            "agents": {
                name: {
                    "name": agent.agent_name,
                    "status": "active",
                }
                for name, agent in self.agents.items()
            },
            "total_agents": len(self.agents),
        }
