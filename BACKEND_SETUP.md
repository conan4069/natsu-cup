# Configuración del Backend - Natsu Cup

## 🐳 Usando Docker

### Comandos rápidos con el script

```bash
# Ver todos los comandos disponibles
./scripts/backend.sh help

# Iniciar servicios
./scripts/backend.sh start

# Detener servicios
./scripts/backend.sh stop

# Reiniciar servicios
./scripts/backend.sh restart

# Ver logs del backend
./scripts/backend.sh logs

# Abrir shell de Django
./scripts/backend.sh shell

# Ejecutar migraciones
./scripts/backend.sh migrate

# Crear migraciones
./scripts/backend.sh makemigrations

# Crear superusuario
./scripts/backend.sh createsuperuser

# Cargar datos de ejemplo
./scripts/backend.sh loaddata sample_data.json

# Exportar datos
./scripts/backend.sh dumpdata league.player

# Ejecutar tests
./scripts/backend.sh test

# Recolectar archivos estáticos
./scripts/backend.sh collectstatic
```

### Comandos directos de Docker

```bash
# Iniciar servicios
docker compose up -d

# Detener servicios
docker compose down

# Ver logs
docker compose logs -f web

# Ejecutar comando en el contenedor
docker compose exec web python manage.py [comando]

# Ejecutar shell de Django
docker compose exec web python manage.py shell

# Ejecutar migraciones
docker compose exec web python manage.py migrate

# Crear migraciones
docker compose exec web python manage.py makemigrations

# Crear superusuario
docker compose exec web python manage.py createsuperuser

# Cargar datos de ejemplo
docker compose exec web python manage.py loaddata sample_data.json

# Exportar datos
docker compose exec web python manage.py dumpdata league.player --indent 2
```

## 📊 Datos de Ejemplo

### Cargar datos de ejemplo

```bash
# Cargar jugadores y equipos de ejemplo
./scripts/backend.sh loaddata sample_data.json
```

### Datos incluidos

**8 Jugadores famosos:**
- Lionel Messi (Argentina)
- Cristiano Ronaldo (Portugal)
- Neymar Jr (Brasil)
- Kevin De Bruyne (Bélgica)
- Erling Haaland (Noruega)
- Kylian Mbappé (Francia)
- Jude Bellingham (Inglaterra)
- Vinícius Jr (Brasil)

**15 Equipos famosos:**
- Real Madrid
- Manchester City
- Barcelona
- Bayern Munich
- PSG
- Liverpool
- Manchester United
- Chelsea
- Arsenal
- Juventus
- AC Milan
- Inter Milan
- Atlético Madrid
- Borussia Dortmund
- Ajax

## 🔧 Configuración Inicial

### 1. Iniciar servicios
```bash
./scripts/backend.sh start
```

### 2. Ejecutar migraciones
```bash
./scripts/backend.sh migrate
```

### 3. Crear superusuario (opcional)
```bash
./scripts/backend.sh createsuperuser
```

### 4. Cargar datos de ejemplo
```bash
./scripts/backend.sh loaddata sample_data.json
```

## 🌐 Acceso a la API

Una vez iniciados los servicios, la API estará disponible en:

- **URL Base**: `http://localhost:8000`
- **Admin Django**: `http://localhost:8000/admin/`
- **API Endpoints**: `http://localhost:8000/api/`

### Endpoints principales:

- `GET /api/players/` - Listar jugadores
- `GET /api/teams/` - Listar equipos
- `GET /api/tournaments/` - Listar torneos
- `POST /api/tournaments/` - Crear torneo
- `GET /api/tournaments/{id}/` - Ver torneo
- `POST /api/tournaments/{id}/team-entries/` - Agregar equipo al torneo
- `POST /api/tournaments/{id}/assign-random-teams/` - Asignar equipos automáticamente

## 🐛 Troubleshooting

### Problemas comunes:

1. **Docker no está corriendo**
   ```bash
   # Verificar que Docker esté activo
   docker info
   ```

2. **Puerto 8000 ocupado**
   ```bash
   # Verificar qué está usando el puerto
   lsof -i :8000
   ```

3. **Error de migraciones**
   ```bash
   # Recrear migraciones
   ./scripts/backend.sh makemigrations
   ./scripts/backend.sh migrate
   ```

4. **Error de permisos**
   ```bash
   # Hacer ejecutable el script
   chmod +x scripts/backend.sh
   ```

### Verificar estado de servicios:

```bash
# Ver contenedores corriendo
docker compose ps

# Ver logs en tiempo real
./scripts/backend.sh logs

# Ver logs de un servicio específico
docker compose logs web
```

## 📝 Notas Importantes

- Los datos de ejemplo se cargan en el fixture `apps/league/fixtures/sample_data.json`
- El script `scripts/backend.sh` facilita la gestión del backend
- Todos los comandos Django se ejecutan dentro del contenedor Docker
- La base de datos se persiste en un volumen de Docker
- Los archivos estáticos se sirven desde el contenedor

## 🔄 Flujo de Desarrollo

1. **Desarrollo**: Editar código en el host
2. **Docker**: Los cambios se reflejan automáticamente en el contenedor
3. **Migraciones**: Ejecutar cuando se cambian modelos
4. **Tests**: Ejecutar antes de commits
5. **Datos**: Cargar fixtures cuando sea necesario 