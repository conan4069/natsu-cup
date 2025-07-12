from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    Tournament, Player, GameTeam, TeamEntry, Match, GroupStanding, TournamentStanding
)
from .serializers import (
    TournamentSerializer, PlayerSerializer,
    GameTeamSerializer, TeamEntrySerializer,
    MatchSerializer, GroupStandingSerializer, TournamentStandingSerializer
)
from .brackets import (
    generate_group_matches,
    generate_knockout_bracket,
    generate_playoffs_for_missing_slots,
    get_qualified_teams_for_knockout
)
from .utils import (
    update_player_stats, update_team_stats, update_tournament_status,
    generate_league_matches, update_tournament_standings
)

import random

# 🏆 Torneos
class TournamentListCreateView(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class TournamentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class TeamEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = TeamEntrySerializer

    def get_queryset(self):
        tournament_id = self.kwargs.get('tournament_id')
        return TeamEntry.objects.filter(tournament_id=tournament_id)

    def perform_create(self, serializer):
        tournament_id = self.kwargs.get('tournament_id')
        serializer.save(tournament_id=tournament_id)

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
                            'avatar': player.avatar.url if player.avatar else None
                        }
                        for player in entry.players.all()
                    ],
                    'assigned_team': {
                        'id': entry.assigned_team.id,
                        'name': entry.assigned_team.name,
                        'logo': entry.assigned_team.logo.url if entry.assigned_team.logo else None
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

class PlayerCreateView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerStatsView(views.APIView):
    def get(self, request, player_id):
        try:
            player = Player.objects.get(pk=player_id)
        except Player.DoesNotExist:
            return Response({'error': 'Player not found'}, status=404)
        
        # Obtener todas las entradas del jugador
        team_entries = TeamEntry.objects.filter(players=player)
        
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
            'total_points': wins * 3 + draws,  # Sistema de puntos: 3 por victoria, 1 por empate
        }
        
        return Response(stats)

class PlayerTournamentsView(views.APIView):
    def get(self, request, player_id):
        try:
            player = Player.objects.get(pk=player_id)
        except Player.DoesNotExist:
            return Response({'error': 'Player not found'}, status=404)
        
        # Obtener todas las entradas del jugador con información del torneo
        team_entries = TeamEntry.objects.filter(players=player).select_related('tournament', 'assigned_team')
        
        tournaments = []
        for entry in team_entries:
            tournament = entry.tournament
            
            # Obtener estadísticas del jugador en este torneo
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

class GameTeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameTeam.objects.all()
    serializer_class = GameTeamSerializer

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

