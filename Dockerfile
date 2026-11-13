FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /home/speckle

# Copy package metadata and the modules required by setuptools before installing.
COPY pyproject.toml README.md LICENSE ./
COPY main.py flatten.py audit.py ./
RUN python -m pip install --upgrade pip \
    && python -m pip install .

# Include the remaining function files, tests, assets, and Speckle configuration.
COPY . ./
