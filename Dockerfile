FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install uv for reproducible, lockfile-based dependency installs.
RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

# Install the locked project dependencies into the image.
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8501

# Default to the Streamlit app; override at runtime for CLI entry points.
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
