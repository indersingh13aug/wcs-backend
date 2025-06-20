FROM python:3.11-slim

# Install dependencies
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
    curl

# Set workdir
WORKDIR /app

# Copy code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
