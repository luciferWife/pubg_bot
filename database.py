teams = []

def register_team(team_name, captain, player1, player2, player3, player4, reserve):
    team = {
        "team_name": team_name,
        "captain": captain,
        "players": [player1, player2, player3, player4],
        "reserve": reserve
    }
    teams.append(team)
    return team
