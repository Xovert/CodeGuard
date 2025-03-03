#!/usr/bin/env bash

if [ ! -f 'entrypoint.sh' ]; then
  cp docker-entrypoint.sh entrypoint.sh
fi

if [ ! -f 'CodeGuard/config.ini' ]; then
  echo "An error has occured!"
  echo "You must first create a config.ini file."
  exit 1
fi

if ! grep -q -- '--reload' entrypoint.sh 2>/dev/null; then
  sed -i '/--worker-class.*$WORKER_CLASS"/a \    --reload' entrypoint.sh
fi

# Bring up your Docker services
docker compose up -d
