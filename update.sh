#!/bin/bash

check_for_update() {
    echo "Vérification des mises à jour..."

    # Charger la version locale
    if [ -f "config.env" ]; then
        local_version_line=$(cat config.env | grep 'VERSION=')
        local_version=$(echo $local_version_line | cut -d '=' -f2)
    else
        echo "Fichier config.env local introuvable. Impossible de vérifier la version actuelle."
        return 1
    fi

    echo "Version actuelle : $local_version"

    config_env_url="https://raw.githubusercontent.com/CFO-Clement/Seahawks_Nester/main/config.env"

    remote_version_line=$(curl -s $config_env_url | grep 'VERSION=')
    remote_version=$(echo $remote_version_line | cut -d '=' -f2)

    if [ ! -z "$remote_version" ]; then
        echo "Version disponible : $remote_version"
        if [ "$remote_version" != "$local_version" ]; then
            echo "Une nouvelle version ($remote_version) est disponible."
            echo "Mise à jour du projet..."
            update_project
        else
            echo "Vous utilisez déjà la dernière version."
        fi
    else
        echo "Impossible de récupérer la version distante."
    fi
}

update_project() {
    git stash
    if git pull; then
        echo "Le projet a été mis à jour avec succès."
    else
        echo "Échec de la mise à jour du projet. Veuillez vérifier manuellement."
    fi
}

check_for_update