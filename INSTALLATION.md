INSTALLATION.md# Installation Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git
- Virtual environment tool (venv or conda)

## Step 1: Clone the Repository

```bash
git clone https://github.com/ramji3030/autonomous-social-media-agent.git
cd autonomous-social-media-agent
```

## Step 2: Create Virtual Environment

### Using venv (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Using conda
```bash
conda create -n social-agent python=3.9
conda activate social-agent
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
TWITTER_API_KEY=your_twitter_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
BRAND_TONE=professional
BRAND_STYLE=conversational
BRAND_VALUES=innovation, transparency, excellence
```

## Step 5: Verify Installation

```bash
python -c "from orchestrator import AgentOrchestrator; print('Installation successful!')"
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'langgraph'`
**Solution**: Make sure you've activated your virtual environment and installed dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### Issue: `OPENAI_API_KEY not found`
**Solution**: Set up your `.env` file with the required API keys as shown in Step 4.

### Issue: Python version compatibility
**Solution**: Check your Python version:
```bash
python --version
```
Upgrade if needed to Python 3.9+

## Next Steps

After successful installation:
1. Read the [USAGE.md](USAGE.md) guide for basic usage
2. Check [API_REFERENCE.md](API_REFERENCE.md) for detailed API documentation
3. Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.9 | 3.10+ |
| RAM | 2GB | 8GB |
| Disk Space | 500MB | 2GB |
| Network | Stable internet (for API calls) | High-speed |

## Supported Platforms

- Linux (Ubuntu 20.04+, Debian 10+)
- macOS (10.14+)
- Windows 10/11
