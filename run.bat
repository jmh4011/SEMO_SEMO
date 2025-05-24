@echo off
setlocal

set SERVICE_ENV=%1

if "%SERVICE_ENV%"=="staging" (
    set ENV_FILE=.env.staging
    goto start
)

if "%SERVICE_ENV%"=="production" (
    set ENV_FILE=.env.production
    goto start
)

if "%SERVICE_ENV%"=="stop" (
    set ENV_FILE=.env.production
    docker compose down -v
    exit /b
)

echo [!] Invalid or no argument provided.
echo.
echo Usage:
echo   run.bat staging [--build]
echo   run.bat production [--build]
echo   run.bat stop [-v]
exit /b 1

:start
echo [*] Starting bot with %ENV_FILE%...
docker compose --env-file %ENV_FILE% up -d --build
