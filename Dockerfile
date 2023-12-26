FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /indizio

COPY . ./indizio

WORKDIR /indizio

RUN python -m pip install \
    dash \
    dash_bootstrap_components \
    dash_cytoscape \
    diskcache \
    "dash[diskcache]" \
    dash_bio \
    pydantic \
    networkx \
    orjson \
    dendropy \
    frozendict \
    pillow \
    pandas

EXPOSE 8050
ENTRYPOINT [ "python", "-m", "indizio" ]
