# Use Python 3.10 so realesrgan & basicsr work
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for OpenCV/RealESRGAN + Git + Playwright deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    git \
    wget \
    ca-certificates \
    fonts-unifont \
    fonts-ubuntu \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium (without --with-deps, since we added fonts manually)
RUN playwright install chromium

# Copy project files
COPY . .

# Run your bot (merged_runner.py is the entrypoint)
CMD ["python", "merged_runner.py"]

