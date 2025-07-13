from itertools import combinations
from .models import Match, TeamEntry, GroupStanding, TournamentStanding
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

def generate_playoff_qualification_matches(tournament, current_teams, target_teams):
    """
    Genera partidos de repechaje para completar los equipos necesarios.
    """
    if len(current_teams) >= target_teams:
        return current_teams, []
    
    # Obtener equipos disponibles para repechaje
    available_teams = get_teams_for_playoff_qualification(tournament, current_teams)
    
    if len(available_teams) < (target_teams - len(current_teams)) * 2:
        raise ValueError(f"No hay suficientes equipos para completar {target_teams} equipos")
    
    # Generar partidos de repechaje
    playoff_matches = []
    qualified_from_playoff = []
    
    # Calcular cuántos partidos necesitamos
    needed_matches = (target_teams - len(current_teams))
    
    # Crear partidos de repechaje
    for i in range(needed_matches):
        match = Match.objects.create(
            tournament=tournament,
            stage='playoff_qualification',
            played=False
        )
        
        # Asignar equipos al partido
        team1 = available_teams[i * 2]
        team2 = available_teams[i * 2 + 1]
        match.participants.set([team1, team2])
        
        playoff_matches.append(match)
    
    return current_teams, playoff_matches

def get_teams_for_playoff_qualification(tournament, already_qualified):
    """
    Obtiene equipos disponibles para repechaje (terceros, cuartos, etc.)
    """
    standings = GroupStanding.objects.filter(tournament=tournament)
    
    # Agrupar por grupo
    group_map = {}
    for standing in standings:
        group_map.setdefault(standing.group_code, []).append(standing)
    
    available_teams = []
    
    for group_code, group_standings in group_map.items():
        sorted_standings = sorted(
            group_standings,
            key=lambda x: (x.points, x.goal_difference, x.goals_for),
            reverse=True
        )
        
        # Agregar equipos no clasificados (terceros, cuartos, etc.)
        for i in range(2, len(sorted_standings)):
            team_entry = sorted_standings[i].team_entry
            if team_entry not in already_qualified:
                available_teams.append(team_entry)
    
    # Ordenar por méritos (puntos, diferencia de goles, etc.)
    available_teams.sort(key=lambda x: (
        x.groupstanding_set.first().points,
        x.groupstanding_set.first().goal_difference,
        x.groupstanding_set.first().goals_for
    ), reverse=True)
    
    return available_teams

def generate_complete_knockout_bracket(tournament, qualified_teams, initial_stage='quarterfinal'):
    """
    Genera un bracket completo de eliminatorias desde la etapa inicial hasta la final.
    Crea todos los partidos necesarios con placeholders para equipos futuros.
    """
    matches_created = []
    
    # Determinar todas las etapas necesarias
    stages = []
    if initial_stage == 'round_of_16':
        stages = ['round_of_16', 'quarterfinal', 'semifinal', 'final']
    elif initial_stage == 'quarterfinal':
        stages = ['quarterfinal', 'semifinal', 'final']
    elif initial_stage == 'semifinal':
        stages = ['semifinal', 'final']
    elif initial_stage == 'final':
        stages = ['final']
    
    # Generar partidos de la etapa inicial con equipos reales
    current_stage = stages[0]
    current_teams = qualified_teams.copy()
    
    # Para cuartos de final, usar clasificación cruzada si viene de grupos
    if current_stage == 'quarterfinal' and tournament.competition_type == 'groups':
        # Ordenar equipos por grupos y posiciones
        group_winners = []
        group_runners = []
        
        # Obtener ganadores y segundos de cada grupo
        standings = GroupStanding.objects.filter(tournament=tournament)
        group_map = {}
        for standing in standings:
            group_map.setdefault(standing.group_code, []).append(standing)
        
        # Ordenar grupos alfabéticamente para consistencia
        sorted_groups = sorted(group_map.keys())
        
        for group_code in sorted_groups:
            group_standings = group_map[group_code]
            sorted_standings = sorted(
                group_standings,
                key=lambda x: (x.points, x.goal_difference, x.goals_for),
                reverse=True
            )
            if len(sorted_standings) >= 1:
                group_winners.append(sorted_standings[0].team_entry)
            if len(sorted_standings) >= 2:
                group_runners.append(sorted_standings[1].team_entry)
        
        # Clasificación cruzada: A1 vs B2, B1 vs A2, C1 vs D2, D1 vs C2, etc.
        current_teams = []
        for i in range(min(len(group_winners), len(group_runners))):
            current_teams.append(group_winners[i])
            current_teams.append(group_runners[i])
    
    # Crear partidos de la primera etapa
    first_stage_matches = []
    for i in range(0, len(current_teams), 2):
        if i + 1 < len(current_teams):
            match = Match.objects.create(
                tournament=tournament,
                stage=current_stage,
                played=False
            )
            match.participants.set([current_teams[i], current_teams[i + 1]])
            first_stage_matches.append(match)
            matches_created.append(match)
    
    # Generar partidos de etapas posteriores con placeholders
    for stage in stages[1:]:
        num_matches = len(first_stage_matches) // 2
        stage_matches = []
        
        for i in range(num_matches):
            match = Match.objects.create(
                tournament=tournament,
                stage=stage,
                played=False
            )
            
            # Conectar con partidos de la etapa anterior
            if i * 2 < len(first_stage_matches):
                match.player_slot_1 = first_stage_matches[i * 2]
            if i * 2 + 1 < len(first_stage_matches):
                match.player_slot_2 = first_stage_matches[i * 2 + 1]
            match.save()
            
            stage_matches.append(match)
            matches_created.append(match)
        
        first_stage_matches = stage_matches
    
    return matches_created

