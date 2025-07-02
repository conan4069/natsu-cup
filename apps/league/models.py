from django.db import models

class Player(models.Model):
  display_name = models.CharField(max_length=100)
  avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

  def __str__(self):
      return self.display_name

class GameTeam(models.Model):
  name = models.CharField(max_length=100)
  logo = models.ImageField(upload_to='teams/', null=True, blank=True)

  def __str__(self):
    return self.name

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    format = models.CharField(choices=[('1v1', '1v1'), ('2v2', '2v2')], max_length=4)
    total_teams = models.PositiveIntegerField()
    has_group_stage = models.BooleanField(default=False)
    has_knockout = models.BooleanField(default=True)
    teams_per_group = models.PositiveIntegerField(default=4)
    rules = models.TextField(blank=True)

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
      ('group', 'Group Stage'),
      ('round_of_16', 'Round of 16'),
      ('quarterfinal', 'Quarterfinal'),
      ('semifinal', 'Semifinal'),
      ('final', 'Final'),
    ],
    max_length=20
  )
  group_code = models.CharField(max_length=10, null=True, blank=True)
  goals = models.JSONField(default=dict)  # e.g. {"team_entry_id": goals}
  played = models.BooleanField(default=False)
  scheduled_at = models.DateTimeField(null=True, blank=True)

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

  @property
  def goal_difference(self):
    return self.goals_for - self.goals_against
