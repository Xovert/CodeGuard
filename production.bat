@echo off

if not exist "entrypoint.sh" (
    copy /Y "docker-entrypoint.sh" "entrypoint.sh"
)

if not exist "CodeGuard\config.ini" (
    echo An error has occurred!
    echo You must first create a config.ini file.
    exit /b 1
)

:: Remove the --reload line if present
powershell -Command "(Get-Content entrypoint.sh) -notmatch '--reload' | Set-Content entrypoint.sh"

:: Bring up your Docker services in production mode
docker compose up -d