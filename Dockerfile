
FROM mambaorg/micromamba:cuda12.4.1-ubuntu22.04


WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./environment.yml /code/environment.yml
COPY ./app /code/app

RUN micromamba install --yes -n base --file ./environment.yml && \
    micromamba clean --all --yes
    ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN pip install --no-cache-dir -r /code/requirements.txt

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]