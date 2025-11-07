"""
Base Agent Class

Abstract base class for all specialized agents in the system.
"""

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

import structlog

logger = structlog.get_logger()


class BaseAgent(ABC):
    """
    Abstract base class for all agents.

    Provides common functionality for:
    - Event publishing
    - Progress tracking
    - Error handling
    - Logging
    """

    def __init__(self, agent_name: str, event_bus=None):
        """
        Initialize base agent.

        Args:
            agent_name: Name of the agent (e.g., 'research', 'analysis')
            event_bus: Event bus for publishing updates (optional)
        """
        self.agent_name = agent_name
        self.event_bus = event_bus
        self.logger = logger.bind(agent=agent_name)

    async def publish_progress(
        self, task_id: str, progress: int, message: str
    ) -> None:
        """
        Publish progress update to event bus.

        Args:
            task_id: Unique task identifier
            progress: Progress percentage (0-100)
            message: Progress message
        """
        if self.event_bus:
            await self.event_bus.publish(
                f"task.progress.{task_id}",
                {
                    "task_id": task_id,
                    "agent": self.agent_name,
                    "progress": progress,
                    "message": message,
                },
            )

        self.logger.info(
            "task_progress",
            task_id=task_id,
            progress=progress,
            message=message,
        )

    async def publish_completion(self, task_id: str, result: dict[str, Any]) -> None:
        """
        Publish task completion to event bus.

        Args:
            task_id: Unique task identifier
            result: Task result data
        """
        if self.event_bus:
            await self.event_bus.publish(
                f"task.completed.{task_id}",
                {
                    "task_id": task_id,
                    "agent": self.agent_name,
                    "result": result,
                },
            )

        self.logger.info("task_completed", task_id=task_id, agent=self.agent_name)

    async def publish_error(self, task_id: str, error: str) -> None:
        """
        Publish task error to event bus.

        Args:
            task_id: Unique task identifier
            error: Error message
        """
        if self.event_bus:
            await self.event_bus.publish(
                f"task.failed.{task_id}",
                {
                    "task_id": task_id,
                    "agent": self.agent_name,
                    "error": error,
                },
            )

        self.logger.error("task_failed", task_id=task_id, error=error)

    @abstractmethod
    async def process_task(self, task_id: str, params: dict[str, Any]) -> dict[str, Any]:
        """
        Process a task assigned to this agent.

        Must be implemented by all agent subclasses.

        Args:
            task_id: Unique task identifier
            params: Task parameters specific to agent type

        Returns:
            Task result dictionary
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.agent_name}')>"
