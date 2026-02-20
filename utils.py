"""Utility functions for the autonomous social media agent.

Provides helpers for logging, data processing, and API integration.
"""

import json
from typing import Any, Dict
from datetime import datetime
import logging


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Set up logging configuration.
    
    Args:
        log_level: Logging level
        
    Returns:
        Configured logger
    """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


def serialize_data(data: Any) -> str:
    """Serialize data to JSON string.
    
    Args:
        data: Data to serialize
        
    Returns:
        JSON string
    """
    return json.dumps(data, default=str)


def deserialize_data(data_str: str) -> Dict[str, Any]:
    """Deserialize JSON string to data.
    
    Args:
        data_str: JSON string
        
    Returns:
        Deserialized data
    """
    return json.loads(data_str)


def format_timestamp() -> str:
    """Get formatted current timestamp.
    
    Returns:
        ISO format timestamp
    """
    return datetime.now().isoformat()


def calculate_engagement_rate(interactions: int, impressions: int) -> float:
    """Calculate engagement rate.
    
    Args:
        interactions: Number of interactions
        impressions: Number of impressions
        
    Returns:
        Engagement rate as decimal
    """
    if impressions == 0:
        return 0.0
    return interactions / impressions


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
