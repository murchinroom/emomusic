# TODO: docker run failed
#       OSError: cannot load library 'libsndfile.so': libsndfile.so: cannot open shared object file: No such file or directory
# 哈哈哈 Python 部署——我的一生之敌。

# Build phase
FROM python:3.9.16-slim-bullseye AS builder

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN \
    sed -i 's#http://deb.debian.org#https://mirrors.tuna.tsinghua.edu.cn#g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y build-essential

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

# Build the server
#RUN poetry build -f wheel && \
#    pip install dist/*.whl

# Runtime phase
#FROM python:3.9.16-slim-bullseye

# Set the working directory
#WORKDIR /app

# Copy the server binary and its dependencies from the builder image
#COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
#COPY --from=builder /app /app

# Expose the port that the server will listen on
# EXPOSE 50051

# Start the server
CMD cd /app/emomusic && \
    python -m uvicorn main:app --host 0.0.0.0 --port 8002

