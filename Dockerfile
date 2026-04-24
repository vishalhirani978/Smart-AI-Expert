FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages directly
RUN pip install --no-cache-dir \
    flask \
    groq \
    google-generativeai \
    cohere \
    openai \
    requests \
    python-dotenv \
    gunicorn

# Copy all project files
COPY . .

# Expose port
EXPOSE 7860

# Set environment
ENV PORT=7860

# Start app
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "120", "--workers", "1", "app:app"]