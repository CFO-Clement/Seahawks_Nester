#!/bin/bash

ENV_FILE="./config.env"

configure_env() {
    read -p "Entrez une cles secrete pour la signature des cookies (SECRET_KEY)" SECRET_KEY
    read -p "Entrez l'ip d' ecoute de Flask (FLASK_EXPOSED_IP)" FLASK_LISTEN_IP
    read -p "Entrez le port d' ecoute de Flask (FLASK_LISTEN_PORT)" FLASK_LISTEN_PORT
    read -p "Entrez l' ip d'ecoute du Nester(NESTER_LISTEN_IP)" NESTER_LISTEN_IP
    read -p "Entrez le port d'ecoute du Nester (NESTER_LISTEN_PORT)" NESTER_LISTEN_PORT


    echo "SECRET_KEY=${SECRET_KEY}" > ${ENV_FILE}
    echo "FLASK_LISTEN_IP=${FLASK_LISTEN_IP}" >> ${ENV_FILE}
    echo "FLASK_LISTEN_PORT=${FLASK_LISTEN_PORT}" >> ${ENV_FILE}
    echo "NESTER_LISTEN_IP=${NESTER_LISTEN_IP}" >> ${ENV_FILE}
    echo "NESTER_LISTEN_PORT=${NESTER_LISTEN_PORT}" >> ${ENV_FILE}
    echo "" >> ${ENV_FILE}

    main
}

build_compose() {
    sudo docker-compose --env-file ${ENV_FILE} build
}

build_dockerfile() {
    sudo docker build --build-arg NESTER_LISTEN_PORT=${NESTER_LISTEN_PORT} FLASK_LISTEN_PORT=${FLASK_LISTEN_PORT} -t nester_image .
}

main() {
    if [ "$#" -gt 0 ]; then
        if [ "$1" = "compose" ]; then
            build_compose
        elif [ "$1" = "docker" ]; then
            build_dockerfile
        else
            echo "Argument invalide: $1"
            echo "Utilisation: $0 [compose|docker]"
            exit 1
        fi
    else
        echo "Bienvenue dans le script d'installation"
        echo "1. Configurer les variables d'environnement"
        echo "2. Construire avec Docker Compose"
        echo "3. Construire avec Dockerfile"
        read -p "Choisissez une option: " choice

        case $choice in
            1)
                configure_env
                ;;
            2)
                build_compose
                ;;
            3)
                build_dockerfile
                ;;
            *)
                echo "Option invalide."
                exit 1
                ;;
        esac
    fi

    echo "Installation terminée."
}
main
