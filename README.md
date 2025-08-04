# Response Monitor Django Project

A Django application with middleware that monitors and records API response times in Redis.

## Features

- Response time monitoring middleware
- Redis-based response time storage

## Prerequisites

- Python 3.8+
- Redis Server
- uv for dependency management

## Installation

### 1. Install UV (if not already installed)

```bash
# macOS
brew install uv

# Or with pip
pip install uv
```

### 2. Clone and Setup Project

```bash
git clone https://github.com/baharaz78/response_monitor.git
cd response_monitor
```

### 3. Create Virtual Environment and Install Dependencies

```bash
# Create virtual environment
uv venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
uv add django redis

uv sync
```

## Configuration

```python
# Redis Configuration
RESPONSE_MONITOR_REDIS = {
    'HOST': 'localhost',
    'PORT': 6379,
    'PASSWORD': None,
    'DB': 1,
    'MAX_HISTORY': 100,
    'EXPIRE_SECONDS': 24 * 3600,
}
```

### Database Setup

```bash
uv run python manage.py migrate
```

## Usage

### Start Development Server

```bash
uv run python manage.py runserver
```
