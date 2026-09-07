FROM python:3.11-slim

# Create a non-root user with UID 1000 expected by Hugging Face Spaces
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Install system dependencies
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
USER user

# Install Python dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=user . .

# Expose ports (7860 is the primary port exposed by Hugging Face Spaces)
EXPOSE 7860 8000

# Start both FastAPI/LangServe (backend) and Gradio (frontend)
CMD ["sh", "-c", "python -m app.server & python frontend/app.py"]