# Detalle y actualización de partido
class MatchDetailView(generics.RetrieveUpdateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class TeamEntryDeleteView(generics.DestroyAPIView):
  queryset = TeamEntry.objects.all()
  serializer_class = TeamEntrySerializer

class AssignRandomTeamsView(APIView):
  def post(self, request, tournament_id):
    try:
      tournament = Tournament.objects.get(pk=tournament_id)
    except Tournament.DoesNotExist:
      return Response({'error': 'Tournament not found'}, status=404)

    entries = TeamEntry.objects.filter(tournament=tournament, assigned_team__isnull=True)
    available_teams = list(GameTeam.objects.all())

    if len(available_teams) < entries.count():
      return Response({'error': 'Not enough available teams'}, status=400)

    random.shuffle(available_teams)
    for entry, team in zip(entries, available_teams):
      entry.assigned_team = team
      entry.save()

    return Response({'message': f'{entries.count()} teams assigned randomly'}, status=200)

class CompleteKnockoutStageView(APIView):
  def post(self, request, tournament_id):
    desired_total = request.data.get('total_slots')  # ej: 8
    next_stage = request.data.get('next_stage')      # ej: 'quarterfinal'

    if not desired_total or not next_stage:
      return Response({'error': 'Both total_slots and next_stage are required'}, status=400)

    try:
      tournament = Tournament.objects.get(pk=tournament_id)
    except Tournament.DoesNotExist:
      return Response({'error': 'Tournament not found'}, status=404)

    current_entries = TeamEntry.objects.filter(tournament=tournament)
    entry_count = current_entries.count()

    playoff_matches = []
    try:
      if entry_count < desired_total:
        playoff_matches = generate_playoffs_for_missing_slots(
          tournament=tournament,
          desired_total=desired_total,
          stage_name=next_stage
        )
    except ValueError as e:
      return Response({'error': str(e)}, status=400)

    # Combinar actuales + ganadores futuros
    total_expected = entry_count + len(playoff_matches)
    if total_expected != desired_total:
      return Response({
        'error': f'Incomplete bracket: total {total_expected}, expected {desired_total}'
      }, status=400)

    # Generar la fase principal (con slots vacíos si es necesario)
    knockout = generate_knockout_bracket(
      tournament,
      list(current_entries),
      stage=next_stage
    )

    return Response({
      'message': f'Bracket for {next_stage} completed',
      'playoffs_created': [m.id for m in playoff_matches],
      'matches_created': [m.id for m in knockout] if knockout else []
    }, status=201)

class TournamentMatchesView(APIView):
    def get(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)

        # Obtener todos los partidos del torneo con información completa
        matches = Match.objects.filter(tournament=tournament).prefetch_related(
            'participants', 
            'participants__players', 
            'participants__assigned_team'
        )
        
        match_data = []
        for match in matches:
            participants_data = []
            
            for participant in match.participants.all():
                participant_info = {
                    'id': participant.id,
                    'players': [
                        {
                            'id': player.id,
                            'display_name': player.display_name,
                            'avatar': player.avatar.url if player.avatar else None
                        }
                        for player in participant.players.all()
                    ],
                    'assigned_team': {
                        'id': participant.assigned_team.id,
                        'name': participant.assigned_team.name,
                        'logo': participant.assigned_team.logo.url if participant.assigned_team.logo else None
                    } if participant.assigned_team else None,
                    'team_name': str(participant)
                }
                participants_data.append(participant_info)
            
            match_info = {
                'id': match.id,
                'stage': match.stage,
                'group_code': match.group_code,
                'played': match.played,
                'goals': match.goals,
                'participants': participants_data,
                'created_at': match.created_at,
                'updated_at': match.updated_at
            }
            match_data.append(match_info)

        return Response({
            'tournament_id': tournament.id,
            'tournament_name': tournament.name,
            'matches': match_data
        })

class KnockoutPreviewView(APIView):
    def get(self, request, tournament_id):
      try:
        tournament = Tournament.objects.get(pk=tournament_id)
      except Tournament.DoesNotExist:
        return Response({'error': 'Tournament not found'}, status=404)

      # Simulación: se esperan 8 equipos para cuartos
      expected_slots = 8
      current_entries = TeamEntry.objects.filter(tournament=tournament)
      current_count = current_entries.count()
      missing = max(0, expected_slots - current_count)

      # Clasificación paso a paso
      standings = GroupStanding.objects.filter(tournament=tournament)
      steps = []
      group_map = {}

      for s in standings:
        group_map.setdefault(s.group_code, []).append(s)

      for group_code, group_standings in group_map.items():
        ordered = sorted(group_standings, key=lambda x: (x.points, x.goal_difference), reverse=True)
        if len(ordered) >= 2:
            steps.append({
                'type': 'group_winner',
                'team_entry_id': ordered[0].team_entry.id,
                'team_name': str(ordered[0].team_entry),
                'group': group_code
            })
            steps.append({
                'type': 'group_runner_up',
                'team_entry_id': ordered[1].team_entry.id,
                'team_name': str(ordered[1].team_entry),
                'group': group_code
            })
        if len(ordered) >= 3:
            steps.append({
                'type': 'best_third',
                'team_entry_id': ordered[2].team_entry.id,
                'team_name': str(ordered[2].team_entry),
                'group': group_code,
                'status': 'pending' if missing else 'qualified'
            })

      # Simular partidos generados (puedes reemplazar con Match.objects.filter(...))
      matches = Match.objects.filter(tournament=tournament, stage__in=['quarterfinal', 'semifinal', 'final'])

      match_data = []
      for m in matches:
        p = list(m.participants.all())
        match_data.append({
            'id': m.id,
            'stage': m.stage,
            'team1': {'name': str(p[0])} if len(p) > 0 else None,
            'team2': {'name': str(p[1])} if len(p) > 1 else None,
            'placeholder_team1': f'Winner of M{m.player_slot_1.id}' if m.player_slot_1 else None,
            'placeholder_team2': f'Winner of M{m.player_slot_2.id}' if m.player_slot_2 else None
        })

      return Response({
        'stage': 'quarterfinal',
        'expected_slots': expected_slots,
        'current_entries': current_count,
        'missing_slots': missing,
        'qualification_steps': steps,
        'main_bracket': {
          'matches': match_data
        }
      }, status=200)

# Actualizar la vista de guardar resultado de partido
class SaveMatchResultView(APIView):
    def post(self, request, match_id):
        try:
            match = Match.objects.get(pk=match_id)
        except Match.DoesNotExist:
            return Response({'error': 'Match not found'}, status=404)

        goals = request.data.get('goals', {})
        
        # Validar que los goals correspondan a los participantes
        participants = list(match.participants.all())
        for participant_id in goals.keys():
            if not any(str(p.id) == participant_id for p in participants):
                return Response({'error': f'Invalid participant ID: {participant_id}'}, status=400)

        # Actualizar partido
        match.goals = goals
        match.played = True
        match.save()

        # Actualizar estadísticas de jugadores y equipos
        for participant in participants:
            # Actualizar estadísticas de jugadores
            for player in participant.players.all():
                update_player_stats(player.id)
            
            # Actualizar estadísticas del equipo si tiene uno asignado
            if participant.assigned_team:
                update_team_stats(participant.assigned_team.id)
        
        # Actualizar estado del torneo
        update_tournament_status(match.tournament.id)
        
        # Si es un partido de liga, actualizar clasificación
        if match.stage == 'league':
            update_tournament_standings(match.tournament.id)

        return Response({'message': 'Match result saved successfully'}, status=200)

class GenerateLeagueMatchesView(APIView):
    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        if tournament.competition_type not in ['league', 'hybrid']:
            return Response({'error': 'Tournament is not a league type'}, status=400)
        
        # Generar partidos de liga
        matches = generate_league_matches(tournament)
        
        return Response({
            'message': f'{len(matches)} league matches generated',
            'matches_created': [m.id for m in matches]
        }, status=201)

class GeneratePlayoffsView(APIView):
    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        # Obtener los mejores equipos según la clasificación
        standings = TournamentStanding.objects.filter(tournament=tournament)
        top_teams = [s.team_entry for s in standings[:tournament.playoff_teams]]
        
        if len(top_teams) < 2:
            return Response({'error': 'Not enough teams for playoffs'}, status=400)
        
        # Generar partidos de playoffs (usar la función existente de knockout)
        from .brackets import generate_knockout_bracket
        matches = generate_knockout_bracket(tournament, top_teams, 'quarterfinal')
        
        return Response({
            'message': f'Playoffs generated with {len(top_teams)} teams',
            'matches_created': [m.id for m in matches]
        }, status=201)

class TournamentStandingsView(APIView):
    def get(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        standings = TournamentStanding.objects.filter(tournament=tournament)
        serializer = TournamentStandingSerializer(standings, many=True)
        
        return Response(serializer.data, status=200)

class UpdateTournamentStandingsView(APIView):
    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        update_tournament_standings(tournament_id)
        
        return Response({'message': 'Standings updated successfully'}, status=200)

# Nueva vista para clasificaciones de grupos
class GroupStandingsView(APIView):
    def get(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        # Obtener todas las clasificaciones de grupos
        standings = GroupStanding.objects.filter(tournament=tournament)
        
        # Agrupar por código de grupo
        group_standings = {}
        for standing in standings:
            group_code = standing.group_code
            if group_code not in group_standings:
                group_standings[group_code] = []
            group_standings[group_code].append(standing)
        
        # Ordenar cada grupo por puntos, diferencia de goles, etc.
        for group_code in group_standings:
            group_standings[group_code].sort(
                key=lambda x: (x.points, x.goal_difference, x.goals_for),
                reverse=True
            )
        
        # Serializar los datos
        result = {}
        for group_code, standings_list in group_standings.items():
            serializer = GroupStandingSerializer(standings_list, many=True)
            result[group_code] = serializer.data
        
        return Response(result, status=200)

# Nueva vista para generar fase eliminatoria
class GenerateKnockoutStageView(APIView):
    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        if not tournament.has_knockout:
            return Response({'error': 'Knockout stage is disabled in this tournament'}, status=400)
        
        # Verificar que todos los partidos de grupos estén completados
        group_matches = Match.objects.filter(tournament=tournament, stage='group')
        if not group_matches.exists():
            return Response({'error': 'No group matches found'}, status=400)
        
        unplayed_matches = group_matches.filter(played=False)
        if unplayed_matches.exists():
            return Response({
                'error': 'Not all group matches are completed',
                'unplayed_matches': unplayed_matches.count()
            }, status=400)
        
        # Obtener los equipos clasificados
        from .brackets import get_best_third_place_teams
        
        # Obtener primeros y segundos de cada grupo
        qualified_teams = []
        standings = GroupStanding.objects.filter(tournament=tournament)
        
        # Agrupar por grupo
        group_map = {}
        for standing in standings:
            group_map.setdefault(standing.group_code, []).append(standing)
        
        # Tomar los 2 mejores de cada grupo
        for group_code, group_standings in group_map.items():
            sorted_standings = sorted(
                group_standings,
                key=lambda x: (x.points, x.goal_difference, x.goals_for),
                reverse=True
            )
            
            # Agregar primero y segundo
            if len(sorted_standings) >= 1:
                qualified_teams.append(sorted_standings[0].team_entry)
            if len(sorted_standings) >= 2:
                qualified_teams.append(sorted_standings[1].team_entry)
        
        # Si necesitamos más equipos, tomar los mejores terceros
        expected_teams = 8  # Para cuartos de final
        if len(qualified_teams) < expected_teams:
            needed_third_place = expected_teams - len(qualified_teams)
            third_place_teams = get_best_third_place_teams(tournament, needed_third_place)
            qualified_teams.extend(third_place_teams)
        
        if len(qualified_teams) < 2:
            return Response({'error': 'Not enough qualified teams for knockout stage'}, status=400)
        
        # Generar el bracket eliminatorio
        from .brackets import generate_knockout_bracket
        matches = generate_knockout_bracket(tournament, qualified_teams, 'quarterfinal')
        
        return Response({
            'message': f'Knockout stage generated with {len(qualified_teams)} teams',
            'qualified_teams': len(qualified_teams),
            'matches_created': len(matches)
        }, status=201)

# Nueva vista para obtener equipos clasificados
class QualifiedTeamsView(APIView):
    def get(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=404)
        
        # Verificar que el torneo tenga fase de grupos
        if not tournament.has_group_stage:
            return Response({'error': 'Tournament does not have group stage'}, status=400)
        
        # Obtener equipos clasificados
        qualified_teams = get_qualified_teams_for_knockout(tournament)
        
        # Serializar los datos
        from .serializers import TeamEntrySerializer
        
        def serialize_qualified_team(team_data):
            team_entry_data = TeamEntrySerializer(team_data['team_entry']).data
            return {
                'team_entry': team_entry_data,
                'group_code': team_data['group_code'],
                'position': team_data['position'],
                'points': team_data['points'],
                'goal_difference': team_data['goal_difference'],
                'goals_for': team_data['goals_for'],
                'qualification_type': get_qualification_type(team_data['position'])
            }
        
        def get_qualification_type(position):
            if position == 1:
                return 'group_winner'
            elif position == 2:
                return 'group_runner_up'
            else:
                return 'best_third_place'
        
        # Serializar cada categoría
        result = {
            'group_winners': [serialize_qualified_team(team) for team in qualified_teams['group_winners']],
            'group_runners_up': [serialize_qualified_team(team) for team in qualified_teams['group_runners_up']],
            'best_third_place': [serialize_qualified_team(team) for team in qualified_teams['best_third_place']],
            'total_qualified': qualified_teams['total_qualified'],
            'tournament_info': {
                'id': tournament.id,
                'name': tournament.name,
                'format': tournament.format,
                'has_knockout': tournament.has_knockout
            }
        }
        
        return Response(result, status=200)
