from django.db import models
from django.db.models import F

class Player(models.Model):
    display_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    # Campos de estadísticas
    total_matches = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    goals_scored = models.PositiveIntegerField(default=0)
    goals_conceded = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.display_name

class GameTeam(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='teams/', null=True, blank=True)
    # Campos de estadísticas
    total_matches = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    goals_scored = models.PositiveIntegerField(default=0)
    goals_conceded = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    format = models.CharField(choices=[('1v1', '1v1'), ('2v2', '2v2')], max_length=4)
    total_teams = models.PositiveIntegerField()
    
    # Nuevo campo para tipo de competición
    competition_type = models.CharField(choices=[
        ('cup', 'Copa (Eliminatoria directa)'),
        ('league', 'Liga (Todos contra todos)'),
        ('hybrid', 'Liga + Playoffs'),
        ('groups', 'Fase de grupos + Eliminatoria'),
    ], default='cup', max_length=20)
    
    # Configuración para liga
    league_rounds = models.PositiveIntegerField(default=1)  # Vueltas
    playoff_teams = models.PositiveIntegerField(default=4)  # Equipos que van a playoffs
    
    # Configuración para grupos
    has_group_stage = models.BooleanField(default=False)
    has_knockout = models.BooleanField(default=True)
    teams_per_group = models.PositiveIntegerField(default=4)
    
    rules = models.TextField(blank=True)
    status = models.CharField(
        choices=[
            ('draft', 'Borrador'),
            ('active', 'En progreso'),
            ('completed', 'Completado'),
            ('cancelled', 'Cancelado')
        ],
        default='draft',
        max_length=20
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TeamEntry(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    players = models.ManyToManyField('Player')
    assigned_team = models.ForeignKey('GameTeam', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Entry {self.pk} [{self.tournament.name}]'

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    participants = models.ManyToManyField(TeamEntry)
    stage = models.CharField(
        choices=[
            ('league', 'League'),
            ('group', 'Group Stage'),
            ('round_of_16', 'Round of 16'),
            ('quarterfinal', 'Quarterfinal'),
            ('semifinal', 'Semifinal'),
            ('final', 'Final'),
        ],
        max_length=20
    )
    round = models.PositiveIntegerField(null=True, blank=True)  # Para ligas
    group_code = models.CharField(max_length=10, null=True, blank=True)
    goals = models.JSONField(default=dict)
    played = models.BooleanField(default=False)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Para encadenar rondas
    player_slot_1 = models.ForeignKey('self', null=True, blank=True, related_name='next_1', on_delete=models.SET_NULL)
    player_slot_2 = models.ForeignKey('self', null=True, blank=True, related_name='next_2', on_delete=models.SET_NULL)

class GroupStanding(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    group_code = models.CharField(max_length=10)
    team_entry = models.ForeignKey(TeamEntry, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    matches_played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

class TournamentStanding(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team_entry = models.ForeignKey(TeamEntry, on_delete=models.CASCADE)
    matches_played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['tournament', 'team_entry']
        ordering = ['-points', '-goals_for', '-goals_against']  # Corregido aquí
    
    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against
