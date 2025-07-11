from django.urls import path
from . import views
from .views import (
    GenerateLeagueMatchesView, GeneratePlayoffsView, TournamentStandingsView, 
    UpdateTournamentStandingsView, SaveMatchResultView, GroupStandingsView,
    GenerateKnockoutStageView, QualifiedTeamsView
)

urlpatterns = [
    path('tournaments/', views.TournamentListCreateView.as_view()),
    path('tournaments/<int:pk>/', views.TournamentDetailView.as_view()),
    path('tournaments/<int:tournament_id>/generate-groups/', views.GenerateGroupMatchesView.as_view()),
    path(
      'tournaments/<int:tournament_id>/entries/',
      views.TeamEntryListCreateView.as_view(),
      name='tournament-entries'
    ),
    path(
      'entries/<int:pk>/delete/',
      views.TeamEntryDeleteView.as_view(),
      name='delete-entry'
    ),
    path(
      'tournaments/<int:tournament_id>/assign-teams/',
      views.AssignRandomTeamsView.as_view(),
      name='assign-random-teams'
    ),
    path(
        'tournaments/<int:tournament_id>/knockout-preview/',
        views.KnockoutPreviewView.as_view(),
        name='knockout-preview'
    ),
    path(
      'tournaments/<int:tournament_id>/complete-knockout-stage/',
      views.CompleteKnockoutStageView.as_view(),
      name='complete-knockout'
    ),
    path('matches/<int:pk>/', views.MatchDetailView.as_view()),
    path('tournaments/<int:tournament_id>/matches/', views.TournamentMatchesView.as_view()),
    path('players/', views.PlayerListView.as_view()),
    path('players/create/', views.PlayerCreateView.as_view()),
    path('players/<int:pk>/', views.PlayerDetailView.as_view()),
    path('players/<int:player_id>/stats/', views.PlayerStatsView.as_view()),
    path('players/<int:player_id>/tournaments/', views.PlayerTournamentsView.as_view()),
    path('teams/', views.GameTeamListCreateView.as_view()),
    path('teams/<int:pk>/', views.GameTeamDetailView.as_view()),
    path('teams/<int:team_id>/stats/', views.GameTeamStatsView.as_view()),
    path('teams/<int:team_id>/tournaments/', views.GameTeamTournamentsView.as_view()),
    path('tournaments/<int:tournament_id>/generate-league-matches/', GenerateLeagueMatchesView.as_view(), name='generate-league-matches'),
    path('tournaments/<int:tournament_id>/generate-playoffs/', GeneratePlayoffsView.as_view(), name='generate-playoffs'),
    path('tournaments/<int:tournament_id>/standings/', TournamentStandingsView.as_view(), name='tournament-standings'),
    path('tournaments/<int:tournament_id>/update-standings/', UpdateTournamentStandingsView.as_view(), name='update-standings'),
    path('matches/<int:match_id>/save-result/', SaveMatchResultView.as_view(), name='save-match-result'),
    # Nuevos endpoints para grupos
    path('tournaments/<int:tournament_id>/group-standings/', GroupStandingsView.as_view(), name='group-standings'),
    path('tournaments/<int:tournament_id>/generate-knockout/', GenerateKnockoutStageView.as_view(), name='generate-knockout'),
    path('tournaments/<int:tournament_id>/qualified-teams/', QualifiedTeamsView.as_view(), name='qualified-teams'),
]
