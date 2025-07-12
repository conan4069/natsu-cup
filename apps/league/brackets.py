from itertools import combinations
from .models import Match, TeamEntry, GroupStanding
import random

def generate_group_matches(tournament, group_entries_map):
    """
    Genera partidos de grupos y retorna la lista de partidos creados.
    Solo crea partidos que no existan previamente.
    """
    matches_created = []
    
    for group_code, teams in group_entries_map.items():
        for a, b in combinations(teams, 2):
            # Verificar si ya existe el partido
            existing_match = Match.objects.filter(
                tournament=tournament,
                stage='group',
                group_code=group_code,
                participants=a
            ).filter(participants=b).first()
            
            if not existing_match:
                # Crear nuevo partido
                match = Match.objects.create(
                    tournament=tournament,
                    stage='group',
                    group_code=group_code,
                )
                match.participants.set([a, b])
                matches_created.append(match)
    
    return matches_created

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

def get_qualified_teams_for_knockout(tournament):
    """
    Obtiene los equipos clasificados para la fase eliminatoria.
    Retorna un diccionario con los equipos organizados por tipo de clasificación.
    """
    standings = GroupStanding.objects.filter(tournament=tournament)
    
    # Agrupar por grupo
    group_map = {}
    for standing in standings:
        group_map.setdefault(standing.group_code, []).append(standing)
    
    qualified_teams = {
        'group_winners': [],
        'group_runners_up': [],
        'best_third_place': [],
        'total_qualified': 0
    }
    
    # Obtener primeros y segundos de cada grupo
    for group_code, group_standings in group_map.items():
        sorted_standings = sorted(
            group_standings,
            key=lambda x: (x.points, x.goal_difference, x.goals_for),
            reverse=True
        )
        
        # Agregar primero (ganador del grupo)
        if len(sorted_standings) >= 1:
            qualified_teams['group_winners'].append({
                'team_entry': sorted_standings[0].team_entry,
                'group_code': group_code,
                'position': 1,
                'points': sorted_standings[0].points,
                'goal_difference': sorted_standings[0].goal_difference,
                'goals_for': sorted_standings[0].goals_for
            })
        
        # Agregar segundo (subcampeón del grupo)
        if len(sorted_standings) >= 2:
            qualified_teams['group_runners_up'].append({
                'team_entry': sorted_standings[1].team_entry,
                'group_code': group_code,
                'position': 2,
                'points': sorted_standings[1].points,
                'goal_difference': sorted_standings[1].goal_difference,
                'goals_for': sorted_standings[1].goals_for
            })
    
    # Obtener los mejores terceros
    all_thirds = []
    for group_code, group_standings in group_map.items():
        sorted_standings = sorted(
            group_standings,
            key=lambda x: (x.points, x.goal_difference, x.goals_for),
            reverse=True
        )
        
        if len(sorted_standings) >= 3:
            all_thirds.append({
                'team_entry': sorted_standings[2].team_entry,
                'group_code': group_code,
                'position': 3,
                'points': sorted_standings[2].points,
                'goal_difference': sorted_standings[2].goal_difference,
                'goals_for': sorted_standings[2].goals_for
            })
    
    # Ordenar terceros por méritos
    all_thirds.sort(key=lambda x: (x['points'], x['goal_difference'], x['goals_for']), reverse=True)
    
    # Tomar los mejores terceros (normalmente 4 para completar 16 equipos)
    needed_third_place = 4  # Ajustar según el formato del torneo
    qualified_teams['best_third_place'] = all_thirds[:needed_third_place]
    
    # Calcular total
    qualified_teams['total_qualified'] = (
        len(qualified_teams['group_winners']) + 
        len(qualified_teams['group_runners_up']) + 
        len(qualified_teams['best_third_place'])
    )
    
    return qualified_teams

