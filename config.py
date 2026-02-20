"""Configuration settings for autonomous social media agent.

Manages LangGraph settings, API configurations, and agent parameters.
"""

import os
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class LangGraphConfig:
    """LangGraph configuration settings."""
    
    # Graph settings
    max_iterations: int = 10
    timeout: int = 300  # seconds
    checkpoint_interval: int = 5
    enable_streaming: bool = True
    
    # Node configuration
    node_timeout: int = 60  # seconds
    retry_policy: str = "exponential_backoff"
    max_retries: int = 3


@dataclass
class AgentConfig:
    """Configuration for individual agents."""
    
    # Agent settings
    name: str
    enabled: bool = True
    parallel_execution: bool = False
    
    # Resource limits
    max_memory_mb: int = 512
    max_cpu_percent: float = 80.0
    
    # Model settings
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2048


@dataclass
class PlatformConfig:
    """Configuration for social media platforms."""
    
    name: str  # twitter, tiktok, instagram, etc.
    enabled: bool = True
    
    # Rate limiting
    requests_per_minute: int = 60
    batch_size: int = 10
    
    # Content settings
    max_content_length: int = 280  # twitter default
    supported_media: list = field(default_factory=lambda: ["text", "image"])
    hashtag_limit: int = 10


class Config:
    """Main configuration class for the entire system."""
    
    def __init__(self):
        """Initialize configuration from environment and defaults."""
        # LangGraph configuration
        self.langgraph = LangGraphConfig(
            max_iterations=int(os.getenv("LANGGRAPH_MAX_ITERATIONS", "10")),
            timeout=int(os.getenv("LANGGRAPH_TIMEOUT", "300")),
        )
        
        # Agent configurations
        self.agents = {
            "trend_monitor": AgentConfig(
                name="TrendMonitor",
                enabled=True,
            ),
            "content_generator": AgentConfig(
                name="ContentGenerator",
                enabled=True,
                temperature=0.8,  # Higher creativity
            ),
            "engagement_tracker": AgentConfig(
                name="EngagementTracker",
                enabled=True,
                temperature=0.3,  # Lower randomness for metrics
            ),
        }
        
        # Platform configurations
        self.platforms = {
            "twitter": PlatformConfig(
                name="twitter",
                max_content_length=280,
            ),
            "tiktok": PlatformConfig(
                name="tiktok",
                max_content_length=2200,
                supported_media=["text", "video", "image"],
            ),
            "instagram": PlatformConfig(
                name="instagram",
                max_content_length=2200,
                supported_media=["text", "image", "carousel"],
            ),
        }
        
        # Brand voice settings
        self.brand_voice = {
            "tone": os.getenv("BRAND_TONE", "professional"),
            "style": os.getenv("BRAND_STYLE", "conversational"),
            "values": os.getenv(
                "BRAND_VALUES",
                "innovation, transparency, excellence",
            ),
        }
        
        # API keys and credentials
        self.api_keys = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "twitter": os.getenv("TWITTER_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
        }
        
        # Monitoring and logging
        self.monitoring = {
            "enabled": os.getenv("MONITORING_ENABLED", "true").lower() == "true",
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "metrics_collection": os.getenv("METRICS_ENABLED", "true").lower() == "true",
        }
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Get configuration for a specific agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            AgentConfig or None
        """
        return self.agents.get(agent_name)
    
    def get_platform_config(self, platform_name: str) -> Optional[PlatformConfig]:
        """Get configuration for a specific platform.
        
        Args:
            platform_name: Name of the platform
            
        Returns:
            PlatformConfig or None
        """
        return self.platforms.get(platform_name)
    
    def validate(self) -> bool:
        """Validate all configuration settings.
        
        Returns:
            True if valid, False otherwise
        """
        # Check required API keys
        if not self.api_keys.get("openai"):
            print("Warning: OPENAI_API_KEY not set")
        
        # Validate agent configurations
        for agent_name, config in self.agents.items():
            if config.temperature < 0 or config.temperature > 2:
                print(f"Invalid temperature for {agent_name}")
                return False
        
        return True


# Global config instance
config = Config()
