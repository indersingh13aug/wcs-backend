FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wkhtmltopdf \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    libjpeg62-turbo \
    libfreetype6 \
    libx11-6 \
    xfonts-75dpi \
    xfonts-base \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . /app
# COPY .env.production .env  
# default

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Start app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]