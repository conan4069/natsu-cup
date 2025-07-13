from django.urls import path
from . import views

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
      'tournaments/<int:tournament_id>/knockout-stage/',
      views.KnockoutStageView.as_view(),
      name='knockout-stage'
    ),
    path('matches/<int:match_id>/', views.MatchView.as_view()),
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
    
    # Endpoints unificados
    path('tournaments/<int:tournament_id>/standings/', views.StandingsView.as_view(), name='standings'),
    path('tournaments/<int:tournament_id>/qualified-teams/', views.QualifiedTeamsView.as_view(), name='qualified-teams'),
    
    # URLs para liga y playoffs
    path('tournaments/<int:tournament_id>/generate-league-matches/', views.GenerateLeagueMatchesView.as_view(), name='generate-league-matches'),
    path('tournaments/<int:tournament_id>/generate-playoffs/', views.GeneratePlayoffsView.as_view(), name='generate-playoffs'),
]
