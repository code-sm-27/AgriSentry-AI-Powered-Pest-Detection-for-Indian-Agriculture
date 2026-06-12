FROM python:3.10-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/backend/

# Expose port (Hugging Face Spaces requires port 7860)
EXPOSE 7860

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
