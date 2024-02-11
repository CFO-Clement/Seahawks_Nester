@echo off
setlocal enabledelayedexpansion

set ENV_FILE=./config.env

:configure_env
set /p SECRET_KEY=Entrez une cles secrete pour la signature des cookies (SECRET_KEY):
set /p FLASK_EXPOSE_IP=Entrez l' ip d'ecoute de Flask (FLASK_EXPOSE_IP):
set /p FLASK_LISTEN_PORT=Entrez le port d'ecoute de Flask (FLASK_LISTEN_PORT):
set /p NESTER_LISTEN_IP=Entrez l' ip d'ecoute du Nester(NESTER_LISTEN_IP):
set /p NESTER_LISTEN_PORT=Entrez le port d'ecoute du Nester(NESTER_LISTEN_PORT):

echo SECRET_KEY=!SECRET_KEY! >> %ENV_FILE%
echo FLASK_EXPOSE_IP=!FLASK_EXPOSE_IP! >> %ENV_FILE%
echo FLASK_LISTEN_PORT=!FLASK_LISTEN_PORT! >> %ENV_FILE%
echo NESTER_LISTEN_IP=!NESTER_LISTEN_IP! >> %ENV_FILE%
echo NESTER_LISTEN_PORT=!NESTER_LISTEN_PORT! >> %ENV_FILE%

goto main

:build_compose
docker-compose --env-file %ENV_FILE% build
goto :eof

:build_dockerfile
docker build --build-arg NESTER_LISTEN_PORT=!NESTER_LISTEN_PORT! FLASK_LISTEN_PORT=!FLASK_LISTEN_PORT! -t nester_image .
goto :eof

:main
if "%~1" neq "" (
    if "%1" == "compose" (
        call :build_compose
    ) else if "%1" == "docker" (
        call :build_dockerfile
    ) else (
        echo Argument invalide: %1
        echo Utilisation: %0 [compose|docker]
        exit /b 1
    )
) else (
    echo Bienvenue dans le script d'installation
    echo 1. Configurer les variables d'environnement
    echo 2. Construire avec Docker Compose
    echo 3. Construire avec Dockerfile
    set /p choice=Choisissez une option:

    if "!choice!"=="1" (
        call :configure_env
    ) else if "!choice!"=="2" (
        call :build_compose
    ) else if "!choice!"=="3" (
        call :build_dockerfile
    ) else (
        echo Option invalide.
        exit /b 1
    )
)

echo Installation terminee.
