#!/bin/bash
set -euo pipefail

WORKERS=${WORKERS:-1}
WORKER_CLASS=${WORKER_CLASS:-gevent}
WORKER_TEMP_DIR=${WORKER_TEMP_DIR:-/dev/shm}
SECRET_KEY=${SECRET_KEY:-}
SECURITY_PASSWORD_SALT=${SECURITY_PASSWORD_SALT:-}

if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(head -c 64 /dev/urandom | base64 | tr -d '\n')
fi

if [ -z "$SECURITY_PASSWORD_SALT" ]; then
    SECURITY_PASSWORD_SALT=$(head -c 64 /dev/urandom | base64 | tr -d '\n')
fi

# Initialize database
flask db upgrade
# Seed the database
flask seed

# Start CTFd
exec gunicorn 'CodeGuard:create_app()' \
    --bind '0.0.0.0:8000' \
    --workers $WORKERS \
    --worker-tmp-dir "$WORKER_TEMP_DIR" \
    --worker-class "$WORKER_CLASS"