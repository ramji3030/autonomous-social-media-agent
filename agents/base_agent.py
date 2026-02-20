"""Base agent class for all autonomous agents.

This module defines the abstract base class that all agents inherit from.
It provides the core interface for agent execution, state management,
and LLM integration.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from datetime import datetime
import json


class BaseAgent(ABC):
    """Abstract base class for all autonomous agents.
    
    Attributes:
        name: Unique identifier for the agent
        description: Human-readable description of agent purpose
        config: Configuration dictionary for the agent
        memory: Message history and state tracking
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the base agent.
        
        Args:
            name: Unique agent identifier
            description: Agent purpose description
            config: Optional configuration dictionary
        """
        self.name = name
        self.description = description
        self.config = config or {}
        self.memory: List[Dict[str, Any]] = []
        self.created_at = datetime.now().isoformat()
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent with given input.
        
        Args:
            input_data: Input parameters for agent execution
            
        Returns:
            Dictionary containing agent output and metadata
        """
        pass
    
    @abstractmethod
    async def process(self, message: str) -> str:
        """Process a single message through the agent.
        
        Args:
            message: Input message to process
            
        Returns:
            Processed output from the agent
        """
        pass
    
    def add_to_memory(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add message to agent memory.
        
        Args:
            role: Role of the message sender (user/assistant)
            content: Message content
            metadata: Optional additional metadata
        """
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "metadata": metadata or {},
        }
        self.memory.append(memory_entry)
    
    def get_memory(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retrieve agent memory.
        
        Args:
            limit: Maximum number of recent messages to return
            
        Returns:
            List of memory entries
        """
        if limit:
            return self.memory[-limit:]
        return self.memory
    
    def clear_memory(self) -> None:
        """Clear the agent memory."""
        self.memory = []
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current agent state.
        
        Returns:
            Dictionary containing agent state
        """
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "memory_size": len(self.memory),
            "config": self.config,
        }
    
    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"{self.__class__.__name__}(name={self.name}, description={self.description})"
