FROM python:3.12.8-slim-bookworm AS build

WORKDIR /opt/CodeGuard

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . /opt/CodeGuard

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12.8-slim-bookworm AS release
WORKDIR /opt/CodeGuard

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libffi8 \
        libssl3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=1001:1001 . /opt/CodeGuard

RUN useradd \
    --no-log-init \
    --shell /bin/bash \
    -u 1001 \
    codeguard \
    && mkdir -p /opt/CodeGuard/instance \
    && chown -R 1001:1001 /opt/CodeGuard/instance /opt/CodeGuard \
    && chmod +x /opt/CodeGuard/entrypoint.sh

COPY --chown=1001:1001 --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

USER 1001
EXPOSE 5000
ENTRYPOINT ["/opt/CodeGuard/entrypoint.sh"]