def generate_knockout_bracket(tournament, qualified_teams, stage='round_of_16'):
    """
    Genera partidos de eliminatoria para la etapa especificada.
    Solo genera los partidos de la etapa actual, no etapas adicionales.
    """
    random.shuffle(qualified_teams)
    matches = []

    # Generar solo los partidos de la etapa especificada
    for i in range(0, len(qualified_teams), 2):
        if i + 1 < len(qualified_teams):  # Asegurar que hay 2 equipos
            match = Match.objects.create(
                tournament=tournament,
                stage=stage,
                played=False
            )
            match.participants.set([qualified_teams[i], qualified_teams[i + 1]])
            matches.append(match)
    
    return matches

def get_team_display_name(team_entry):
    """
    Obtiene el nombre de visualización del equipo.
    """
    if team_entry.assigned_team:
        return team_entry.assigned_team.name
    
    player_names = [player.display_name for player in team_entry.players.all()]
    if len(player_names) == 1:
        return player_names[0]
    elif len(player_names) == 2:
        return f"{player_names[0]} & {player_names[1]}"
    else:
        return f"Equipo {team_entry.id}"

def get_team_logo_url(team_entry, request=None):
    """
    Obtiene la URL del logo del equipo.
    """
    if team_entry.assigned_team and team_entry.assigned_team.logo:
        if request:
            return request.build_absolute_uri(team_entry.assigned_team.logo.url)
        return f"/media/{team_entry.assigned_team.logo}"
    return None

