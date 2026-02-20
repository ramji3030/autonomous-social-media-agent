# USAGE.md - Autonomous Social Media Agent

## Quick Start Guide

### Basic Setup

```bash
# Clone the repository
git clone https://github.com/ramji3030/autonomous-social-media-agent.git
cd autonomous-social-media-agent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Running the Agent

#### 1. Start the Orchestrator

```python
from orchestrator import SocialMediaOrchestrator

# Initialize the orchestrator
orchestrator = SocialMediaOrchestrator()

# Run the agent
orchestrator.run()
```

#### 2. Configure Platforms

Edit `config.py` to specify which social media platforms to manage:

```python
PLATFORMS = {
    'twitter': {'enabled': True, 'api_key': 'your-key'},
    'linkedin': {'enabled': True, 'api_key': 'your-key'},
    'instagram': {'enabled': True, 'api_key': 'your-key'},
    'tiktok': {'enabled': True, 'api_key': 'your-key'}
}
```

#### 3. Monitor Trends and Generate Content

The agent automatically:
- Monitors social media trends via TrendMonitor
- Generates brand-consistent content via ContentGenerator
- Tracks engagement metrics via EngagementTracker
- Adapts voice and tone per platform

### Advanced Usage

#### Custom Agent Configuration

Modify agent behavior by extending base classes:

```python
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def execute(self, input_data):
        # Your custom logic here
        pass
```

#### Multi-Agent Orchestration

Control multiple agents through the orchestrator:

```python
orchestrator.agents['trend_monitor'].run()
orchestrator.agents['content_generator'].run()
orchestrator.agents['engagement_tracker'].run()
```

#### Logging and Debugging

Enable detailed logging:

```python
import logging
from utils import setup_logging

setup_logging(level=logging.DEBUG)
```

## Common Use Cases

### 1. Content Generation Workflow

```python
# Generate content for the week
trends = orchestrator.agents['trend_monitor'].get_trending_topics()
content = orchestrator.agents['content_generator'].generate_posts(trends)
orchestrator.publish_content(content)
```

### 2. Engagement Analysis

```python
# Analyze engagement metrics
metrics = orchestrator.agents['engagement_tracker'].analyze_metrics()
print(f"Average engagement: {metrics['average_engagement']}%")
```

### 3. Voice Adaptation per Platform

```python
# Generate platform-specific content
for platform in ['twitter', 'linkedin', 'instagram']:
    content = orchestrator.agents['content_generator'].generate_for_platform(
        topic='AI',
        platform=platform,
        voice_tone='professional'  # Adapts to platform
    )
```

## Configuration Options

### Environment Variables

```bash
# API Keys
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
TWITTER_API_KEY=your-key
LINKEDIN_API_KEY=your-key

# Agent Settings
MAX_ITERATIONS=10
TIMEOUT_SECONDS=300
BATCH_SIZE=5

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/agent.log
```

### Agent Parameters

```python
config = {
    'trend_monitor': {
        'update_frequency': 3600,  # seconds
        'max_topics': 10,
        'language': 'en'
    },
    'content_generator': {
        'model': 'gpt-4',
        'max_tokens': 500,
        'temperature': 0.7
    },
    'engagement_tracker': {
        'analysis_window': 7,  # days
        'metrics': ['likes', 'comments', 'shares']
    }
}
```

## API Endpoints (if deployed as service)

### GET /status
Check agent health status

### POST /generate-content
Request content generation

```json
{
  "topic": "AI in 2024",
  "platforms": ["twitter", "linkedin"],
  "tone": "informative"
}
```

### GET /metrics
Retrieve engagement metrics

## Performance Tips

1. **Batch Processing**: Generate multiple posts at once to optimize API calls
2. **Caching**: Trends are cached for 1 hour to reduce API calls
3. **Async Operations**: Use async/await for parallel processing
4. **Rate Limiting**: Respect API rate limits by adjusting batch sizes

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

## Next Steps

- Read [API_REFERENCE.md](API_REFERENCE.md) for detailed API documentation
- Review [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md) for planned features
- Check [INSTALLATION.md](INSTALLATION.md) for advanced setup options
