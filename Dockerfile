# Build phase
FROM python:3.9.19-slim-bullseye AS builder

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN \
    sed -i 's#http://deb.debian.org#https://mirrors.tuna.tsinghua.edu.cn#g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y libsndfile1

ENV PIP_DEFAULT_TIMEOUT=1000 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 

RUN pip install poetry \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

# Copy and install the dependencies
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi --no-root

# Copy the source code
COPY . .

# DO NOT USE MULTI PHASE FOR THIS. DUE TO THE INSTALLATION OF libsndfile1. 
# Runtime phase
# FROM python:3.9.19-slim-bullseye

# Set the working directory
#WORKDIR /app

# Copy the server binary and its dependencies from the builder image
#COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
#COPY --from=builder /app /app

# Patch libsndfile1 to support mp3
# sudo ln -sf /home/z/libsndfile-binaries/libsndfile_arm64.so /usr/lib64/libsndfile.so.1
# bullseye install libsndfile1 at: /usr/lib/aarch64-linux-gnu/libsndfile.so.1
RUN mkdir -p /usr/lib64 && \
    ln -sf /app/libsndfile-binaries/libsndfile_$(uname -m | sed 's/x86_64/x86_64/;s/arm64\|aarch64/arm64/').so /usr/lib/aarch64-linux-gnu/libsndfile.so.1
 
# Expose the port that the server will listen on
# EXPOSE 50051

# Start the server
CMD cd /app/emomusic && \
    python -m uvicorn main:app --host 0.0.0.0 --port 8002

