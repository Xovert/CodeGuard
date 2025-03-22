#!/usr/bin/env bash

if [ ! -f 'CodeGuard/config.ini' ]; then
  echo "An error has occured!"
  echo "You must first create a config.ini file."
  exit 1
fi

cp prod-entrypoint.sh entrypoint.sh
# Bring up your Docker services in production mode
docker compose up -d
