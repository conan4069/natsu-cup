export const shuffleAndGroup = (players, groupSize = 2) => {
  const shuffled = [...players].sort(() => 0.5 - Math.random())
  const result = []
  for (let i = 0; i < shuffled.length; i += groupSize) {
    result.push(shuffled.slice(i, i + groupSize))
  }
  return result
}

// Frontend       →        API Django
// ──────────────           ───────────────
// Crear jugadores   →   /players/ (custom POST)
// Formar 2v2        →   /tournaments/<id>/entries/
// Asignar equipos   →   /tournaments/<id>/assign-teams/
// Ver preview       →   /tournaments/<id>/knockout-preview/
// Confirmar fase    →   /tournaments/<id>/complete-knockout-stage/
