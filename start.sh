#!/bin/bash

start_compose() {
    echo "Démarrage des conteneurs avec Docker Compose..."
    sudo docker-compose --env-file config.env up
}

start_docker() {
    echo "Démarrage des conteneurs avec Docker..."
    sudo docker run -d --name nester nester_image
}

if [ "$#" -gt 0 ]; then
    if [ "$1" = "compose" ]; then
        start_compose
    elif [ "$1" = "docker" ]; then
        start_docker
    elif [ "$1" = "update" ]; then
        ./update.sh
        ./install.sh
    else
        echo "Argument invalide: $1"
        echo "Utilisation: $0 [compose|docker]"
        exit 1
    fi
else
    echo "Bienvenue dans le script de démarrage"
    echo "1. Démarrer avec Docker Compose"
    echo "2. Démarrer avec Docker"
    echo "3. Mettre à jour"
    read -p "Choisissez une option: " choice

    case $choice in
        1)
            start_compose
            ;;
        2)
            start_docker
            ;;
        3)
            ./update.sh
            ./install.sh
            ;;
        *)
            echo "Option invalide."
            exit 1
            ;;
    esac
fi

echo "Les conteneurs sont démarrés."
