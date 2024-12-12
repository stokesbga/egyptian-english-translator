
FROM mambaorg/micromamba


WORKDIR /code


COPY ./environment.yml /code/environment.yml
COPY ./app /code/app

RUN micromamba install --yes -n base --file ./environment.yml && \
    micromamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1

EXPOSE 7777

CMD ["fastapi", "run", "app/main.py", "--port", "7777"]