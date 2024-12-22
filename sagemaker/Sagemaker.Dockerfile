
FROM ubuntu:22.04

LABEL com.amazonaws.sagemaker.capabilities.multi-models=true
LABEL com.amazonaws.sagemaker.capabilities.accept-bind-to-port=true

ENV DEBIAN_FRONTEND=noninteractive

# Install python3
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y curl python3.11 python3.11-dev python3.11-distutils

RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# Install necessary dependencies for MMS and SageMaker Inference Toolkit
RUN apt-get -y install --no-install-recommends \
    build-essential \
    ca-certificates \
    openjdk-8-jdk-headless \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/* \
    && python --version \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python get-pip.py

# Install MMS and SageMaker Inference Toolkit to set up MMS
RUN pip --no-cache-dir install multi-model-server \
    sagemaker-inference \
    retrying

# Symlink cuda
RUN ln -s /usr/lib/cuda /usr/local/cuda-12.4


WORKDIR /app

COPY app ./inference_code_dir
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
ENV PATH="/app:${PATH}"

COPY handler.py .
COPY dockerd-entrypoint.py .

# Define an entrypoint script for the docker image
ENTRYPOINT ["python", "/app/dockerd-entrypoint.py"]

# Define command to be passed to the entrypoint
CMD ["serve"]