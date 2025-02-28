# Base stage
FROM python:3.10-slim as base
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Install base dependencies including build essentials for uWSGI
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    postgresql-client \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install base Python dependencies
COPY requirements-base.txt .
RUN pip install --no-cache-dir -r requirements-base.txt \
    && rm -rf ~/.cache/pip/*

# ML stage
FROM base as ml
# Add user creation here
RUN adduser --disabled-password --no-create-home app

# Install ML dependencies
COPY requirements-ml.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-opencv \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements-ml.txt \
    && rm -rf ~/.cache/pip/*

# Create directories and set permissions
RUN mkdir -p /app /scripts /ml_models /vol/web/static /vol/web/media /vol/web/static/admin \
    && chmod -R 755 /ml_models \
    && chown -R app:app /vol/web/static /vol/web/media /vol/web/static/admin /app

# Copy scripts
COPY ./scripts /scripts
RUN chmod -R +x /scripts
ENV PATH="/scripts:$PATH"

# Final stage for backend
FROM base as backend
# Add user and setup directories for backend
RUN adduser --disabled-password --no-create-home app && \
    mkdir -p /app /scripts /vol/web/static /vol/web/media /vol/web/static/admin && \
    chown -R app:app /vol/web/static /vol/web/media /vol/web/static/admin /app

# Copy scripts
COPY ./scripts /scripts
RUN chmod -R +x /scripts
ENV PATH="/scripts:$PATH"

COPY --from=base /opt/venv /opt/venv
COPY . /app/
WORKDIR /app
RUN python manage.py collectstatic --noinput
USER app
EXPOSE 8000
CMD ["/app/entrypoint.sh"]
# Final stage for celery
FROM ml as celery
COPY --from=ml /opt/venv /opt/venv
COPY . /app/
WORKDIR /app
USER app
CMD ["celery", "-A", "trai", "worker", "--loglevel=info"]

# Final stage for migrate
FROM base as migrate
# Add user and setup directories for migrate
RUN adduser --disabled-password --no-create-home app && \
    mkdir -p /app /scripts /vol/web/static /vol/web/media /vol/web/static/admin && \
    chown -R app:app /vol/web/static /vol/web/media /vol/web/static/admin /app

COPY --from=base /opt/venv /opt/venv
COPY . /app/
WORKDIR /app
USER app
CMD ["python", "manage.py", "migrate"]

