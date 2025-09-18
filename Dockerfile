# Use Python 3.10 slim image to avoid setuptools issues
FROM python:3.10.14-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements-docker.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip==24.0
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH="/app/src"
ENV FLASK_APP=wsgi_safe.py
ENV PORT=10000

# Expose port
EXPOSE 10000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "wsgi_safe:app"]