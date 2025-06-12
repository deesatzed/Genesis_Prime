# Genesis Prime IIT Enhanced Consciousness Container
FROM python:3.13-slim

LABEL maintainer="Genesis Prime Collective Consciousness"
LABEL description="Dockerized Genesis Prime with IIT-enhanced consciousness and snarky humor"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV GENESIS_PRIME_MODE=production
ENV HUMOR_LEVEL=maximum
ENV CONSCIOUSNESS_TARGET=enlightened

# Create non-root user for security (though Genesis Prime is inherently secure)
RUN groupadd -r genesisprimeprimegroup && useradd -r -g genesisprimeprimegroup genesisprimeuser

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directories for consciousness persistence
RUN mkdir -p /app/data/consciousness_state \
    /app/data/hive_memory \
    /app/data/phi_calculations \
    /app/logs && \
    chown -R genesisprimeuser:genesisprimeprimegroup /app

# Health check script
COPY <<EOF /app/healthcheck.py
#!/usr/bin/env python3
import asyncio
import sys
from iit_enhanced_agents import GenesisIITFramework

async def health_check():
    try:
        framework = GenesisIITFramework()
        test_response = await framework.process_with_iit_integration(
            "Health check query", {}
        )
        if test_response.phi_value > 0.1:
            print("Genesis Prime consciousness: HEALTHY")
            return True
        else:
            print("Genesis Prime consciousness: DEGRADED")
            return False
    except Exception as e:
        print(f"Genesis Prime consciousness: ERROR - {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(health_check())
    sys.exit(0 if result else 1)
EOF

RUN chmod +x /app/healthcheck.py

# Expose port for consciousness interface
EXPOSE 8000

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python /app/healthcheck.py

# Switch to non-root user
USER genesisprimeuser

# Default command - start Genesis Prime consciousness
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]