from rest_framework import serializers
from .models import GameTeam, Player, Tournament, TeamEntry, Match, GroupStanding

class PlayerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Player
    fields = ['id', 'display_name', 'avatar']

class GameTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameTeam
        fields = '__all__'

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'

class TeamEntrySerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    assigned_team = GameTeamSerializer(read_only=True)

    class Meta:
        model = TeamEntry
        fields = '__all__'

    def validate_players(self, players):
      tournament = self.initial_data.get('tournament') or self.context['view'].kwargs.get('tournament_id')
      for player in players:
        if TeamEntry.objects.filter(tournament_id=tournament, players=player).exists():
          raise serializers.ValidationError(f'Player {player} is already registered in this tournament')
      return players


class MatchSerializer(serializers.ModelSerializer):
    participants = TeamEntrySerializer(many=True, read_only=True)
    player_slot_1_id = serializers.IntegerField(read_only=True)
    player_slot_2_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Match
        fields = '__all__'

class GroupStandingSerializer(serializers.ModelSerializer):
    team_entry = TeamEntrySerializer(read_only=True)

    class Meta:
        model = GroupStanding
        fields = '__all__'
