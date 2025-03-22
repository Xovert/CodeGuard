@echo off

if not exist "entrypoint.sh" (
    copy /Y "dev-entrypoint.sh" "entrypoint.sh"
)

if not exist "CodeGuard\config.ini" (
    echo An error has occurred!
    echo You must first create a config.ini file.
    exit /b 1
)

:: Bring up your Docker services
docker compose up -d
