@echo off
setlocal enabledelayedexpansion

:start_compose
echo Demarrage des conteneurs avec Docker Compose...
docker-compose --env-file config.env up
goto end

:start_docker
echo Demarrage des conteneurs avec Docker...
docker run -d --name nester nester_image
goto end

:main
if not "%~1"=="" (
    if "%1"=="compose" (
        call :start_compose
    ) else if "%1"=="docker" (
        call :start_docker
    ) else (
        echo Argument invalide: %1
        echo Utilisation: %0 [compose|docker]
        exit /b 1
    )
) else (
    echo Bienvenue dans le script de demarrage
    echo 1. Demarrer avec Docker Compose
    echo 2. Demarrer avec Docker
    echo 3. Mise a jour
    set /p choice=Choisissez une option:

    if "!choice!"=="1" (
        call :start_compose
    ) else if "!choice!"=="2" (
        call :start_docker
    ) else if "!choice!"=="3" (
        cmd update.bat
        cmd install.bat
    ) else (
        echo Option invalide.
        exit /b 1
    )
)

:end
echo Les conteneurs sont demarres.
