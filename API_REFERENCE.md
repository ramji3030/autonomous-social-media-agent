# API_REFERENCE.md - Autonomous Social Media Agent

## Core Components

### 1. SocialMediaOrchestrator

Main orchestrator managing all agents and workflow coordination.

#### Class: `SocialMediaOrchestrator`

```python
from orchestrator import SocialMediaOrchestrator

orchestrator = SocialMediaOrchestrator(config=None)
```

**Methods:**

#### `__init__(config: Optional[Dict] = None) -> None`
Initialize the orchestrator with configuration.

**Parameters:**
- `config` (Dict, optional): Configuration dictionary for agents and settings

**Returns:** None

---

#### `run() -> None`
Start the main orchestration loop.

**Returns:** None

**Raises:** `OrchestrationError` if initialization fails

---

#### `agents` Property
Access individual agents.

```python
orchestrator.agents['trend_monitor']
orchestrator.agents['content_generator']
orchestrator.agents['engagement_tracker']
```

**Available Agents:**
- `trend_monitor`: TrendMonitor agent
- `content_generator`: ContentGenerator agent  
- `engagement_tracker`: EngagementTracker agent

---

### 2. BaseAgent

Base class for all agents.

#### Class: `BaseAgent`

```python
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    pass
```

**Methods:**

#### `execute(input_data: Dict) -> Dict`
Execute agent logic (abstract method).

**Parameters:**
- `input_data` (Dict): Input data for the agent

**Returns:** Dict containing agent output

**Raises:** `NotImplementedError` if not overridden

---

#### `validate_input(input_data: Dict) -> bool`
Validate input data format.

**Parameters:**
- `input_data` (Dict): Input to validate

**Returns:** bool indicating validity

---

### 3. TrendMonitor

Monitors social media trends and topics.

#### Class: `TrendMonitor(BaseAgent)`

```python
from agents.trend_monitor import TrendMonitor

trend_monitor = TrendMonitor(config=None)
```

**Methods:**

#### `get_trending_topics(limit: int = 10, language: str = 'en') -> List[Dict]`
Fetch current trending topics.

**Parameters:**
- `limit` (int): Maximum number of trends to return (default: 10)
- `language` (str): Language code (default: 'en')

**Returns:** List of dictionaries containing trend data

```python
trends = trend_monitor.get_trending_topics(limit=5, language='en')
# Output: [
#   {'topic': 'AI', 'volume': 50000, 'momentum': 'rising'},
#   {'topic': 'Web3', 'volume': 45000, 'momentum': 'stable'}
# ]
```

---

#### `analyze_trend(topic: str) -> Dict`
Analyze a specific trend.

**Parameters:**
- `topic` (str): Topic to analyze

**Returns:** Dictionary with trend analysis

```python
analysis = trend_monitor.analyze_trend('AI')
# Output: {
#   'sentiment': 'positive',
#   'volume': 50000,
#   'momentum': 'rising',
#   'related_topics': ['machine-learning', 'deep-learning']
# }
```

---

### 4. ContentGenerator

Generates brand-consistent social media content.

#### Class: `ContentGenerator(BaseAgent)`

```python
from agents.content_generator import ContentGenerator

content_gen = ContentGenerator(brand_voice='professional')
```

**Methods:**

#### `generate_posts(topics: List[str], platform: str = 'twitter', count: int = 1) -> List[Dict]`
Generate content for specified topics.

**Parameters:**
- `topics` (List[str]): List of topics for content generation
- `platform` (str): Target platform (twitter, linkedin, instagram, tiktok)
- `count` (int): Number of posts per topic (default: 1)

**Returns:** List of generated posts

```python
posts = content_gen.generate_posts(
    topics=['AI', 'Web3'],
    platform='twitter',
    count=1
)
# Output: [
#   {'content': 'Tweet about AI...', 'hashtags': ['#AI', '#Tech']},
#   {'content': 'Tweet about Web3...', 'hashtags': ['#Web3', '#Crypto']}
# ]
```

