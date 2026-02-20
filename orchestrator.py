"""Main orchestrator for autonomous social media agent system.

This module implements the LangGraph-based orchestration system that
coordinates all agents and manages their execution flow.
"""

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime
import json

from agents import (
    TrendMonitorAgent,
    ContentGeneratorAgent,
    EngagementTrackerAgent,
)


class AgentOrchestrator:
    """Main orchestrator for managing multi-agent social media system.
    
    Orchestrates the workflow between trend monitoring, content generation,
    and engagement tracking agents using LangGraph principles.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the orchestrator and all agents.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.agents = {}
        self.execution_history: List[Dict[str, Any]] = []
        self.state = {
            "trends": [],
            "generated_content": [],
            "engagement_metrics": {},
        }
        
        # Initialize agents
        self._initialize_agents()
    
    def _initialize_agents(self) -> None:
        """Initialize all agent instances."""
        self.agents["trend_monitor"] = TrendMonitorAgent(
            platform=self.config.get("platform", "twitter")
        )
        self.agents["content_generator"] = ContentGeneratorAgent(
            platform=self.config.get("platform", "twitter"),
            brand_voice=self.config.get("brand_voice"),
        )
        self.agents["engagement_tracker"] = EngagementTrackerAgent(
            platform=self.config.get("platform", "twitter")
        )
    
    async def execute_workflow(self, input_params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete social media agent workflow.
        
        Workflow:
        1. Monitor trends
        2. Generate content based on trends
        3. Track engagement metrics
        4. Adapt strategy based on performance
        
        Args:
            input_params: Workflow input parameters
            
        Returns:
            Complete workflow execution result
        """
        workflow_id = datetime.now().isoformat()
        
        try:
            # Step 1: Monitor trends
            print("[Step 1] Monitoring trends...")
            trend_result = await self.agents["trend_monitor"].execute(
                {"query": input_params.get("query", "")}
            )
            self.state["trends"] = trend_result.get("trends", [])
            
            # Step 2: Generate content based on trends
            print("[Step 2] Generating content...")
            topic = input_params.get("topic") or (
                trend_result.get("trends", [{}])[0].get("topic", "")
            )
            
            content_result = await self.agents["content_generator"].execute(
                {
                    "topic": topic,
                    "tone": input_params.get("tone"),
                    "hashtags": input_params.get("hashtags", []),
                }
            )
            self.state["generated_content"].append(content_result)
            
            # Step 3: Track engagement (simulate post and collect metrics)
            print("[Step 3] Tracking engagement...")
            engagement_result = await self.agents["engagement_tracker"].execute(
                {"metrics_data": input_params.get("metrics", {})}
            )
            self.state["engagement_metrics"] = engagement_result.get("analysis", {})
            
            # Compile results
            result = {
                "workflow_id": workflow_id,
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "trends": self.state["trends"],
                "content": content_result.get("content"),
                "engagement_analysis": self.state["engagement_metrics"],
                "recommendations": engagement_result.get("recommendations", []),
            }
            
            self.execution_history.append(result)
            return result
            
        except Exception as e:
            return {
                "workflow_id": workflow_id,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
    
    async def continuous_monitoring(self, interval_seconds: int = 3600) -> None:
        """Run continuous monitoring of trends and content generation.
        
        Args:
            interval_seconds: Interval between monitoring cycles
        """
        print(f"Starting continuous monitoring (interval: {interval_seconds}s)")
        
        while True:
            try:
                result = await self.execute_workflow({"query": "trending topics"})
                print(f"[{result['timestamp']}] Monitoring cycle complete")
            except Exception as e:
                print(f"Error in monitoring cycle: {e}")
            
            await asyncio.sleep(interval_seconds)
    
    def get_agent(self, agent_name: str):
        """Get a specific agent by name.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Agent instance or None
        """
        return self.agents.get(agent_name)
    
    def get_all_agents(self) -> Dict[str, Any]:
        """Get all initialized agents.
        
        Returns:
            Dictionary of agents
        """
        return self.agents
    
    def get_execution_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get workflow execution history.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of execution records
        """
        if limit:
            return self.execution_history[-limit:]
        return self.execution_history
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get the current orchestrator state.
        
        Returns:
            Current state dictionary
        """
        return {
            "state": self.state,
            "agents_initialized": list(self.agents.keys()),
            "execution_count": len(self.execution_history),
            "last_execution": self.execution_history[-1] if self.execution_history else None,
        }
    
    def reset_state(self) -> None:
        """Reset the orchestrator state."""
        self.state = {
            "trends": [],
            "generated_content": [],
            "engagement_metrics": {},
        }
        print("Orchestrator state reset")


if __name__ == "__main__":
    # Example usage
    async def main():
        orchestrator = AgentOrchestrator(
            config={
                "platform": "twitter",
                "brand_voice": {
                    "tone": "professional",
                    "style": "conversational",
                },
            }
        )
        
        result = await orchestrator.execute_workflow(
            {
                "query": "AI and technology trends",
                "topic": "Artificial Intelligence Innovation",
                "tone": "professional",
                "hashtags": ["#AI", "#Innovation"],
            }
        )
        
        print(json.dumps(result, indent=2))
    
    asyncio.run(main())
