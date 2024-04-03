FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /indizio

COPY . ./indizio

WORKDIR /indizio

RUN python -m pip install .

ENTRYPOINT [ "python", "-m", "indizio" ]
