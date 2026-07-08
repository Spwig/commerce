# Build stage
FROM python:3.12-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Runtime stage
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies including Postfix for built-in SMTP server
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    ffmpeg \
    libmagic1 \
    libjpeg62-turbo \
    libpng16-16 \
    libwebp7 \
    libwebpmux3 \
    libwebpdemux2 \
    postfix \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configure Postfix for localhost relay (built-in SMTP server)
RUN postconf -e "inet_interfaces = localhost" && \
    postconf -e "mynetworks = 127.0.0.0/8 [::1]/128" && \
    postconf -e "mydestination = localhost" && \
    postconf -e "relayhost =" && \
    postconf -e "mailbox_size_limit = 0" && \
    postconf -e "recipient_delimiter = +" && \
    postconf -e "inet_protocols = ipv4"

# Create non-root user
RUN groupadd -r spwig && useradd -r -g spwig spwig

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy application code (includes pre-baked staticfiles/ when present in build context)
COPY --chown=spwig:spwig . .

# Create necessary directories
RUN mkdir -p /app/static /app/media /app/logs /app/components_data /var/run/smtp_server /opt/shop-platform/license && \
    chown -R spwig:spwig /app /var/run/smtp_server /opt/shop-platform

# Create supervisor configuration directory
RUN mkdir -p /etc/supervisor/conf.d

# Copy supervisor configurations
COPY docker/supervisord.conf /etc/supervisor/supervisord.conf
COPY docker/supervisor-postfix.conf /etc/supervisor/conf.d/postfix.conf
COPY docker/supervisor-spwig.conf /etc/supervisor/conf.d/spwig.conf
COPY docker/supervisor-smtp-server.conf /etc/supervisor/conf.d/smtp-server.conf

# Expose ports (Spwig app and SMTP server)
EXPOSE 8000 2525

# Copy scripts
COPY --chown=spwig:spwig docker/setup-component-volume.sh /docker/setup-component-volume.sh
COPY --chown=spwig:spwig docker-entrypoint.sh /
RUN chmod +x /docker/setup-component-volume.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]