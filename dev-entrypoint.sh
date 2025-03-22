#!/bin/bash
set -euo pipefail

WORKERS=${WORKERS:-1}
WORKER_CLASS=${WORKER_CLASS:-gevent}
WORKER_TEMP_DIR=${WORKER_TEMP_DIR:-/dev/shm}
SECRET_KEY=${SECRET_KEY:-}
SECURITY_PASSWORD_SALT=${SECURITY_PASSWORD_SALT:-}

if [ ! -f 'secrets/.secret_key' ] && [ -z "$SECRET_KEY" ]; then
    head -c 64 /dev/urandom > secrets/.secret_key
    chmod 600 .secret_key
fi

if [ ! -f 'secrets/.security_salt' ] && [ -z "$SECURITY_PASSWORD_SALT" ]; then
    head -c 64 /dev/urandom > secrets/.security_salt
    chmod 600 .security_salt
fi

# Initialize database
flask db upgrade
# Seed the database
flask seed

exec gunicorn "CodeGuard:create_app()" \
    --bind '0.0.0.0:5000' \
    --workers $WORKERS \
    --worker-tmp-dir "$WORKER_TEMP_DIR" \
    --worker-class "$WORKER_CLASS" \
    --reload