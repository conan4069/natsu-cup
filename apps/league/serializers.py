from rest_framework import serializers
from .models import GameTeam, Player, Tournament, TeamEntry, Match, GroupStanding, TournamentStanding

class PlayerSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = ['id', 'display_name', 'avatar', 'stats']
    
    def get_stats(self, obj):
        return {
            'total_matches': obj.total_matches,
            'wins': obj.wins,
            'losses': obj.losses,
            'draws': obj.draws,
            'win_rate': round((obj.wins / obj.total_matches * 100) if obj.total_matches > 0 else 0, 1),
            'goals_scored': obj.goals_scored,
            'goals_conceded': obj.goals_conceded,
        }

class GameTeamSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()
    
    class Meta:
        model = GameTeam
        fields = '__all__'
    
    def get_stats(self, obj):
        return {
            'total_matches': obj.total_matches,
            'wins': obj.wins,
            'losses': obj.losses,
            'draws': obj.draws,
            'win_rate': round((obj.wins / obj.total_matches * 100) if obj.total_matches > 0 else 0, 1),
            'goals_scored': obj.goals_scored,
            'goals_conceded': obj.goals_conceded,
        }

class TournamentSerializer(serializers.ModelSerializer):
    team_count = serializers.SerializerMethodField()
    matches_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tournament
        fields = '__all__'
    
    def get_team_count(self, obj):
        return obj.total_teams
    
    def get_matches_count(self, obj):
        return Match.objects.filter(tournament=obj).count()

class TeamEntrySerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    assigned_team = GameTeamSerializer(read_only=True)

    class Meta:
        model = TeamEntry
        fields = ['id', 'players', 'assigned_team', 'tournament']
        read_only_fields = ['tournament']

    def create(self, validated_data):
        # Obtener datos del request
        players_data = self.initial_data.get('players', [])
        assigned_team_id = self.initial_data.get('assigned_team')
        
        # Crear la entrada
        team_entry = TeamEntry.objects.create(**validated_data)
        
        # Asignar players
        if players_data:
            players = Player.objects.filter(id__in=players_data)
            team_entry.players.set(players)
        
        # Asignar equipo si se proporciona
        if assigned_team_id:
            try:
                assigned_team = GameTeam.objects.get(id=assigned_team_id)
                team_entry.assigned_team = assigned_team
                team_entry.save()
            except GameTeam.DoesNotExist:
                pass
        
        return team_entry

    def validate_players(self, players):
        tournament = self.initial_data.get('tournament') or self.context['view'].kwargs.get('tournament_id')
        for player in players:
            if TeamEntry.objects.filter(tournament_id=tournament, players=player).exists():
                raise serializers.ValidationError(f'Player {player} is already registered in this tournament')
        return players

class MatchSerializer(serializers.ModelSerializer):
    participants = TeamEntrySerializer(many=True, read_only=True)
    team1 = serializers.SerializerMethodField()
    team2 = serializers.SerializerMethodField()
    team1_score = serializers.SerializerMethodField()
    team2_score = serializers.SerializerMethodField()
    winner = serializers.SerializerMethodField()
    player_slot_1_id = serializers.IntegerField(read_only=True)
    player_slot_2_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Match
        fields = '__all__'
    
    def get_team1(self, obj):
        participants = list(obj.participants.all())
        if participants:
            return {
                'id': participants[0].id,
                'name': str(participants[0])
            }
        return None
    
    def get_team2(self, obj):
        participants = list(obj.participants.all())
        if len(participants) > 1:
            return {
                'id': participants[1].id,
                'name': str(participants[1])
            }
        return None
    
    def get_team1_score(self, obj):
        participants = list(obj.participants.all())
        if participants and obj.goals:
            return obj.goals.get(str(participants[0].id), 0)
        return 0
    
    def get_team2_score(self, obj):
        participants = list(obj.participants.all())
        if len(participants) > 1 and obj.goals:
            return obj.goals.get(str(participants[1].id), 0)
        return 0
    
    def get_winner(self, obj):
        if not obj.played or not obj.goals:
            return None
        
        participants = list(obj.participants.all())
        if len(participants) < 2:
            return None
        
        team1_id = str(participants[0].id)
        team2_id = str(participants[1].id)
        team1_goals = obj.goals.get(team1_id, 0)
        team2_goals = obj.goals.get(team2_id, 0)
        
        if team1_goals > team2_goals:
            return 'team1'
        elif team2_goals > team1_goals:
            return 'team2'
        return 'draw'

class GroupStandingSerializer(serializers.ModelSerializer):
    team_entry = TeamEntrySerializer(read_only=True)

    class Meta:
        model = GroupStanding
        fields = '__all__'

class TournamentStandingSerializer(serializers.ModelSerializer):
    team_entry = TeamEntrySerializer(read_only=True)
    goal_difference = serializers.SerializerMethodField()
    
    class Meta:
        model = TournamentStanding
        fields = '__all__'
    
    def get_goal_difference(self, obj):
        return obj.goal_difference
