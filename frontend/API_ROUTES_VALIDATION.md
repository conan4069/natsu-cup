# Validación de Rutas API - Frontend vs Django

## ✅ Rutas Validadas

### Torneos (`/tournaments/`)
| Frontend | Django | Método | Descripción |
|----------|--------|--------|-------------|
| `GET /tournaments/` | `tournaments/` | GET | Listar torneos |
| `POST /tournaments/` | `tournaments/` | POST | Crear torneo |
| `GET /tournaments/{id}/` | `tournaments/<int:pk>/` | GET | Obtener torneo |
| `PUT /tournaments/{id}/` | `tournaments/<int:pk>/` | PUT | Actualizar torneo |
| `DELETE /tournaments/{id}/` | `tournaments/<int:pk>/` | DELETE | Eliminar torneo |

### Generación de Grupos
| Frontend | Django | Método | Descripción |
|----------|--------|--------|-------------|
| `POST /tournaments/{id}/generate-groups/` | `tournaments/<int:tournament_id>/generate-groups/` | POST | Generar grupos |

### Entradas de Equipos
| Frontend | Django | Método | Descripción |
|----------|--------|--------|-------------|
| `GET /tournaments/{id}/entries/` | `tournaments/<int:tournament_id>/entries/` | GET | Listar entradas |
| `POST /tournaments/{id}/entries/` | `tournaments/<int:tournament_id>/entries/` | POST | Crear entrada |
| `DELETE /entries/{id}/delete/` | `entries/<int:pk>/delete/` | DELETE | Eliminar entrada |

### Asignación de Equipos
| Frontend | Django | Método | Descripción |
|----------|--------|--------|-------------|
| `POST /tournaments/{id}/assign-teams/` | `tournaments/<int:tournament_id>/assign-teams/` | POST | Asignar equipos aleatoriamente |

### Knockout
| Frontend | Django | Método | Descripción |
|----------|--------|--------|-------------|
| `GET /tournaments/{id}/knockout-preview/` | `tournaments/<int:tournament_id>/knockout-preview/` | GET | Vista previa knockout |
| `POST /tournaments/{id}/complete-knockout-stage/` | `tournaments/<int:tournament_id>/complete-knockout-stage/` | POST | Completar etapa knockout |

### Partidos
| Frontend | Django | Método | Descripción |
|----------|--------|--------|-------------|
| `GET /matches/{id}/` | `matches/<int:pk>/` | GET | Obtener partido |

### Jugadores
| Frontend | Django | Método | Descripción |
|----------|--------|--------|-------------|
| `GET /players/` | `players/` | GET | Listar jugadores |

### Equipos del Juego
| Frontend | Django | Método | Descripción |
|----------|--------|--------|-------------|
| `GET /teams/` | `teams/` | GET | Listar equipos del juego |

## 📋 Funciones Disponibles en Frontend

### tournamentAPI
```javascript
// Gestión de torneos
tournamentAPI.getTournaments()
tournamentAPI.createTournament(data)
tournamentAPI.getTournament(id)
tournamentAPI.updateTournament(id, data)
tournamentAPI.deleteTournament(id)

// Grupos
tournamentAPI.generateGroups(tournamentId)

// Entradas
tournamentAPI.getTeamEntries(tournamentId)
tournamentAPI.createTeamEntry(tournamentId, data)
tournamentAPI.deleteTeamEntry(entryId)

// Asignación
tournamentAPI.assignRandomTeams(tournamentId)

// Knockout
tournamentAPI.getKnockoutPreview(tournamentId)
tournamentAPI.completeKnockoutStage(tournamentId, data)
```

### matchAPI
```javascript
matchAPI.getMatch(matchId)
```

### playerAPI
```javascript
playerAPI.getPlayers()
```

### gameTeamAPI
```javascript
gameTeamAPI.getGameTeams()
```

## 🔧 Configuración

### Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp env.example .env

# Configurar URL de la API
VITE_API_URL=http://localhost:8000/api
```

### Uso en Componentes
```javascript
import { tournamentAPI, handleApiError } from '@/services/api'

try {
  const response = await tournamentAPI.getTournaments()
  console.log(response.data)
} catch (error) {
  const errorInfo = handleApiError(error)
  console.error(errorInfo.message)
}
```

## ✅ Estado de Validación

- ✅ **Todas las rutas coinciden** entre frontend y Django
- ✅ **Métodos HTTP correctos** para cada endpoint
- ✅ **Parámetros de URL** coinciden exactamente
- ✅ **Configuración de axios** lista para usar
- ✅ **Manejo de errores** centralizado
- ✅ **Variables de entorno** configuradas

## 📝 Notas

- Todas las rutas del frontend están basadas en `apps/league/urls.py`
- La configuración de axios incluye interceptores para autenticación
- El manejo de errores es consistente en toda la aplicación
- Las funciones están organizadas por dominio (torneos, partidos, etc.) 