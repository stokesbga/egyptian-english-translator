
FROM nvidia/cuda:12.4.1-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        git \
        python3-pip \
        python3-dev \
        python3-opencv \
        libglib2.0-0

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app
RUN  --mount=type=cache,target=/root/.cache/pip pip install -r /code/requirements.txt

EXPOSE 80

ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:80", "app.main:app", "-n"]