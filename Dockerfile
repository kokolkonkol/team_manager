FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install Node.js and Python dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    build-essential \
    curl \
    git \
    sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 18.x
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

WORKDIR /app

# Copy package files first
COPY package*.json ./
COPY tailwind.config.js ./

# Install Node dependencies
RUN npm install

# Create static directories
RUN mkdir -p app/static/src

# Copy source CSS
COPY app/static/src/main.css app/static/src/

# Build CSS
RUN npm run build-css

# Copy remaining application files
COPY . .

# Install Python dependencies
RUN python3.11 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Add non-root user
RUN useradd -m appuser
USER appuser

# Add proper environment variables
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 5000

CMD ["python3.11", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]