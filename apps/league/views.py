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

# 🛡️ Equipos del juego
class GameTeamListView(generics.ListAPIView):
    queryset = GameTeam.objects.all()
    serializer_class = GameTeamSerializer

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
      'matches_created': [m.id for m in knockout]
    }, status=201)

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
