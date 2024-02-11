@echo off
setlocal

set "config_env_url=https://raw.githubusercontent.com/CFO-Clement/Seahawks_Nester/main/config.env"

call :check_for_update
goto :eof

:check_for_update
echo Vérification des mises à jour...

if exist config.env (
    for /f "tokens=2 delims==" %%a in ('type config.env ^| findstr "VERSION="') do set "local_version=%%a"
) else (
    echo Fichier config.env local introuvable. Impossible de vérifier la version actuelle.
    exit /b 1
)

echo Version actuelle: %local_version%

for /f "tokens=*" %%i in ('curl -s %config_env_url% ^| findstr "VERSION="') do set "remote_version_line=%%i"
for /f "tokens=2 delims==" %%a in ("%remote_version_line%") do set "remote_version=%%a"

if not "%remote_version%"=="" (
    echo Version disponible: %remote_version%
    if not "%remote_version%"=="%local_version%" (
        echo Une nouvelle version (%remote_version%) est disponible.
        echo Mise à jour du projet...
        call :update_project
    ) else (
        echo Vous utilisez déjà la dernière version.
    )
) else (
    echo Impossible de récupérer la version distante.
)

exit /b

:update_project
if git pull (
    echo Le projet a été mis à jour avec succès.
) else (
    echo Échec de la mise à jour du projet. Veuillez vérifier manuellement.
)

exit /b
