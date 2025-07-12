// Datos de ejemplo para la Natsu Cup

export const samplePlayers = [
  {
    id: 1,
    display_name: 'Lionel Messi',
    avatar: null,
    stats: {
      total_matches: 45,
      wins: 32,
      losses: 8,
      draws: 5,
      win_rate: 71.1
    }
  },
  {
    id: 2,
    display_name: 'Cristiano Ronaldo',
    avatar: null,
    stats: {
      total_matches: 42,
      wins: 28,
      losses: 10,
      draws: 4,
      win_rate: 66.7
    }
  },
  {
    id: 3,
    display_name: 'Neymar Jr',
    avatar: null,
    stats: {
      total_matches: 38,
      wins: 25,
      losses: 9,
      draws: 4,
      win_rate: 65.8
    }
  },
  {
    id: 4,
    display_name: 'Kevin De Bruyne',
    avatar: null,
    stats: {
      total_matches: 40,
      wins: 30,
      losses: 6,
      draws: 4,
      win_rate: 75.0
    }
  },
  {
    id: 5,
    display_name: 'Erling Haaland',
    avatar: null,
    stats: {
      total_matches: 35,
      wins: 28,
      losses: 5,
      draws: 2,
      win_rate: 80.0
    }
  },
  {
    id: 6,
    display_name: 'Kylian Mbappé',
    avatar: null,
    stats: {
      total_matches: 39,
      wins: 26,
      losses: 8,
      draws: 5,
      win_rate: 66.7
    }
  },
  {
    id: 7,
    display_name: 'Jude Bellingham',
    avatar: null,
    stats: {
      total_matches: 32,
      wins: 22,
      losses: 7,
      draws: 3,
      win_rate: 68.8
    }
  },
  {
    id: 8,
    display_name: 'Vinícius Jr',
    avatar: null,
    stats: {
      total_matches: 36,
      wins: 24,
      losses: 8,
      draws: 4,
      win_rate: 66.7
    }
  }
]

export const sampleTeams = [
  {
    id: 1,
    name: 'Real Madrid',
    logo: null,
    stats: {
      total_matches: 120,
      wins: 85,
      losses: 20,
      draws: 15,
      win_rate: 70.8,
    },
  },
  {
    id: 2,
    name: 'Manchester City',
    logo: null,
    stats: {
      total_matches: 115,
      wins: 82,
      losses: 18,
      draws: 15,
      win_rate: 71.3,
    },
  },
  {
    id: 3,
    name: 'Barcelona',
    logo: null,
    stats: {
      total_matches: 118,
      wins: 78,
      losses: 25,
      draws: 15,
      win_rate: 66.1,
    },
  },
  {
    id: 4,
    name: 'Bayern Munich',
    logo: null,
    stats: {
      total_matches: 110,
      wins: 75,
      losses: 22,
      draws: 13,
      win_rate: 68.2,
    },
  },
  {
    id: 5,
    name: 'PSG',
    logo: null,
    stats: {
      total_matches: 105,
      wins: 70,
      losses: 20,
      draws: 15,
      win_rate: 66.7,
    },
  },
  {
    id: 6,
    name: 'Liverpool',
    logo: null,
    stats: {
      total_matches: 112,
      wins: 72,
      losses: 25,
      draws: 15,
      win_rate: 64.3,
    },
  },
  {
    id: 7,
    name: 'Manchester United',
    logo: null,
    stats: {
      total_matches: 108,
      wins: 65,
      losses: 30,
      draws: 13,
      win_rate: 60.2,
    },
  },
  {
    id: 8,
    name: 'Chelsea',
    logo: null,
    stats: {
      total_matches: 100,
      wins: 60,
      losses: 28,
      draws: 12,
      win_rate: 60,
    },
  },
  {
    id: 9,
    name: 'Arsenal',
    logo: null,
    stats: {
      total_matches: 95,
      wins: 55,
      losses: 30,
      draws: 10,
      win_rate: 57.9,
    },
  },
  {
    id: 10,
    name: 'Juventus',
    logo: null,
    stats: {
      total_matches: 98,
      wins: 58,
      losses: 25,
      draws: 15,
      win_rate: 59.2,
    },
  },
  {
    id: 11,
    name: 'AC Milan',
    logo: null,
    stats: {
      total_matches: 90,
      wins: 50,
      losses: 30,
      draws: 10,
      win_rate: 55.6,
    },
  },
  {
    id: 12,
    name: 'Inter Milan',
    logo: null,
    stats: {
      total_matches: 92,
      wins: 52,
      losses: 28,
      draws: 12,
      win_rate: 56.5,
    },
  },
  {
    id: 13,
    name: 'Atlético Madrid',
    logo: null,
    stats: {
      total_matches: 88,
      wins: 48,
      losses: 25,
      draws: 15,
      win_rate: 54.5,
    },
  },
  {
    id: 14,
    name: 'Borussia Dortmund',
    logo: null,
    stats: {
      total_matches: 85,
      wins: 45,
      losses: 30,
      draws: 10,
      win_rate: 52.9,
    },
  },
  {
    id: 15,
    name: 'Ajax',
    logo: null,
    stats: {
      total_matches: 82,
      wins: 42,
      losses: 30,
      draws: 10,
      win_rate: 51.2,
    },
  },
]

export const sampleTournaments = [
  {
    id: 1,
    name: 'Natsu Cup 2024',
    format: '1v1',
    total_teams: 8,
    teams_per_group: 4,
    has_group_stage: true,
    has_knockout: true,
    status: 'in_progress',
    created_at: '2024-01-15T10:00:00Z',
    team_count: 8,
    matches_count: 12
  },
  {
    id: 2,
    name: 'Champions League Local',
    format: '2v2',
    total_teams: 16,
    teams_per_group: 4,
    has_group_stage: true,
    has_knockout: true,
    status: 'completed',
    created_at: '2024-01-10T14:30:00Z',
    team_count: 16,
    matches_count: 31
  },
  {
    id: 3,
    name: 'Copa Libertadores',
    format: '1v1',
    total_teams: 12,
    teams_per_group: 3,
    has_group_stage: true,
    has_knockout: true,
    status: 'in_progress',
    created_at: '2024-01-20T09:15:00Z',
    team_count: 12,
    matches_count: 18
  }
]