---

#### `generate_for_platform(topic: str, platform: str, voice_tone: str) -> Dict`
Generate platform-specific content with adapted tone.

**Parameters:**
- `topic` (str): Content topic
- `platform` (str): Target platform
- `voice_tone` (str): Tone (professional, casual, technical, creative)

**Returns:** Dictionary with platform-optimized content

```python
content = content_gen.generate_for_platform(
    topic='Machine Learning',
    platform='linkedin',
    voice_tone='professional'
)
# Output: {
#   'content': 'Professional LinkedIn post about ML...',
#   'format': 'article',
#   'cta': 'Learn more...'
# }
```

---

### 5. EngagementTracker

Tracks and analyzes engagement metrics.

#### Class: `EngagementTracker(BaseAgent)`

```python
from agents.engagement_tracker import EngagementTracker

tracker = EngagementTracker()
```

**Methods:**

#### `analyze_metrics(time_window: int = 7) -> Dict`
Analyze engagement metrics.

**Parameters:**
- `time_window` (int): Number of days to analyze (default: 7)

**Returns:** Dictionary with engagement analysis

```python
metrics = tracker.analyze_metrics(time_window=7)
# Output: {
#   'total_engagements': 5000,
#   'average_engagement_rate': 4.5,
#   'top_content': [{'post_id': '123', 'engagement': 500}],
#   'audience_growth': 250
# }
```

---

#### `get_platform_stats(platform: str) -> Dict`
Get platform-specific engagement stats.

**Parameters:**
- `platform` (str): Platform name

**Returns:** Dictionary with platform stats

```python
stats = tracker.get_platform_stats('twitter')
# Output: {
#   'followers': 10000,
#   'engagement_rate': 5.2,
#   'reach': 50000,
#   'impressions': 100000
# }
```

---

## Configuration

### config.py

```python
# API Configuration
OPENAI_API_KEY = 'your-key'
ANTHROPIC_API_KEY = 'your-key'

# Platform Configuration
PLATFORMS = {
    'twitter': {'enabled': True, 'api_key': 'your-key'},
    'linkedin': {'enabled': True, 'api_key': 'your-key'},
    'instagram': {'enabled': True, 'api_key': 'your-key'},
    'tiktok': {'enabled': True, 'api_key': 'your-key'}
}

# Agent Configuration
AGENT_CONFIG = {
    'trend_monitor': {
        'update_frequency': 3600,
        'max_topics': 10,
        'language': 'en'
    },
    'content_generator': {
        'model': 'gpt-4',
        'max_tokens': 500,
        'temperature': 0.7
    },
    'engagement_tracker': {
        'analysis_window': 7,
        'metrics': ['likes', 'comments', 'shares']
    }
}
```

## Error Handling

### Common Exceptions

```python
from orchestrator import (
    OrchestrationError,
    AgentError,
    ConfigurationError
)

try:
    orchestrator.run()
except OrchestrationError as e:
    logger.error(f"Orchestration failed: {e}")
except AgentError as e:
    logger.error(f"Agent execution failed: {e}")
except ConfigurationError as e:
    logger.error(f"Configuration error: {e}")
```

## Utilities

### utils.py

```python
from utils import (
    setup_logging,
    format_output,
    validate_data,
    cache_result
)

# Setup logging
setup_logging(level=logging.DEBUG)

# Format output
formatted_data = format_output(data, format='json')

# Validate data
is_valid = validate_data(data, schema)

# Cache results
@cache_result(ttl=3600)
def get_trending_topics():
    pass
```

## Best Practices

1. **Error Handling**: Always wrap agent calls in try-catch blocks
2. **Logging**: Enable debug logging during development
3. **Rate Limiting**: Respect API rate limits with batch processing
4. **Caching**: Cache trends to reduce API calls
5. **Async Operations**: Use async/await for parallel processing
6. **Configuration**: Keep sensitive data in environment variables
