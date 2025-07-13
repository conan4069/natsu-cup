from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    Tournament, Player, GameTeam, TeamEntry, Match, TournamentStanding, GroupStanding
)
from .serializers import (
    TournamentSerializer, PlayerSerializer,
    GameTeamSerializer, TeamEntrySerializer,
    MatchSerializer
)
from .brackets import generate_group_matches, get_qualified_teams_for_knockout

import random

# 🏆 Torneos
class TournamentListCreateView(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class TournamentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class TeamEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = TeamEntrySerializer
    
    def get_queryset(self):
        tournament_id = self.kwargs.get('tournament_id')
        return TeamEntry.objects.filter(tournament_id=tournament_id)
    
    def perform_create(self, serializer):
        tournament_id = self.kwargs.get('tournament_id')
        serializer.save(tournament_id=tournament_id)
    
    def get_serializer_context(self):
        return {'request': self.request}

# ⚔️ Generación de fase de grupos
class GenerateGroupMatchesView(views.APIView):
    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)

        entries = TeamEntry.objects.filter(tournament=tournament).prefetch_related('players', 'assigned_team')
        if not tournament.has_group_stage:
            return Response({'error': 'Group stage is disabled in this tournament'}, status=400)
        if not entries.exists():
            return Response({'error': 'No team entries registered'}, status=400)

        # Agrupar por códigos: A, B, C...
        group_size = tournament.teams_per_group
        group_map = {}
        sorted_entries = list(entries)
        
        for i in range(0, len(sorted_entries), group_size):
            group_code = chr(ord('A') + i // group_size)
            group_map[group_code] = sorted_entries[i:i+group_size]

        # Generar partidos (solo los que faltan)
        matches_created = generate_group_matches(tournament, group_map)

        # Preparar respuesta con información detallada
        response_data = {
            'message': f'{len(matches_created)} nuevos partidos de grupo generados',
            'matches_created': len(matches_created),
            'groups': {}
        }

        # Agregar información de cada grupo
        for group_code, team_entries in group_map.items():
            group_info = {
                'code': group_code,
                'teams': []
            }
            
            for entry in team_entries:
                team_info = {
                    'id': entry.id,
                    'players': [
                        {
                            'id': player.id,
                            'display_name': player.display_name,
                            'avatar': request.build_absolute_uri(player.avatar.url) if player.avatar else None
                        }
                        for player in entry.players.all()
                    ],
                    'assigned_team': {
                        'id': entry.assigned_team.id,
                        'name': entry.assigned_team.name,
                        'logo': request.build_absolute_uri(entry.assigned_team.logo.url) if entry.assigned_team.logo else None
                    } if entry.assigned_team else None,
                    'team_name': str(entry)
                }
                group_info['teams'].append(team_info)
            
            response_data['groups'][group_code] = group_info

        return Response(response_data, status=201)

# 👥 Jugadores
class PlayerListView(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class PlayerCreateView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class PlayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class PlayerStatsView(views.APIView):
    def get(self, request, player_id):
        try:
            player = Player.objects.get(pk=player_id)
        except Player.DoesNotExist:
            return Response({'error': 'Player not found'}, status=404)
        
        # Obtener todas las entradas del jugador (solo las que realmente participan)
        team_entries = TeamEntry.objects.filter(players=player).distinct()
        
        # Estadísticas básicas
        total_tournaments = team_entries.count()
        total_matches = 0
        wins = 0
        losses = 0
        draws = 0
        
        # Calcular estadísticas de partidos
        for entry in team_entries:
            # Solo partidos donde este TeamEntry específico participa
            matches = Match.objects.filter(
                participants=entry,
                played=True
            ).distinct()
            
            total_matches += matches.count()
            
            for match in matches:
                goals = match.goals
                if goals and str(entry.id) in goals:
                    # Obtener goles del equipo del jugador
                    entry_goals = goals.get(str(entry.id), 0)
                    other_goals = sum(g for k, g in goals.items() if k != str(entry.id))
                    
                    if entry_goals > other_goals:
                        wins += 1
                    elif entry_goals < other_goals:
                        losses += 1
                    else:
                        draws += 1
        
        # Calcular porcentajes
        win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
        loss_rate = (losses / total_matches * 100) if total_matches > 0 else 0
        draw_rate = (draws / total_matches * 100) if total_matches > 0 else 0
        
        stats = {
            'player_id': player.id,
            'player_name': player.display_name,
            'total_tournaments': total_tournaments,
            'total_matches': total_matches,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'win_rate': round(win_rate, 1),
            'loss_rate': round(loss_rate, 1),
            'draw_rate': round(draw_rate, 1),
            'total_points': wins * 3 + draws,
        }
        
        return Response(stats)

class PlayerTournamentsView(views.APIView):
    def get(self, request, player_id):
        try:
            player = Player.objects.get(pk=player_id)
        except Player.DoesNotExist:
            return Response({'error': 'Player not found'}, status=404)
        
        # Obtener todas las entradas del jugador con información del torneo
        team_entries = TeamEntry.objects.filter(
            players=player
        ).select_related('tournament', 'assigned_team').distinct()
        
        tournaments = []
        for entry in team_entries:
            tournament = entry.tournament
            
            # Obtener estadísticas del jugador en este torneo específico
            tournament_matches = Match.objects.filter(
                participants=entry,
                played=True
            ).distinct()
            
            tournament_wins = 0
            tournament_losses = 0
            tournament_draws = 0
            
            for match in tournament_matches:
                goals = match.goals
                if goals and str(entry.id) in goals:
                    entry_goals = goals.get(str(entry.id), 0)
                    other_goals = sum(g for k, g in goals.items() if k != str(entry.id))
                    
                    if entry_goals > other_goals:
                        tournament_wins += 1
                    elif entry_goals < other_goals:
                        tournament_losses += 1
                    else:
                        tournament_draws += 1
            
            # Calcular estadísticas
            total_matches = tournament_wins + tournament_losses + tournament_draws
            points = tournament_wins * 3 + tournament_draws
            
            tournaments.append({
                'id': tournament.id,
                'name': tournament.name,
                'format': tournament.format,
                'entry_id': entry.id,
                'assigned_team': entry.assigned_team.name if entry.assigned_team else None,
                'matches_played': total_matches,
                'wins': tournament_wins,
                'losses': tournament_losses,
                'draws': tournament_draws,
                'points': points,
                'win_rate': round((tournament_wins / total_matches * 100) if total_matches > 0 else 0, 1),
                'status': 'completed' if total_matches > 0 else 'registered'
            })
        
        # Ordenar por fecha de creación (más recientes primero)
        tournaments.sort(key=lambda x: x['id'], reverse=True)
        
        return Response({
            'player_id': player.id,
            'player_name': player.display_name,
            'tournaments': tournaments,
            'total_tournaments': len(tournaments)
        })

# ��️ Equipos del juego CRUD
class GameTeamListCreateView(generics.ListCreateAPIView):
    queryset = GameTeam.objects.all()
    serializer_class = GameTeamSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class GameTeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameTeam.objects.all()
    serializer_class = GameTeamSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class GameTeamStatsView(views.APIView):
    def get(self, request, team_id):
        try:
            team = GameTeam.objects.get(pk=team_id)
        except GameTeam.DoesNotExist:
            return Response({'error': 'Team not found'}, status=404)
        
        # Obtener todas las entradas donde este equipo fue asignado
        team_entries = TeamEntry.objects.filter(assigned_team=team)
        
        # Estadísticas básicas
        total_tournaments = team_entries.count()
        total_matches = 0
        wins = 0
        losses = 0
        draws = 0
        
        # Calcular estadísticas de partidos
        for entry in team_entries:
            matches = Match.objects.filter(participants=entry, played=True)
            total_matches += matches.count()
            
            for match in matches:
                goals = match.goals
                if goals:
                    # Obtener goles del equipo
                    entry_goals = goals.get(str(entry.id), 0)
                    other_goals = sum(g for k, g in goals.items() if k != str(entry.id))
                    
                    if entry_goals > other_goals:
                        wins += 1
                    elif entry_goals < other_goals:
                        losses += 1
                    else:
                        draws += 1
        
        # Calcular porcentajes
        win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
        loss_rate = (losses / total_matches * 100) if total_matches > 0 else 0
        draw_rate = (draws / total_matches * 100) if total_matches > 0 else 0
        
        stats = {
            'team_id': team.id,
            'team_name': team.name,
            'total_tournaments': total_tournaments,
            'total_matches': total_matches,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'win_rate': round(win_rate, 1),
            'loss_rate': round(loss_rate, 1),
            'draw_rate': round(draw_rate, 1),
            'total_points': wins * 3 + draws,  # Sistema de puntos: 3 por victoria, 1 por empate
        }
        
        return Response(stats)

class GameTeamTournamentsView(views.APIView):
    def get(self, request, team_id):
        try:
            team = GameTeam.objects.get(pk=team_id)
        except GameTeam.DoesNotExist:
            return Response({'error': 'Team not found'}, status=404)
        
        # Obtener todas las entradas del equipo con información del torneo
        team_entries = TeamEntry.objects.filter(assigned_team=team).select_related('tournament')
        
        tournaments = []
        for entry in team_entries:
            tournament = entry.tournament
            
            # Obtener estadísticas del equipo en este torneo
            tournament_matches = Match.objects.filter(
                participants=entry,
                played=True
            )
            
            tournament_wins = 0
            tournament_losses = 0
            tournament_draws = 0
            
            for match in tournament_matches:
                goals = match.goals
                if goals:
                    entry_goals = goals.get(str(entry.id), 0)
                    other_goals = sum(g for k, g in goals.items() if k != str(entry.id))
                    
                    if entry_goals > other_goals:
                        tournament_wins += 1
                    elif entry_goals < other_goals:
                        tournament_losses += 1
                    else:
                        tournament_draws += 1
            
            # Calcular posición (simplificado)
            total_matches = tournament_wins + tournament_losses + tournament_draws
            points = tournament_wins * 3 + tournament_draws
            
            tournaments.append({
                'id': tournament.id,
                'name': tournament.name,
                'format': tournament.format,
                'entry_id': entry.id,
                'matches_played': total_matches,
                'wins': tournament_wins,
                'losses': tournament_losses,
                'draws': tournament_draws,
                'points': points,
                'win_rate': round((tournament_wins / total_matches * 100) if total_matches > 0 else 0, 1),
                'status': 'completed' if total_matches > 0 else 'registered'
            })
        
        # Ordenar por fecha de creación (más recientes primero)
        tournaments.sort(key=lambda x: x['id'], reverse=True)
        
        return Response({
            'team_id': team.id,
            'team_name': team.name,
            'tournaments': tournaments,
            'total_tournaments': len(tournaments)
        })

class MatchView(APIView):
    def get(self, request, match_id):
        try:
            match = Match.objects.get(pk=match_id)
        except Match.DoesNotExist:
            return Response({'error': 'Match not found'}, status=404)
        
        # Usar el serializer existente
        serializer = MatchSerializer(match, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, match_id):
        try:
            match = Match.objects.get(pk=match_id)
        except Match.DoesNotExist:
            return Response({'error': 'Match not found'}, status=404)
        
        # Actualizar partido completo
        serializer = MatchSerializer(match, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, match_id):
        try:
            match = Match.objects.get(pk=match_id)
        except Match.DoesNotExist:
            return Response({'error': 'Match not found'}, status=404)
        
        try:
            data = request.data
            goals = data.get('goals', {})
            
            # Validar que hay goles
            if not goals:
                return Response({'error': 'Se requieren los goles de ambos equipos'}, status=400)
            
            # Actualizar partido
            match.played = True
            match.goals = goals
            match.save()
            
            # Actualizar clasificación del torneo
            self.update_tournament_standings(match.tournament)
            
            return Response({
                'message': 'Resultado guardado exitosamente',
                'match_id': match.id
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def update_tournament_standings(self, tournament):
        """Actualizar clasificación del torneo después de guardar un resultado"""
        # Obtener todos los partidos jugados del torneo
        matches = Match.objects.filter(tournament=tournament, played=True)
        
        # Calcular estadísticas por equipo
        team_stats = {}
        
        for match in matches:
            # Usar TeamEntry en lugar de Participant
            team_entries = match.team_entries.all()
            if len(team_entries) != 2:
                continue
                
            team1 = team_entries[0].assigned_team
            team2 = team_entries[1].assigned_team
            
            team1_goals = match.goals.get(str(team_entries[0].id), 0)
            team2_goals = match.goals.get(str(team_entries[1].id), 0)
            
            # Actualizar estadísticas de equipo 1
            if team1 not in team_stats:
                team_stats[team1] = {'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}
            
            team_stats[team1]['goals_for'] += team1_goals
            team_stats[team1]['goals_against'] += team2_goals
            
            if team1_goals > team2_goals:
                team_stats[team1]['wins'] += 1
            elif team1_goals == team2_goals:
                team_stats[team1]['draws'] += 1
            else:
                team_stats[team1]['losses'] += 1
            
            # Actualizar estadísticas de equipo 2
            if team2 not in team_stats:
                team_stats[team2] = {'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}
            
            team_stats[team2]['goals_for'] += team2_goals
            team_stats[team2]['goals_against'] += team1_goals
            
            if team2_goals > team1_goals:
                team_stats[team2]['wins'] += 1
            elif team2_goals == team1_goals:
                team_stats[team2]['draws'] += 1
            else:
                team_stats[team2]['losses'] += 1
        
        # Actualizar o crear registros de clasificación
        for team, stats in team_stats.items():
            matches_played = stats['wins'] + stats['draws'] + stats['losses']
            points = (stats['wins'] * 3) + stats['draws']
            goal_difference = stats['goals_for'] - stats['goals_against']
            
            TournamentStanding.objects.update_or_create(
                tournament=tournament,
                team=team,
                defaults={
                    'matches_played': matches_played,
                    'wins': stats['wins'],
                    'draws': stats['draws'],
                    'losses': stats['losses'],
                    'goals_for': stats['goals_for'],
                    'goals_against': stats['goals_against'],
                    'goal_difference': goal_difference,
                    'points': points
                }
            )

class TeamEntryDeleteView(generics.DestroyAPIView):
  queryset = TeamEntry.objects.all()
  serializer_class = TeamEntrySerializer
  
  def get_serializer_context(self):
    return {'request': self.request}

class AssignRandomTeamsView(APIView):
  def post(self, request, tournament_id):
    try:
      tournament = Tournament.objects.get(pk=tournament_id)
    except Tournament.DoesNotExist:
      return Response({'error': 'Tournament not found'}, status=404)

    # Obtener todas las entradas del torneo (no solo las sin equipo asignado)
    entries = TeamEntry.objects.filter(tournament=tournament)
    available_teams = list(GameTeam.objects.all())

    if len(available_teams) < entries.count():
      return Response({'error': 'Not enough available teams'}, status=400)

    # Mezclar equipos disponibles
    random.shuffle(available_teams)
    
    # Asignar equipos a todas las entradas
    for entry, team in zip(entries, available_teams):
      entry.assigned_team = team
      entry.save()

    return Response({
      'message': f'{entries.count()} teams assigned randomly',
      'assigned_entries': entries.count()
    }, status=200)

class CompleteKnockoutStageView(APIView):
    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        stage_data = request.data.get('stage', 'semifinal')
        
        # Manejar diferentes etapas
        if stage_data == 'quarterfinal':
            # Generar cuartos de final (primera etapa)
            return self.generate_first_stage(tournament, 'quarterfinal')
        elif stage_data == 'semifinal':
            # Completar semifinales
            return self.complete_next_stage(tournament, 'quarterfinal', 'semifinal')
        elif stage_data == 'final':
            # Completar final
            return self.complete_next_stage(tournament, 'semifinal', 'final')
        else:
            return Response({'error': 'Invalid stage. Must be quarterfinal, semifinal, or final'}, status=400)
    
    def generate_first_stage(self, tournament, stage):
        """Genera la primera etapa de eliminatorias"""
        from .brackets import get_qualified_teams_for_knockout
        
        # Obtener equipos clasificados
        qualified_teams_data = get_qualified_teams_for_knockout(tournament)
        
        # Combinar todos los equipos clasificados
        all_qualified = []
        all_qualified.extend([team['team_entry'] for team in qualified_teams_data['group_winners']])
        all_qualified.extend([team['team_entry'] for team in qualified_teams_data['group_runners_up']])
        all_qualified.extend([team['team_entry'] for team in qualified_teams_data['best_third_place']])
        
        if len(all_qualified) < 2:
            return Response({'error': 'Not enough qualified teams'}, status=400)
        
        # Generar partidos de la primera etapa
        from .brackets import generate_knockout_bracket
        matches = generate_knockout_bracket(tournament, all_qualified, stage)
        
        return Response({
            'message': f'{stage.capitalize()} stage generated with {len(all_qualified)} teams',
            'winners_count': len(all_qualified),
            'matches_created': len(matches),
            'stage': stage,
            'qualified_teams': len(all_qualified)
        }, status=201)
    
    def complete_next_stage(self, tournament, previous_stage, next_stage):
        """Completa la siguiente etapa basada en los ganadores de la anterior"""
        # Obtener partidos de la etapa anterior
        previous_matches = Match.objects.filter(
            tournament=tournament,
            stage=previous_stage,
            played=True
        )
        
        if not previous_matches.exists():
            return Response({'error': f'No completed matches found for {previous_stage} stage'}, status=400)
        
        # Obtener ganadores
        winners = []
        for match in previous_matches:
            # Usar TeamEntry en lugar de Participant
            team_entries = match.team_entries.all()
            if len(team_entries) != 2:
                continue
                
            team1 = team_entries[0].assigned_team
            team2 = team_entries[1].assigned_team
            
            goals = match.goals or {}
            
            if team1 and team2:
                team1_goals = goals.get(str(team_entries[0].id), 0)
                team2_goals = goals.get(str(team_entries[1].id), 0)
                
                if team1_goals > team2_goals:
                    winners.append(team1)
                elif team2_goals > team1_goals:
                    winners.append(team2)
        
        if len(winners) < 2:
            return Response({'error': 'Not enough winners to generate next stage'}, status=400)
        
        # Buscar partidos existentes de la siguiente etapa
        existing_matches = Match.objects.filter(
            tournament=tournament,
            stage=next_stage
        ).order_by('id')
        
        if existing_matches.exists():
            # Actualizar partidos existentes con los ganadores
            for i, match in enumerate(existing_matches):
                if i * 2 < len(winners):
                    match.team_entries.set([winners[i * 2]])
                if i * 2 + 1 < len(winners):
                    match.team_entries.add(winners[i * 2 + 1])
                match.save()
        else:
            # Generar nuevos partidos
            from .brackets import generate_knockout_bracket
            matches = generate_knockout_bracket(tournament, winners, next_stage)
        
        return Response({
            'message': f'{next_stage.capitalize()} stage completed with {len(winners)} teams',
            'winners_count': len(winners),
            'matches_updated': existing_matches.count() if existing_matches.exists() else len(matches),
            'stage': next_stage
        }, status=201)

class GenerateLeagueMatchesView(APIView):
    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        try:
            # Obtener equipos del torneo
            entries = TeamEntry.objects.filter(tournament=tournament)
            teams = [entry.assigned_team for entry in entries if entry.assigned_team]
            
            if len(teams) < 2:
                return Response({'error': 'Se necesitan al menos 2 equipos para generar partidos'}, status=400)
            
            # Generar todos los partidos posibles (todos contra todos)
            matches_created = []
            for i, team1 in enumerate(teams):
                for j, team2 in enumerate(teams):
                    if i < j:  # Evitar partidos duplicados y contra sí mismo
                        match = Match.objects.create(
                            tournament=tournament,
                            stage='league',
                            played=False,
                            goals={}
                        )
                        
                        # Crear participantes
                        team1_entry = TeamEntry.objects.create(
                            match=match,
                            assigned_team=team1,
                            position=0
                        )
                        team2_entry = TeamEntry.objects.create(
                            match=match,
                            assigned_team=team2,
                            position=1
                        )
                        
                        matches_created.append(match)
            
            return Response({
                'message': f'Se generaron {len(matches_created)} partidos de liga',
                'matches_count': len(matches_created)
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class GeneratePlayoffsView(APIView):
    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        try:
            # Obtener clasificación de la liga
            standings = TournamentStanding.objects.filter(tournament=tournament).order_by('-points', '-goal_difference', '-goals_for')
            
            # Tomar los mejores equipos según playoff_teams
            playoff_count = tournament.playoff_teams or 4
            qualified_teams = list(standings[:playoff_count])
            
            if len(qualified_teams) < 2:
                return Response({'error': 'Se necesitan al menos 2 equipos clasificados para generar playoffs'}, status=400)
            
            # Generar partidos de playoffs
            matches_created = []
            for i in range(0, len(qualified_teams), 2):
                if i + 1 < len(qualified_teams):
                    team1 = qualified_teams[i].team
                    team2 = qualified_teams[i + 1].team
                    
                    match = Match.objects.create(
                        tournament=tournament,
                        stage='playoff',
                        played=False,
                        goals={}
                    )
                    
                    # Crear participantes
                    team1_entry = TeamEntry.objects.create(
                        match=match,
                        assigned_team=team1,
                        position=0
                    )
                    team2_entry = TeamEntry.objects.create(
                        match=match,
                        assigned_team=team2,
                        position=1
                    )
                    
                    matches_created.append(match)
            
            return Response({
                'message': f'Se generaron {len(matches_created)} partidos de playoffs',
                'matches_count': len(matches_created),
                'qualified_teams': len(qualified_teams)
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class TournamentStandingsView(APIView):
    def get(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        try:
            # Obtener clasificación del torneo
            standings = TournamentStanding.objects.filter(tournament=tournament).order_by('-points', '-goal_difference', '-goals_for')
            
            # Serializar datos
            standings_data = []
            for standing in standings:
                standings_data.append({
                    'id': standing.team.id,
                    'name': standing.team.name,
                    'logo': standing.team.logo.url if standing.team.logo else None,
                    'matches_played': standing.matches_played,
                    'wins': standing.wins,
                    'draws': standing.draws,
                    'losses': standing.losses,
                    'goals_for': standing.goals_for,
                    'goals_against': standing.goals_against,
                    'goal_difference': standing.goal_difference,
                    'points': standing.points,
                    'position': standings_data.index(standing) + 1
                })
            
            return Response(standings_data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class GroupStandingsView(APIView):
    def get(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        try:
            # Obtener clasificaciones de grupos
            group_standings = GroupStanding.objects.filter(tournament=tournament).order_by(
                'group_code', '-points', '-goal_difference', '-goals_for'
            )
            
            # Agrupar por código de grupo
            standings_by_group = {}
            for standing in group_standings:
                group_code = standing.group_code
                if group_code not in standings_by_group:
                    standings_by_group[group_code] = []
                
                standing_data = {
                    'id': standing.team.id,
                    'name': standing.team.name,
                    'logo_url': request.build_absolute_uri(standing.team.logo.url) if standing.team.logo else None,
                    'group_code': standing.group_code,
                    'matches_played': standing.matches_played,
                    'wins': standing.wins,
                    'draws': standing.draws,
                    'losses': standing.losses,
                    'goals_for': standing.goals_for,
                    'goals_against': standing.goals_against,
                    'goal_difference': standing.goal_difference,
                    'points': standing.points,
                    'position': len(standings_by_group[group_code]) + 1
                }
                standings_by_group[group_code].append(standing_data)
            
            return Response(standings_by_group)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class GenerateKnockoutStageView(APIView):
    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        try:
            # Obtener equipos clasificados
            qualified_teams_data = get_qualified_teams_for_knockout(tournament)
            
            # Determinar estrategia según cantidad de equipos
            total_teams = qualified_teams_data['total_qualified']
            
            if total_teams <= 2:
                # Generar final directamente
                stage = 'final'
                strategy = 'direct_final'
            elif total_teams <= 4:
                # Generar semifinales
                stage = 'semifinal'
                strategy = 'semifinals'
            elif total_teams <= 8:
                # Generar cuartos de final
                stage = 'quarterfinal'
                strategy = 'quarterfinals'
            else:
                # Generar octavos de final
                stage = 'round_of_16'
                strategy = 'round_of_16'
            
            # Generar partidos usando la función existente
            from .brackets import generate_knockout_bracket
            qualified_teams = []
            for team_list in [qualified_teams_data['group_winners'], qualified_teams_data['group_runners_up'], qualified_teams_data['best_third_place']]:
                qualified_teams.extend(team_list)
            
            matches_created = generate_knockout_bracket(tournament, qualified_teams, stage)
            
            return Response({
                'message': f'Fase eliminatoria generada: {stage}',
                'strategy': strategy,
                'stage': stage,
                'qualified_teams': len(qualified_teams),
                'matches_created': len(matches_created)
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class QualifiedTeamsView(APIView):
    def get(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        try:
            # Obtener equipos clasificados
            qualified_teams_data = get_qualified_teams_for_knockout(tournament)
            
            return Response(qualified_teams_data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class CompletePlayoffQualificationView(APIView):
    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        try:
            # Obtener partidos de calificación de playoffs
            playoff_matches = Match.objects.filter(
                tournament=tournament,
                stage='playoff_qualification',
                played=True
            )
            
            if not playoff_matches.exists():
                return Response({'error': 'No hay partidos de calificación completados'}, status=400)
            
            # Obtener ganadores de los playoffs
            winners = []
            for match in playoff_matches:
                goals = match.goals
                if goals:
                    # Encontrar el participante con más goles
                    max_goals = 0
                    winner_participant = None
                    
                    for participant in match.participants.all():
                        participant_goals = goals.get(str(participant.id), 0)
                        if participant_goals > max_goals:
                            max_goals = participant_goals
                            winner_participant = participant
                    
                    if winner_participant and winner_participant.assigned_team:
                        winners.append(winner_participant.assigned_team)
            
            # Generar siguiente etapa con los ganadores
            if len(winners) >= 2:
                from .brackets import generate_knockout_bracket
                matches_created = generate_knockout_bracket(tournament, winners, 'quarterfinal')
                
                return Response({
                    'message': f'Calificación de playoffs completada. {len(winners)} equipos avanzan.',
                    'winners_count': len(winners),
                    'matches_created': len(matches_created)
                })
            else:
                return Response({'error': 'No hay suficientes ganadores para continuar'}, status=400)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class StandingsView(APIView):
    def get(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        standings_type = request.query_params.get('type', 'tournament')
        
        try:
            if standings_type == 'group':
                return self.get_group_standings(tournament, request)
            else:
                return self.get_tournament_standings(tournament, request)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def get_tournament_standings(self, tournament, request):
        """Obtener clasificación del torneo"""
        standings = TournamentStanding.objects.filter(tournament=tournament).order_by('-points', '-goal_difference', '-goals_for')
        
        # Serializar datos
        standings_data = []
        for standing in standings:
            standings_data.append({
                'id': standing.team.id,
                'name': standing.team.name,
                'logo': standing.team.logo.url if standing.team.logo else None,
                'matches_played': standing.matches_played,
                'wins': standing.wins,
                'draws': standing.draws,
                'losses': standing.losses,
                'goals_for': standing.goals_for,
                'goals_against': standing.goals_against,
                'goal_difference': standing.goal_difference,
                'points': standing.points,
                'position': standings_data.index(standing) + 1
            })
        
        return Response(standings_data)
    
    def get_group_standings(self, tournament, request):
        """Obtener clasificaciones de grupos"""
        group_standings = GroupStanding.objects.filter(tournament=tournament).order_by(
            'group_code', '-points', '-goal_difference', '-goals_for'
        )
        
        # Agrupar por código de grupo
        standings_by_group = {}
        for standing in group_standings:
            group_code = standing.group_code
            if group_code not in standings_by_group:
                standings_by_group[group_code] = []
            
            standing_data = {
                'id': standing.team.id,
                'name': standing.team.name,
                'logo_url': request.build_absolute_uri(standing.team.logo.url) if standing.team.logo else None,
                'group_code': standing.group_code,
                'matches_played': standing.matches_played,
                'wins': standing.wins,
                'draws': standing.draws,
                'losses': standing.losses,
                'goals_for': standing.goals_for,
                'goals_against': standing.goals_against,
                'goal_difference': standing.goal_difference,
                'points': standing.points,
                'position': len(standings_by_group[group_code]) + 1
            }
            standings_by_group[group_code].append(standing_data)
        
        return Response(standings_by_group)

class TournamentMatchesView(APIView):
    def get(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        try:
            # Obtener todos los partidos del torneo
            matches = Match.objects.filter(tournament=tournament).prefetch_related(
                'participants__assigned_team',
                'participants__players'
            )
            
            # Serializar partidos
            matches_data = []
            for match in matches:
                participants_data = []
                for participant in match.participants.all():
                    participant_data = {
                        'id': participant.id,
                        'position': participant.position,
                        'assigned_team': {
                            'id': participant.assigned_team.id,
                            'name': participant.assigned_team.name,
                            'logo_url': request.build_absolute_uri(participant.assigned_team.logo.url) if participant.assigned_team.logo else None
                        } if participant.assigned_team else None,
                        'players': [
                            {
                                'id': player.id,
                                'name': player.display_name,
                                'avatar_url': request.build_absolute_uri(player.avatar.url) if player.avatar else None
                            }
                            for player in participant.players.all()
                        ]
                    }
                    participants_data.append(participant_data)
                
                match_data = {
                    'id': match.id,
                    'stage': match.stage,
                    'played': match.played,
                    'goals': match.goals,
                    'participants': participants_data,
                    'created_at': match.created_at,
                    'updated_at': match.updated_at
                }
                matches_data.append(match_data)
            
            return Response(matches_data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class KnockoutStageView(APIView):
    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        try:
            stage_data = request.data.get('stage')
            
            if stage_data:
                # Completar etapa específica
                return self.complete_stage(tournament, stage_data)
            else:
                # Generar nueva etapa
                return self.generate_stage(tournament)
                
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def complete_stage(self, tournament, stage):
        """Completar etapa existente"""
        # Obtener partidos de la etapa anterior
        previous_stage_map = {
            'semifinal': 'quarterfinal',
            'final': 'semifinal'
        }
        
        previous_stage = previous_stage_map.get(stage)
        if not previous_stage:
            return Response({'error': 'Etapa no válida'}, status=400)
        
        # Obtener ganadores de la etapa anterior
        previous_matches = Match.objects.filter(
            tournament=tournament,
            stage=previous_stage,
            played=True
        )
        
        winners = []
        for match in previous_matches:
            goals = match.goals
            if goals:
                # Encontrar el participante con más goles
                max_goals = 0
                winner_participant = None
                
                for participant in match.participants.all():
                    participant_goals = goals.get(str(participant.id), 0)
                    if participant_goals > max_goals:
                        max_goals = participant_goals
                        winner_participant = participant
                
                if winner_participant and winner_participant.assigned_team:
                    winners.append(winner_participant.assigned_team)
        
        if len(winners) < 2:
            return Response({'error': 'No hay suficientes ganadores para continuar'}, status=400)
        
        # Generar partidos de la nueva etapa
        from .brackets import generate_knockout_bracket
        matches_created = generate_knockout_bracket(tournament, winners, stage)
        
        return Response({
            'message': f'Etapa {stage} completada',
            'stage': stage,
            'winners_count': len(winners),
            'matches_created': len(matches_created)
        })
    
    def generate_stage(self, tournament):
        """Generar nueva etapa de eliminatorias"""
        # Obtener equipos clasificados
        qualified_teams_data = get_qualified_teams_for_knockout(tournament)
        
        # Determinar estrategia según cantidad de equipos
        total_teams = qualified_teams_data['total_qualified']
        
        if total_teams <= 2:
            # Generar final directamente
            stage = 'final'
            strategy = 'direct_final'
        elif total_teams <= 4:
            # Generar semifinales
            stage = 'semifinal'
            strategy = 'semifinals'
        elif total_teams <= 8:
            # Generar cuartos de final
            stage = 'quarterfinal'
            strategy = 'quarterfinals'
        else:
            # Generar octavos de final
            stage = 'round_of_16'
            strategy = 'round_of_16'
        
        # Generar partidos usando la función existente
        from .brackets import generate_knockout_bracket
        qualified_teams = []
        for team_list in [qualified_teams_data['group_winners'], qualified_teams_data['group_runners_up'], qualified_teams_data['best_third_place']]:
            qualified_teams.extend(team_list)
        
        matches_created = generate_knockout_bracket(tournament, qualified_teams, stage)
        
        return Response({
            'message': f'Fase eliminatoria generada: {stage}',
            'strategy': strategy,
            'stage': stage,
            'qualified_teams': len(qualified_teams),
            'matches_created': len(matches_created)
        })

class KnockoutPreviewView(APIView):
    def get(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        try:
            # Obtener equipos clasificados
            qualified_teams_data = get_qualified_teams_for_knockout(tournament)
            
            # Determinar estructura de eliminatorias
            total_teams = qualified_teams_data['total_qualified']
            
            # Determinar etapas necesarias
            if total_teams <= 2:
                stages = ['final']
            elif total_teams <= 4:
                stages = ['semifinal', 'final']
            elif total_teams <= 8:
                stages = ['quarterfinal', 'semifinal', 'final']
            else:
                stages = ['round_of_16', 'quarterfinal', 'semifinal', 'final']
            
            preview_data = {
                'tournament_id': tournament.id,
                'total_qualified_teams': total_teams,
                'stages': stages,
                'qualified_teams': qualified_teams_data,
                'estimated_matches': sum(len(stages) * 2 ** (i - 1) for i in range(len(stages)))
            }
            
            return Response(preview_data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
