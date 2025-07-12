import api, { handleApiError } from '@/utils/axios'

// Funciones de API para torneos (coincide con apps/league/urls.py)
export const tournamentAPI = {
  // Listar y crear torneos
  getTournaments: () => api.get('/tournaments/'),
  createTournament: data => api.post('/tournaments/', data),

  // Obtener, actualizar y eliminar torneo específico
  getTournament: tournamentId => api.get(`/tournaments/${tournamentId}/`),
  updateTournament: (tournamentId, data) =>
    api.put(`/tournaments/${tournamentId}/`, data),
  deleteTournament: tournamentId => api.delete(`/tournaments/${tournamentId}/`),

  // Generar grupos
  generateGroups: tournamentId =>
    api.post(`/tournaments/${tournamentId}/generate-groups/`),

  // Entradas de equipos
  getTeamEntries: tournamentId =>
    api.get(`/tournaments/${tournamentId}/entries/`),
  createTeamEntry: (tournamentId, data) =>
    api.post(`/tournaments/${tournamentId}/entries/`, data),
  deleteTeamEntry: entryId => api.delete(`/entries/${entryId}/delete/`),

  // Asignar equipos aleatoriamente
  assignRandomTeams: tournamentId =>
    api.post(`/tournaments/${tournamentId}/assign-teams/`),

  // Vista previa de knockout
  getKnockoutPreview: tournamentId =>
    api.get(`/tournaments/${tournamentId}/knockout-preview/`),

  // Completar etapa de knockout
  completeKnockoutStage: (tournamentId, data) =>
    api.post(`/tournaments/${tournamentId}/complete-knockout-stage/`, data),
}

// Funciones de API para partidos
export const matchAPI = {
  // Obtener partido específico
  getMatch: matchId => api.get(`/matches/${matchId}/`),
}

// Funciones de API para jugadores
export const playerAPI = {
  // Listar jugadores
  getPlayers: () => api.get('/players/'),

  // Crear jugador
  createPlayer: data => api.post('/players/create/', data),

  // Obtener jugador específico
  getPlayer: playerId => api.get(`/players/${playerId}/`),

  // Actualizar jugador
  updatePlayer: (playerId, data) => api.put(`/players/${playerId}/`, data),

  // Eliminar jugador
  deletePlayer: playerId => api.delete(`/players/${playerId}/`),

  // Obtener estadísticas del jugador
  getPlayerStats: playerId => api.get(`/players/${playerId}/stats/`),

  // Obtener torneos del jugador
  getPlayerTournaments: playerId => api.get(`/players/${playerId}/tournaments/`),
}

// Funciones de API para equipos del juego
export const gameTeamAPI = {
  // Listar equipos del juego
  getGameTeams: () => api.get('/teams/'),
}

// Funciones de API para equipos
export const teamAPI = {
  // Listar equipos
  getTeams: () => api.get('/teams/'),

  // Crear equipo
  createTeam: data => api.post('/teams/', data),

  // Obtener equipo específico
  getTeam: teamId => api.get(`/teams/${teamId}/`),

  // Actualizar equipo
  updateTeam: (teamId, data) => api.put(`/teams/${teamId}/`, data),

  // Eliminar equipo
  deleteTeam: teamId => api.delete(`/teams/${teamId}/`),

  // Obtener estadísticas del equipo (si aplica)
  getTeamStats: teamId => api.get(`/teams/${teamId}/stats/`),

  // Obtener torneos del equipo (si aplica)
  getTeamTournaments: teamId => api.get(`/teams/${teamId}/tournaments/`),
}

// Exportar la función de manejo de errores para uso en componentes
export { handleApiError }