def determine_knockout_stage_and_teams(tournament):
    """
    Determina la etapa inicial de eliminatorias y los equipos necesarios
    según la cantidad de equipos clasificados.
    """
    # Para torneos de grupos, usar GroupStanding
    if tournament.competition_type == 'groups':
        standings = GroupStanding.objects.filter(tournament=tournament)
        
        # Agrupar por grupo
        group_map = {}
        for standing in standings:
            group_map.setdefault(standing.group_code, []).append(standing)
        
        # Contar equipos clasificados
        qualified_teams = []
        for group_code, group_standings in group_map.items():
            sorted_standings = sorted(
                group_standings,
                key=lambda x: (x.points, x.goal_difference, x.goals_for),
                reverse=True
            )
            
            # Agregar primero y segundo de cada grupo
            if len(sorted_standings) >= 1:
                qualified_teams.append(sorted_standings[0].team_entry)
            if len(sorted_standings) >= 2:
                qualified_teams.append(sorted_standings[1].team_entry)
        
        total_qualified = len(qualified_teams)
        
        # Determinar etapa inicial según cantidad de equipos
        if total_qualified >= 16:
            return {
                'stage': 'round_of_16',
                'required_teams': 16,
                'qualified_teams': qualified_teams,
                'strategy': 'direct_qualification'
            }
        elif total_qualified >= 8:
            return {
                'stage': 'quarterfinal',
                'required_teams': 8,
                'qualified_teams': qualified_teams,
                'strategy': 'direct_qualification'
            }
        elif total_qualified >= 4:
            return {
                'stage': 'semifinal',
                'required_teams': 4,
                'qualified_teams': qualified_teams,
                'strategy': 'direct_qualification'
            }
        elif total_qualified >= 2:
            return {
                'stage': 'final',
                'required_teams': 2,
                'qualified_teams': qualified_teams,
                'strategy': 'direct_qualification'
            }
        else:
            return {
                'stage': 'quarterfinal',
                'required_teams': 8,
                'qualified_teams': qualified_teams,
                'strategy': 'playoff_qualification'
            }
    
    # Para torneos de liga, usar TournamentStanding
    elif tournament.competition_type == 'league':
        standings = TournamentStanding.objects.filter(tournament=tournament).order_by('-points', '-goal_difference', '-goals_for')
        qualified_teams = [standing.team_entry for standing in standings[:tournament.playoff_teams]]
        
        return {
            'stage': 'quarterfinal',
            'required_teams': len(qualified_teams),
            'qualified_teams': qualified_teams,
            'strategy': 'direct_qualification'
        }
    
    # Para torneos de copa directa
    else:
        team_entries = list(TeamEntry.objects.filter(tournament=tournament))
        random.shuffle(team_entries)
        
        return {
            'stage': 'quarterfinal',
            'required_teams': len(team_entries),
            'qualified_teams': team_entries,
            'strategy': 'direct_qualification'
        }

def generate_smart_knockout_bracket(tournament):
    """
    Genera eliminatorias inteligentemente según la cantidad de equipos.
    Crea un bracket completo desde la etapa inicial hasta la final.
    """
    # Determinar etapa y equipos necesarios
    stage_info = determine_knockout_stage_and_teams(tournament)
    
    qualified_teams = stage_info['qualified_teams']
    required_teams = stage_info['required_teams']
    initial_stage = stage_info['stage']
    strategy = stage_info['strategy']
    
    matches_created = []
    
    if strategy == 'playoff_qualification':
        # Necesitamos generar partidos de repechaje
        qualified_teams, playoff_matches = generate_playoff_qualification_matches(
            tournament, qualified_teams, required_teams
        )
        matches_created.extend(playoff_matches)
        
        # Los equipos que pasen de los playoffs se agregarán después
        # Por ahora, generamos el bracket con los equipos que tenemos
        if len(qualified_teams) >= 2:
            knockout_matches = generate_complete_knockout_bracket(tournament, qualified_teams, initial_stage)
            matches_created.extend(knockout_matches)
    else:
        # Clasificación directa
        if len(qualified_teams) >= 2:
            knockout_matches = generate_complete_knockout_bracket(tournament, qualified_teams, initial_stage)
            matches_created.extend(knockout_matches)
    
    return {
        'stage': initial_stage,
        'qualified_teams': len(qualified_teams),
        'required_teams': required_teams,
        'strategy': strategy,
        'matches_created': matches_created
    }

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
    
    # Calcular cuántos equipos deben clasificar en total según la lógica de eliminatorias
    stage_info = determine_knockout_stage_and_teams(tournament)
    required_teams = stage_info['required_teams']
    current_qualified = len(qualified_teams['group_winners']) + len(qualified_teams['group_runners_up'])
    needed_third_place = max(0, required_teams - current_qualified)
    qualified_teams['best_third_place'] = all_thirds[:needed_third_place]
    
    # Calcular total
    qualified_teams['total_qualified'] = (
        len(qualified_teams['group_winners']) + 
        len(qualified_teams['group_runners_up']) + 
        len(qualified_teams['best_third_place'])
    )
    
    return qualified_teams

