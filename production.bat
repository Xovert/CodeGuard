@echo off

if not exist "CodeGuard\config.ini" (
    echo An error has occurred!
    echo You must first create a config.ini file.
    exit /b 1
)

copy /Y "prod-entrypoint.sh" "entrypoint.sh"
:: Bring up your Docker services in production mode
docker compose up -d