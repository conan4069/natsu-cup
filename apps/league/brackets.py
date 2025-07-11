from itertools import combinations
from .models import Match, TeamEntry, GroupStanding
import random

def generate_group_matches(tournament, group_entries_map):
  for group_code, teams in group_entries_map.items():
    for a, b in combinations(teams, 2):
      Match.objects.create(
        tournament=tournament,
        stage='group',
        group_code=group_code,
      ).participants.set([a, b])

def generate_knockout_bracket(tournament, qualified_teams, stage='round_of_16'):
  random.shuffle(qualified_teams)
  matches = []

  for i in range(0, len(qualified_teams), 2):
    match = Match.objects.create(
      tournament=tournament,
      stage=stage,
      played=False
    )
    match.participants.set([qualified_teams[i], qualified_teams[i + 1]])
    matches.append(match)

  # Semis y final se pueden generar vacíos, conectados con player_slot_x
  if stage == 'round_of_16':
    qf = [Match.objects.create(tournament=tournament, stage='quarterfinal') for _ in range(len(matches)//2)]
    for i, match in enumerate(matches):
      parent = qf[i//2]
      if i % 2 == 0:
        parent.player_slot_1 = match
      else:
        parent.player_slot_2 = match
      parent.save()
  
  return matches

def get_best_third_place_teams(tournament, needed=2):
  """
  Retorna los mejores terceros ordenados por puntos y diferencia de goles.
  """
  standings = GroupStanding.objects.filter(tournament=tournament)
  thirds = []

  # Agrupar por grupo
  groups = {}
  for standing in standings:
      groups.setdefault(standing.group_code, []).append(standing)

  # Detectar terceros por grupo
  for group_standings in groups.values():
      ordered = sorted(group_standings, key=lambda x: (x.points, x.goal_difference), reverse=True)
      if len(ordered) >= 3:
          thirds.append(ordered[2])  # el tercero

  # Ordenar los terceros por rendimiento
  thirds_sorted = sorted(thirds, key=lambda x: (x.points, x.goal_difference), reverse=True)
  return [t.team_entry for t in thirds_sorted[:needed]]

def get_missing_slots_for_stage(tournament, desired_total):
  """
  Retorna cuántos equipos hacen falta para completar una fase.
  """
  current_entries = TeamEntry.objects.filter(tournament=tournament).count()
  missing = desired_total - current_entries
  return max(0, missing)

def get_top_third_place_teams(tournament, count_needed):
    """
    Devuelve los mejores terceros ordenados por rendimiento.
    """
    standings = GroupStanding.objects.filter(tournament=tournament)
    thirds = []

    # Agrupar por grupo
    group_map = {}
    for s in standings:
        group_map.setdefault(s.group_code, []).append(s)

    # Sacar el 3er lugar por grupo
    for group in group_map.values():
        ordered = sorted(group, key=lambda x: (x.points, x.goal_difference), reverse=True)
        if len(ordered) >= 3:
            thirds.append(ordered[2])

    # Ordenarlos globalmente por méritos
    ordered_thirds = sorted(thirds, key=lambda x: (x.points, x.goal_difference), reverse=True)
    return [t.team_entry for t in ordered_thirds[:count_needed]]

def generate_playoffs_for_missing_slots(tournament, desired_total, stage_name):
    """
    Genera los partidos de repechaje necesarios para alcanzar el total de equipos requeridos.
    """

    missing = get_missing_slots_for_stage(tournament, desired_total)
    if missing == 0:
        return []

    total_needed = missing * 2  # cada partido necesita 2 equipos
    candidates = get_top_third_place_teams(tournament, total_needed)

    if len(candidates) < total_needed:
        raise ValueError("No hay suficientes terceros para cubrir los puestos faltantes")

    random.shuffle(candidates)
    new_matches = []

    for i in range(0, missing * 2, 2):
        m = Match.objects.create(
            tournament=tournament,
            stage=f'pre_{stage_name}',
            played=False
        )
        m.participants.set([candidates[i], candidates[i + 1]])
        new_matches.append(m)

    return new_matches

