#!/usr/bin/env python3
"""
Script para generar datos de ejemplo para la Natsu Cup
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/Users/conan4069/Documents/natsu-cup')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.league.models import Player, GameTeam
import random

def create_sample_players():
    """Crear 8 jugadores de ejemplo"""
    
    players_data = [
        {
            'display_name': 'Lionel Messi',
            'avatar': None
        },
        {
            'display_name': 'Cristiano Ronaldo',
            'avatar': None
        },
        {
            'display_name': 'Neymar Jr',
            'avatar': None
        },
        {
            'display_name': 'Kevin De Bruyne',
            'avatar': None
        },
        {
            'display_name': 'Erling Haaland',
            'avatar': None
        },
        {
            'display_name': 'Kylian Mbappé',
            'avatar': None
        },
        {
            'display_name': 'Jude Bellingham',
            'avatar': None
        },
        {
            'display_name': 'Vinícius Jr',
            'avatar': None
        }
    ]
    
    created_players = []
    for player_data in players_data:
        player, created = Player.objects.get_or_create(
            display_name=player_data['display_name'],
            defaults=player_data
        )
        if created:
            print(f"✅ Jugador creado: {player.display_name}")
        else:
            print(f"⚠️  Jugador ya existe: {player.display_name}")
        created_players.append(player)
    
    return created_players

def create_sample_teams():
    """Crear 15 equipos famosos"""
    
    teams_data = [
        {
            'name': 'Real Madrid',
            'logo': None
        },
        {
            'name': 'Manchester City',
            'logo': None
        },
        {
            'name': 'Barcelona',
            'logo': None
        },
        {
            'name': 'Bayern Munich',
            'logo': None
        },
        {
            'name': 'PSG',
            'logo': None
        },
        {
            'name': 'Liverpool',
            'logo': None
        },
        {
            'name': 'Manchester United',
            'logo': None
        },
        {
            'name': 'Chelsea',
            'logo': None
        },
        {
            'name': 'Arsenal',
            'logo': None
        },
        {
            'name': 'Juventus',
            'logo': None
        },
        {
            'name': 'AC Milan',
            'logo': None
        },
        {
            'name': 'Inter Milan',
            'logo': None
        },
        {
            'name': 'Atlético Madrid',
            'logo': None
        },
        {
            'name': 'Borussia Dortmund',
            'logo': None
        },
        {
            'name': 'Ajax',
            'logo': None
        }
    ]
    
    created_teams = []
    for team_data in teams_data:
        team, created = GameTeam.objects.get_or_create(
            name=team_data['name'],
            defaults=team_data
        )
        if created:
            print(f"✅ Equipo creado: {team.name}")
        else:
            print(f"⚠️  Equipo ya existe: {team.name}")
        created_teams.append(team)
    
    return created_teams

def main():
    """Función principal"""
    print("🏆 Generando datos de ejemplo para Natsu Cup...")
    print("=" * 50)
    
    # Crear jugadores
    print("\n👥 Creando jugadores...")
    players = create_sample_players()
    
    # Crear equipos
    print("\n🛡️  Creando equipos...")
    teams = create_sample_teams()
    
    print("\n" + "=" * 50)
    print(f"✅ Datos generados exitosamente:")
    print(f"   - {len(players)} jugadores creados")
    print(f"   - {len(teams)} equipos creados")
    print("\n🎉 ¡Los datos de ejemplo están listos para usar!")

if __name__ == '__main__':
    main() 