#!/usr/bin/env bash

if [ ! -f 'CodeGuard/config.ini' ]; then
  echo "An error has occured!"
  echo "You must first create a config.ini file."
  exit 1
fi

cp dev-entrypoint.sh entrypoint.sh
# Bring up your Docker services
docker compose up -d
