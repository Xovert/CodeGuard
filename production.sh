#!/usr/bin/env bash

if [ ! -f 'CodeGuard/config.ini' ]; then
  echo "An error has occured!"
  echo "You must first create a config.ini file."
  exit 1
fi

# Remove the --reload line if present
if grep -q -- '--reload' entrypoint.sh; then
  sed -i '/--reload/d' entrypoint.sh
fi

# Bring up your Docker services in production mode
docker compose up -d
