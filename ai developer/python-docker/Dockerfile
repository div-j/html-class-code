FROM python:3.12-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .

# Expose port 5000
EXPOSE 5000

# Run FastAPI using Uvicorn ASGI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]