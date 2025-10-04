# Use latest Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies for pip and building packages if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd -r flaskuser && useradd -r -g flaskuser -s /bin/bash flaskuser

# Set working directory
WORKDIR /app

# Copy the application code
COPY app .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN chown -R flaskuser:flaskuser /app

USER flaskuser

EXPOSE 5001

CMD ["gunicorn", "-w", "1", "--threads", "100", "-b", "0.0.0.0:5001", "app:app"]
