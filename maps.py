import pandas as pd
# Combine striker, non-striker → batting_team


batting_team_map = pd.concat([
    df[['striker', 'batting_team']].rename(columns={'striker': 'player', 'batting_team': 'team'}),
    df[['non_striker', 'batting_team']].rename(columns={'non_striker': 'player', 'batting_team': 'team'})
])

# Bowler → bowling_team
bowling_team_map = df[['bowler', 'bowling_team']].rename(columns={'bowler': 'player', 'bowling_team': 'team'})

# Merge all player-team mappings
player_team_map = pd.concat([batting_team_map, bowling_team_map])
player_team_map = player_team_map.drop_duplicates().dropna()
