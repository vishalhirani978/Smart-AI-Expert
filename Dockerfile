FROM python:3.11-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies including gunicorn explicitly
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy all project files
COPY . .

# Expose port
EXPOSE 7860

# Set environment
ENV PORT=7860

# Run with full path to gunicorn
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "120", "app:app"]