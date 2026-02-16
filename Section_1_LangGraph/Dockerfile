FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    JUPYTER_PORT=8888

WORKDIR /workspace

# Native libs commonly needed by scientific Python wheels (including rdkit).
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    git \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

COPY . /workspace

EXPOSE 8888

# Disable Jupyter auth for local workshop convenience.
CMD ["sh", "-c", "jupyter lab --ip=0.0.0.0 --port=${JUPYTER_PORT} --no-browser --allow-root --ServerApp.token='' --ServerApp.password='' --ServerApp.allow_origin='*'"]
