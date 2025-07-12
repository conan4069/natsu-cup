#!/bin/bash

# Script para gestionar el backend con Docker
# Uso: ./scripts/backend.sh [comando] [opciones]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}Script de gestión del backend Natsu Cup${NC}"
    echo ""
    echo "Uso: $0 [comando] [opciones]"
    echo ""
    echo "Comandos disponibles:"
    echo "  start          - Iniciar los servicios de Docker"
    echo "  stop           - Detener los servicios de Docker"
    echo "  restart        - Reiniciar los servicios de Docker"
    echo "  logs           - Mostrar logs del backend"
    echo "  shell          - Abrir shell de Django"
    echo "  migrate        - Ejecutar migraciones"
    echo "  makemigrations - Crear migraciones"
    echo "  createsuperuser - Crear superusuario"
    echo "  loaddata       - Cargar datos de ejemplo"
    echo "  dumpdata       - Exportar datos"
    echo "  test           - Ejecutar tests"
    echo "  collectstatic  - Recolectar archivos estáticos"
    echo "  help           - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 start"
    echo "  $0 shell"
    echo "  $0 loaddata sample_data.json"
    echo "  $0 migrate"
}

# Función para ejecutar comando en el contenedor
run_in_container() {
    local cmd="$1"
    echo -e "${YELLOW}Ejecutando: $cmd${NC}"
    docker compose exec web python manage.py $cmd
}

# Función para ejecutar comando directo en el contenedor
run_direct() {
    local cmd="$1"
    echo -e "${YELLOW}Ejecutando: $cmd${NC}"
    docker compose exec web $cmd
}

# Verificar que Docker esté corriendo
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}Error: Docker no está corriendo${NC}"
        exit 1
    fi
}

# Verificar que docker-compose esté disponible
check_compose() {
    if ! docker compose version > /dev/null 2>&1; then
        echo -e "${RED}Error: docker-compose no está disponible${NC}"
        exit 1
    fi
}

# Función principal
main() {
    check_docker
    check_compose

    case "$1" in
        "start")
            echo -e "${GREEN}Iniciando servicios...${NC}"
            docker compose up -d
            echo -e "${GREEN}Servicios iniciados${NC}"
            ;;
        "stop")
            echo -e "${YELLOW}Deteniendo servicios...${NC}"
            docker compose down
            echo -e "${GREEN}Servicios detenidos${NC}"
            ;;
        "restart")
            echo -e "${YELLOW}Reiniciando servicios...${NC}"
            docker compose restart
            echo -e "${GREEN}Servicios reiniciados${NC}"
            ;;
        "logs")
            echo -e "${BLUE}Mostrando logs del backend...${NC}"
            docker compose logs -f web
            ;;
        "shell")
            echo -e "${BLUE}Abriendo shell de Django...${NC}"
            run_direct "python manage.py shell"
            ;;
        "migrate")
            echo -e "${BLUE}Ejecutando migraciones...${NC}"
            run_in_container "migrate"
            echo -e "${GREEN}Migraciones completadas${NC}"
            ;;
        "makemigrations")
            echo -e "${BLUE}Creando migraciones...${NC}"
            run_in_container "makemigrations"
            echo -e "${GREEN}Migraciones creadas${NC}"
            ;;
        "createsuperuser")
            echo -e "${BLUE}Creando superusuario...${NC}"
            run_in_container "createsuperuser"
            ;;
        "loaddata")
            if [ -z "$2" ]; then
                echo -e "${RED}Error: Debes especificar el archivo de fixture${NC}"
                echo "Uso: $0 loaddata <archivo.json>"
                exit 1
            fi
            echo -e "${BLUE}Cargando datos desde $2...${NC}"
            run_in_container "loaddata $2"
            echo -e "${GREEN}Datos cargados exitosamente${NC}"
            ;;
        "dumpdata")
            if [ -z "$2" ]; then
                echo -e "${RED}Error: Debes especificar el modelo${NC}"
                echo "Uso: $0 dumpdata <app.model>"
                exit 1
            fi
            echo -e "${BLUE}Exportando datos de $2...${NC}"
            run_in_container "dumpdata $2 --indent 2"
            ;;
        "test")
            echo -e "${BLUE}Ejecutando tests...${NC}"
            run_in_container "test"
            echo -e "${GREEN}Tests completados${NC}"
            ;;
        "collectstatic")
            echo -e "${BLUE}Recolectando archivos estáticos...${NC}"
            run_in_container "collectstatic --noinput"
            echo -e "${GREEN}Archivos estáticos recolectados${NC}"
            ;;
        "help"|"-h"|"--help"|"")
            show_help
            ;;
        *)
            echo -e "${RED}Error: Comando '$1' no reconocido${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@" 