FROM python:3.13-slim

# Prepare user and ports
RUN useradd --create-home --shell /bin/bash appuser
EXPOSE 8000

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app.py .

# Run application as non-root user
USER appuser
CMD ["fastapi", "run", "app.py"]
