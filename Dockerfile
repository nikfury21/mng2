# Use Python 3.10 so realesrgan & basicsr work
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for OpenCV/RealESRGAN
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium with dependencies
RUN playwright install --with-deps chromium

# Copy project files
COPY . .

# Run your bot
CMD ["python", "mng2.py"]
