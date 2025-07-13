from .models import Player, GameTeam, Match, Tournament, TournamentStanding, GroupStanding

def update_player_stats(player_id):
    """Actualiza las estadísticas de un jugador basado en sus partidos"""
    try:
        player = Player.objects.get(id=player_id)
        
        # Obtener todos los partidos donde participó el jugador
        matches = Match.objects.filter(
            participants__players=player,
            played=True
        )
        
        total_matches = 0
        wins = 0
        losses = 0
        draws = 0
        goals_scored = 0
        goals_conceded = 0
        
        for match in matches:
            participants = list(match.participants.all())
            if len(participants) < 2:
                continue
                
            # Encontrar el team_entry del jugador
            player_entry = None
            opponent_entry = None
            
            for entry in participants:
                if player in entry.players.all():
                    player_entry = entry
                else:
                    opponent_entry = entry
            
            if not player_entry or not opponent_entry:
                continue
            
            player_goals = match.goals.get(str(player_entry.id), 0)
            opponent_goals = match.goals.get(str(opponent_entry.id), 0)
            
            total_matches += 1
            goals_scored += player_goals
            goals_conceded += opponent_goals
            
            if player_goals > opponent_goals:
                wins += 1
            elif player_goals < opponent_goals:
                losses += 1
            else:
                draws += 1
        
        # Actualizar estadísticas del jugador
        player.total_matches = total_matches
        player.wins = wins
        player.losses = losses
        player.draws = draws
        player.goals_scored = goals_scored
        player.goals_conceded = goals_conceded
        player.save()
        
    except Player.DoesNotExist:
        pass

def update_team_stats(team_id):
    """Actualiza las estadísticas de un equipo basado en sus partidos"""
    try:
        team = GameTeam.objects.get(id=team_id)
        
        # Obtener todos los partidos donde participó el equipo
        matches = Match.objects.filter(
            participants__assigned_team=team,
            played=True
        )
        
        total_matches = 0
        wins = 0
        losses = 0
        draws = 0
        goals_scored = 0
        goals_conceded = 0
        
        for match in matches:
            participants = list(match.participants.all())
            if len(participants) < 2:
                continue
                
            # Encontrar el team_entry del equipo
            team_entry = None
            opponent_entry = None
            
            for entry in participants:
                if entry.assigned_team == team:
                    team_entry = entry
                else:
                    opponent_entry = entry
            
            if not team_entry or not opponent_entry:
                continue
            
            team_goals = match.goals.get(str(team_entry.id), 0)
            opponent_goals = match.goals.get(str(opponent_entry.id), 0)
            
            total_matches += 1
            goals_scored += team_goals
            goals_conceded += opponent_goals
            
            if team_goals > opponent_goals:
                wins += 1
            elif team_goals < opponent_goals:
                losses += 1
            else:
                draws += 1
        
        # Actualizar estadísticas del equipo
        team.total_matches = total_matches
        team.wins = wins
        team.losses = losses
        team.draws = draws
        team.goals_scored = goals_scored
        team.goals_conceded = goals_conceded
        team.save()
        
    except GameTeam.DoesNotExist:
        pass

def update_tournament_status(tournament_id):
    """Actualiza el estado de un torneo basado en sus partidos"""
    try:
        tournament = Tournament.objects.get(id=tournament_id)
        
        # Contar partidos totales y jugados
        total_matches = Match.objects.filter(tournament=tournament).count()
        played_matches = Match.objects.filter(tournament=tournament, played=True).count()
        
        # Determinar estado
        if total_matches == 0:
            status = 'draft'
        elif played_matches == 0:
            status = 'active'
        elif played_matches == total_matches:
            status = 'completed'
        else:
            status = 'active'
        
        tournament.status = status
        tournament.save()
        
    except Tournament.DoesNotExist:
        pass

def generate_league_matches(tournament):
    """Genera todos los partidos de una liga (todos contra todos)"""
    from .models import TeamEntry
    
    entries = list(TeamEntry.objects.filter(tournament=tournament))
    
    if len(entries) < 2:
        return []
    
    matches = []
    round_number = 1
    
    # Generar todos los emparejamientos posibles
    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            match = Match.objects.create(
                tournament=tournament,
                stage='league',
                round=round_number,
                scheduled_at=None
            )
            match.participants.add(entries[i], entries[j])
            matches.append(match)
    
    return matches

