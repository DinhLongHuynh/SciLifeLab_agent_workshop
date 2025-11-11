# Dockerfile for running the workshop
from ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install -y \
    wget build-essential \
    python3-venv \
    python3-tk \
    zlib1g-dev \
    libssl-dev \
    libsqlite3-dev \
    libbz2-dev \
    libncurses-dev \
    libjpeg-dev \
    libffi-dev \
    liblzma-dev

# Build python 3.14
WORKDIR /opt/python3.14
RUN wget https://www.python.org/ftp/python/3.14.0/Python-3.14.0.tgz  && \
    gunzip Python-3.14.0.tgz && \
    tar -xf Python-3.14.0.tar
WORKDIR /opt/python3.14/Python-3.14.0
RUN ./configure && \
    make -j 12 && \
    make install

# Install python deps
COPY requirements.txt /
RUN python3.14 -m venv /opt/pyenv3.14 && \
    . /opt/pyenv3.14/bin/activate && \
    pip3 install --upgrade pip && \
    pip3 install -r /requirements.txt

# Add jupyter lab config
COPY jupyter_lab_config.py /

# Setup entrypoint for container and point it to source mountpoint
WORKDIR /
COPY <<EOF /entrypoint.bash
#!/bin/bash
set -x
set -e
. /opt/pyenv3.14/bin/activate
python3 -m jupyter lab --config /jupyter_lab_config.py /repo
EOF
RUN chmod +x /entrypoint.bash
ENTRYPOINT ["/entrypoint.bash"]