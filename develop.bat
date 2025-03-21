@echo off

if not exist "entrypoint.sh" (
    copy /Y "docker-entrypoint.sh" "entrypoint.sh"
)

if not exist "CodeGuard\config.ini" (
    echo An error has occurred!
    echo You must first create a config.ini file.
    exit /b 1
)

:: Check if --reload is present; if not, add it after --worker-class
powershell -Command "if (-Not (Select-String -Path 'entrypoint.sh' -Pattern '--reload')) { (Get-Content 'entrypoint.sh') -replace '(--worker-class.*$WORKER_CLASS")', '$1`n    --reload' | Set-Content 'entrypoint.sh' }"

:: Bring up your Docker services
docker compose up -d