def update_tournament_standings(tournament_id):
    """Actualiza la clasificación de un torneo"""
    try:
        tournament = Tournament.objects.get(id=tournament_id)
        
        # Obtener todos los partidos jugados de liga
        matches = Match.objects.filter(
            tournament=tournament,
            played=True,
            stage='league'
        )
        
        # Limpiar clasificación actual
        TournamentStanding.objects.filter(tournament=tournament).delete()
        
        # Crear diccionario para acumular estadísticas
        standings_data = {}
        
        for match in matches:
            participants = list(match.participants.all())
            if len(participants) < 2:
                continue
            
            team1_entry = participants[0]
            team2_entry = participants[1]
            
            team1_goals = match.goals.get(str(team1_entry.id), 0)
            team2_goals = match.goals.get(str(team2_entry.id), 0)
            
            # Inicializar datos si no existen
            if team1_entry.id not in standings_data:
                standings_data[team1_entry.id] = {
                    'team_entry': team1_entry,
                    'matches_played': 0, 'wins': 0, 'draws': 0, 'losses': 0,
                    'goals_for': 0, 'goals_against': 0, 'points': 0
                }
            if team2_entry.id not in standings_data:
                standings_data[team2_entry.id] = {
                    'team_entry': team2_entry,
                    'matches_played': 0, 'wins': 0, 'draws': 0, 'losses': 0,
                    'goals_for': 0, 'goals_against': 0, 'points': 0
                }
            
            # Actualizar estadísticas
            standings_data[team1_entry.id]['matches_played'] += 1
            standings_data[team2_entry.id]['matches_played'] += 1
            
            standings_data[team1_entry.id]['goals_for'] += team1_goals
            standings_data[team1_entry.id]['goals_against'] += team2_goals
            standings_data[team2_entry.id]['goals_for'] += team2_goals
            standings_data[team2_entry.id]['goals_against'] += team1_goals
            
            if team1_goals > team2_goals:
                standings_data[team1_entry.id]['wins'] += 1
                standings_data[team1_entry.id]['points'] += 3
                standings_data[team2_entry.id]['losses'] += 1
            elif team2_goals > team1_goals:
                standings_data[team2_entry.id]['wins'] += 1
                standings_data[team2_entry.id]['points'] += 3
                standings_data[team1_entry.id]['losses'] += 1
            else:
                standings_data[team1_entry.id]['draws'] += 1
                standings_data[team1_entry.id]['points'] += 1
                standings_data[team2_entry.id]['draws'] += 1
                standings_data[team2_entry.id]['points'] += 1
        
        # Crear registros de clasificación
        for data in standings_data.values():
            TournamentStanding.objects.create(
                tournament=tournament,
                team_entry=data['team_entry'],
                matches_played=data['matches_played'],
                wins=data['wins'],
                draws=data['draws'],
                losses=data['losses'],
                goals_for=data['goals_for'],
                goals_against=data['goals_against'],
                points=data['points']
            )
        
    except Tournament.DoesNotExist:
        pass 

def update_group_standings(tournament_id):
    """Actualiza las clasificaciones de grupos de un torneo"""
    from .models import GroupStanding
    
    try:
        tournament = Tournament.objects.get(id=tournament_id)
        
        # Obtener todos los partidos jugados de grupos
        matches = Match.objects.filter(
            tournament=tournament,
            played=True,
            stage='group'
        )
        
        # Limpiar clasificaciones actuales
        GroupStanding.objects.filter(tournament=tournament).delete()
        
        # Crear diccionario para acumular estadísticas por grupo
        group_standings_data = {}
        
        for match in matches:
            participants = list(match.participants.all())
            if len(participants) < 2:
                continue
            
            team1_entry = participants[0]
            team2_entry = participants[1]
            group_code = match.group_code
            
            if not group_code:
                continue
            
            team1_goals = match.goals.get(str(team1_entry.id), 0)
            team2_goals = match.goals.get(str(team2_entry.id), 0)
            
            # Inicializar datos si no existen
            if team1_entry.id not in group_standings_data:
                group_standings_data[team1_entry.id] = {
                    'team_entry': team1_entry,
                    'group_code': group_code,
                    'matches_played': 0, 'wins': 0, 'draws': 0, 'losses': 0,
                    'goals_for': 0, 'goals_against': 0, 'points': 0
                }
            if team2_entry.id not in group_standings_data:
                group_standings_data[team2_entry.id] = {
                    'team_entry': team2_entry,
                    'group_code': group_code,
                    'matches_played': 0, 'wins': 0, 'draws': 0, 'losses': 0,
                    'goals_for': 0, 'goals_against': 0, 'points': 0
                }
            
            # Actualizar estadísticas
            group_standings_data[team1_entry.id]['matches_played'] += 1
            group_standings_data[team2_entry.id]['matches_played'] += 1
            
            group_standings_data[team1_entry.id]['goals_for'] += team1_goals
            group_standings_data[team1_entry.id]['goals_against'] += team2_goals
            group_standings_data[team2_entry.id]['goals_for'] += team2_goals
            group_standings_data[team2_entry.id]['goals_against'] += team1_goals
            
            if team1_goals > team2_goals:
                group_standings_data[team1_entry.id]['wins'] += 1
                group_standings_data[team1_entry.id]['points'] += 3
                group_standings_data[team2_entry.id]['losses'] += 1
            elif team2_goals > team1_goals:
                group_standings_data[team2_entry.id]['wins'] += 1
                group_standings_data[team2_entry.id]['points'] += 3
                group_standings_data[team1_entry.id]['losses'] += 1
            else:
                group_standings_data[team1_entry.id]['draws'] += 1
                group_standings_data[team1_entry.id]['points'] += 1
                group_standings_data[team2_entry.id]['draws'] += 1
                group_standings_data[team2_entry.id]['points'] += 1
        
        # Crear registros de clasificación de grupos
        for data in group_standings_data.values():
            GroupStanding.objects.create(
                tournament=tournament,
                group_code=data['group_code'],
                team_entry=data['team_entry'],
                points=data['points'],
                goals_for=data['goals_for'],
                goals_against=data['goals_against'],
                matches_played=data['matches_played'],
                wins=data['wins'],
                draws=data['draws'],
                losses=data['losses']
            )
        
    except Tournament.DoesNotExist:
        pass 