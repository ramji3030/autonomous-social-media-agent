# TROUBLESHOOTING.md - Common Issues and Solutions

## Installation Issues

### 1. Python Version Compatibility Error

**Problem:**
```
Error: Python 3.9+ is required
```

**Solution:**
Check your Python version:
```bash
python --version
```

If you have an older version, install Python 3.9+:
- macOS: `brew install python@3.9`
- Ubuntu: `apt-get install python3.9`
- Windows: Download from [python.org](https://python.org)

---

### 2. Virtual Environment Not Activating

**Problem:**
```
Virtual environment not found or not activated
```

**Solution:**
```bash
# Create fresh virtual environment
rm -rf venv
python -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows
```

---

### 3. Dependency Installation Fails

**Problem:**
```
Error: pip install fails with version conflict
```

**Solution:**
```bash
# Update pip
pip install --upgrade pip

# Clear cache
pip cache purge

# Install requirements with verbose output
pip install -r requirements.txt -v
```

---

## Configuration Issues

### 1. Missing API Keys

**Problem:**
```
ConfigurationError: API keys not found
```

**Solution:**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
vim .env

# Verify keys are set
echo $OPENAI_API_KEY
```

---

### 2. Invalid Configuration Format

**Problem:**
```
Error: YAML parsing error in config file
```

**Solution:**
1. Check config.py for proper syntax
2. Ensure proper indentation (use spaces, not tabs)
3. Validate JSON/YAML format online
4. Check for special characters

---

### 3. Platform Credentials Invalid

**Problem:**
```
AuthenticationError: Invalid credentials for platform
```

**Solution:**
1. Verify API credentials are correct
2. Check credential expiration date
3. Regenerate tokens if needed
4. Ensure correct platform in config

```python
PLATFORMS = {
    'twitter': {'enabled': True, 'api_key': 'your-valid-key'},
    # Verify each platform has valid credentials
}
```

---

## Runtime Issues

### 1. Agent Not Starting

**Problem:**
```
OrchestrationError: Failed to initialize orchestrator
```

**Solution:**
1. Check agent configuration
2. Verify all dependencies installed
3. Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

4. Check agent logs:
```bash
tail -f logs/agent.log
```

---

### 2. Timeout Errors

**Problem:**
```
TimeoutError: Agent execution timed out
```

**Solution:**
1. Increase timeout in config.py:
```python
TIMEOUT_SECONDS = 600  # Increase from default
```

2. Check network connection
3. Reduce batch size:
```python
BATCH_SIZE = 3  # Reduce from 5
```

4. Monitor system resources (CPU, RAM, network)

---

### 3. Memory Leaks

**Problem:**
```
MemoryError: Out of memory
```

**Solution:**
1. Reduce batch size
2. Clear cache periodically:
```python
from utils import clear_cache
clear_cache()
```

3. Monitor memory usage:
```bash
watch -n 1 'ps aux | grep python'
```

4. Profile memory:
```python
import tracemalloc
tracemalloc.start()
# ... run code ...
tracemalloc.stop()
```

---

### 4. API Rate Limiting

**Problem:**
```
RateLimitError: Too many requests to API
```

**Solution:**
1. Reduce batch size
2. Implement exponential backoff:
```python
import time
for attempt in range(3):
    try:
        result = api_call()
        break
    except RateLimitError:
        wait_time = 2 ** attempt
        time.sleep(wait_time)
```

3. Enable result caching:
```python
@cache_result(ttl=3600)
def get_trends():
    pass
```

---

## Content Generation Issues

### 1. Poor Quality Content

**Problem:**
```
Generated content is low quality or irrelevant
```

**Solution:**
1. Adjust temperature parameter:
```python
'content_generator': {
    'temperature': 0.7,  # Lower = more focused
    'top_p': 0.9        # Adjust diversity
}
```

2. Use better prompts
3. Add brand guidelines to system prompt
4. Test with different models

---

### 2. Platform-Specific Formatting Issues

**Problem:**
```
Content exceeds platform character limits
```

**Solution:**
1. Check platform limits:
```python
PLATFORM_LIMITS = {
    'twitter': 280,
    'linkedin': 3000,
    'instagram': 2200,
    'tiktok': 150  # Caption limit
}
```

2. Implement truncation:
```python
content = truncate_text(content, max_length=280)
```

---

### 3. Brand Voice Not Consistent

**Problem:**
```
Generated content doesn't match brand voice
```

**Solution:**
1. Update brand guidelines in config
2. Fine-tune system prompt
3. Add brand examples to context
4. Test voice adaptation:

```python
content = content_gen.generate_for_platform(
    topic='AI',
    platform='twitter',
    voice_tone='professional'  # Verify tone
)
```

---

## Engagement Tracking Issues

### 1. Metrics Not Updating

**Problem:**
```
Engagement metrics showing stale data
```

**Solution:**
1. Clear cache
2. Verify API connections
3. Check update frequency:
```python
'engagement_tracker': {
    'update_frequency': 300,  # Reduce interval
}
```

4. Manually refresh:
```python
tracker.refresh_metrics()
```

---

### 2. Missing Platform Data

**Problem:**
```
Metrics incomplete for certain platforms
```

**Solution:**
1. Verify platform is enabled in config
2. Check platform API access
3. Ensure credentials are valid
4. Check platform-specific rate limits

---

## Logging and Debugging

### Enable Debug Mode

```python
import logging
from utils import setup_logging

setup_logging(level=logging.DEBUG, file='logs/debug.log')
```

### Check Log Files

```bash
# View all logs
tail -f logs/agent.log

# Search for errors
grep ERROR logs/agent.log

# Real-time monitoring
watch -n 1 'tail -20 logs/agent.log'
```

### Enable Verbose Output

```bash
export PYTHONUNBUFFERED=1
python -u main.py
```

---

## Performance Optimization

### 1. Slow Content Generation

**Solution:**
1. Use faster models (GPT-3.5 instead of GPT-4)
2. Reduce max_tokens
3. Enable batching
4. Cache results

### 2. High Resource Usage

**Solution:**
1. Reduce batch size
2. Enable garbage collection
3. Use async processing
4. Monitor with `htop`

### 3. Network Issues

**Solution:**
1. Check connection: `ping google.com`
2. Check DNS: `nslookup api.openai.com`
3. Test API connectivity
4. Implement retry logic

---

## Getting Help

1. Check [USAGE.md](USAGE.md) for configuration examples
2. Review [API_REFERENCE.md](API_REFERENCE.md) for component details
3. Check application logs in `logs/` directory
4. Enable debug logging for detailed information
5. Create GitHub issue with error logs and config (without sensitive data)

---

## Quick Diagnostics

```bash
#!/bin/bash
# Run diagnostics

echo "Python version:"
python --version

echo "\nVirtual environment:"
echo $VIRTUAL_ENV

echo "\nInstalled packages:"
pip list | grep -E "langgraph|openai|anthropic"

echo "\nEnvironment variables:"
env | grep -E "API_KEY|TOKEN"

echo "\nDisk space:"
df -h

echo "\nMemory:"
free -h
```
