import streamlit as st
import pandas as pd

def show(df):
    st.header("MVP per Team – T20 World Cup 2024")

    # Step 1: Build player-to-team mapping
    bat_teams = df[['striker', 'batting_team']].rename(columns={'striker': 'player', 'batting_team': 'team'})
    non_bat_teams = df[['non_striker', 'batting_team']].rename(columns={'non_striker': 'player', 'batting_team': 'team'})
    bowl_teams = df[['bowler', 'bowling_team']].rename(columns={'bowler': 'player', 'bowling_team': 'team'})

    team_map = pd.concat([bat_teams, non_bat_teams, bowl_teams], axis=0)
    team_map = team_map.drop_duplicates().dropna()

    # Step 2: Batting Stats
    bat = df.groupby("striker").agg(
        runs=("runs_off_bat", "sum"),
        balls=("ball", "count"),
        innings=("match_id", pd.Series.nunique)
    ).reset_index()
    bat["strike_rate"] = (bat["runs"] / bat["balls"]) * 100
    bat["avg_runs"] = bat["runs"] / bat["innings"]
    bat["batting_index"] = bat["runs"] * bat["strike_rate"] * bat["avg_runs"]
    bat = bat.rename(columns={"striker": "player"})

    # Step 3: Bowling Stats
    valid_wkts = df[df["wicket_type"].isin([
        "caught", "bowled", "lbw", "stumped", "hit wicket", "caught and bowled"
    ])]

    bowl = df.groupby("bowler").agg(
        runs_conceded=("total_runs", "sum"),
        balls_bowled=("ball", "count")
    ).reset_index()
    bowl["overs"] = bowl["balls_bowled"] // 6 + (bowl["balls_bowled"] % 6) / 6
    bowl["economy"] = bowl["runs_conceded"] / bowl["overs"]

    wickets = valid_wkts.groupby("bowler")["player_dismissed"].count().reset_index()
    wickets = wickets.rename(columns={"player_dismissed": "wickets"})

    bowl = pd.merge(bowl, wickets, on="bowler", how="left").fillna(0)
    bowl["bowling_index"] = bowl["wickets"] * (6 / bowl["economy"]) * bowl["wickets"]
    bowl = bowl.rename(columns={"bowler": "player"})

    # Step 4: Merge Bat + Bowl + Team
    perf = pd.merge(bat[["player", "batting_index"]], bowl[["player", "bowling_index"]], on="player", how="outer").fillna(0)
    perf["performance_index"] = perf["batting_index"] + perf["bowling_index"]
    perf["estimated_value"] = 100  # normalized
    perf["mvp_score"] = perf["performance_index"] / perf["estimated_value"]

    # Add team info
    perf = pd.merge(perf, team_map, on="player", how="left")

    # Step 5: MVPs per team
    st.subheader("Top MVPs per Country (based on performance)")
    teams = perf["team"].dropna().unique()

    for team in sorted(teams):
        team_data = perf[perf["team"] == team].sort_values("mvp_score", ascending=False).head(3)
        if not team_data.empty:
            st.markdown(f"####  {team}")
            st.dataframe(team_data[["player", "mvp_score", "batting_index", "bowling_index"]].set_index("player"))
