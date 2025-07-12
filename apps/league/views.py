from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    Tournament, Player, GameTeam, TeamEntry, Match, GroupStanding
)
from .serializers import (
    TournamentSerializer, PlayerSerializer,
    GameTeamSerializer, TeamEntrySerializer,
    MatchSerializer
)
from .brackets import (
    generate_group_matches,
    generate_knockout_bracket,
    generate_playoffs_for_missing_slots,
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

      entries = TeamEntry.objects.filter(tournament=tournament)
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

      generate_group_matches(tournament, group_map)

      return Response({'message': 'Group matches generated'}, status=201)

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

# 🎮 Detalle de partido
class MatchDetailView(generics.RetrieveAPIView):
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

        # Obtener todos los partidos del torneo
        matches = Match.objects.filter(tournament=tournament)
        
        match_data = []
        for match in matches:
            participants = list(match.participants.all())
            
            # Determinar ganador si el partido está jugado
            winner = None
            if match.played and match.goals:
                team1_id = str(participants[0].id) if participants else None
                team2_id = str(participants[1].id) if len(participants) > 1 else None
                
                if team1_id and team2_id:
                    team1_goals = match.goals.get(team1_id, 0)
                    team2_goals = match.goals.get(team2_id, 0)
                    
                    if team1_goals > team2_goals:
                        winner = 'team1'
                    elif team2_goals > team1_goals:
                        winner = 'team2'
            
            match_data.append({
                'id': match.id,
                'stage': match.stage,
                'played': match.played,
                'winner': winner,
                'team1': {
                    'id': participants[0].id,
                    'name': str(participants[0])
                } if participants else None,
                'team2': {
                    'id': participants[1].id,
                    'name': str(participants[1])
                } if len(participants) > 1 else None,
                'placeholder_team1': f'Winner of M{match.player_slot_1.id}' if match.player_slot_1 else None,
                'placeholder_team2': f'Winner of M{match.player_slot_2.id}' if match.player_slot_2 else None,
                'goals': match.goals or {},
                'team1_score': match.goals.get(str(participants[0].id), 0) if participants and match.goals else 0,
                'team2_score': match.goals.get(str(participants[1].id), 0) if len(participants) > 1 and match.goals else 0
            })

        return Response(match_data, status=200)

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
