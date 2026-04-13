import streamlit as st
import pandas as pd

def show(df):
    st.header("Best World Cup XI Selector")

    # Normalize names
    df["striker"] = df["striker"].astype(str).str.strip().str.lower()
    df["bowler"] = df["bowler"].astype(str).str.strip().str.lower()

    # ---------- Batting Stats ----------
    batting_stats = df.groupby("striker").agg(
        runs=("runs_off_bat", "sum"),
        balls=("ball", "count"),
        team=("batting_team", lambda x: x.mode()[0] if not x.mode().empty else "Unknown")
    ).reset_index()

    batting_stats["strike_rate"] = (batting_stats["runs"] / batting_stats["balls"]) * 100
    batting_stats["batting_score"] = batting_stats["runs"] * batting_stats["strike_rate"]

    # ---------- Bowling Stats ----------
    valid_wickets = df[df["wicket_type"].notnull()]
    bowling_stats = valid_wickets.groupby("bowler").agg(
        wickets=("player_dismissed", "count"),
        runs_conceded=("total_runs", "sum"),
        balls=("ball", "count"),
        team=("bowling_team", lambda x: x.mode()[0] if not x.mode().empty else "Unknown")
    ).reset_index()

    bowling_stats["economy"] = bowling_stats["runs_conceded"] / (bowling_stats["balls"] / 6)
    bowling_stats["bowling_score"] = bowling_stats["wickets"] / bowling_stats["economy"]

    # ---------- All-Rounders ----------
    all_rounders = pd.merge(
        batting_stats, bowling_stats,
        left_on="striker", right_on="bowler"
    )
    all_rounders = all_rounders[
        (all_rounders["runs"] > 50) & (all_rounders["wickets"] >= 2)
    ]
    all_rounders["all_round_score"] = all_rounders["batting_score"] + all_rounders["bowling_score"]

    # ---------- Selector Helper ----------
    def select_players(df, n, team_col="team"):
        selected = []
        team_count = {}
        for _, row in df.iterrows():
            team = row[team_col]
            if team_count.get(team, 0) < 4:
                selected.append(row)
                team_count[team] = team_count.get(team, 0) + 1
            if len(selected) == n:
                break
        return pd.DataFrame(selected)

    # ---------- Select Roles ----------
    openers = batting_stats.sort_values("batting_score", ascending=False)
    selected_openers = select_players(openers, 2)

    middle = openers[~openers["striker"].isin(selected_openers["striker"])].sort_values("batting_score", ascending=False)
    selected_middle = select_players(middle, 3)

    all_rounders_sorted = all_rounders.sort_values("all_round_score", ascending=False)
    selected_ar = select_players(all_rounders_sorted, 2, team_col="team_x")

    bowlers_sorted = bowling_stats.sort_values("bowling_score", ascending=False)
    selected_bowlers = select_players(bowlers_sorted, 4)

    # ---------- Combine Final XI ----------
    final_xi = pd.concat([
        selected_openers[["striker", "team", "runs", "strike_rate"]],
        selected_middle[["striker", "team", "runs", "strike_rate"]],
        selected_ar[["striker", "team_x", "runs", "strike_rate"]].rename(columns={"team_x": "team"}),
        selected_bowlers[["bowler", "team", "wickets", "economy"]].rename(columns={"bowler": "striker"})
    ])

    final_xi.reset_index(drop=True, inplace=True)
    final_xi.insert(0, "Position", [
        "Opener 1", "Opener 2",
        "Middle 1", "Middle 2", "Middle 3",
        "All-rounder 1", "All-rounder 2",
        "Bowler 1", "Bowler 2", "Bowler 3", "Bowler 4"
    ])

    st.subheader(" Auto-Selected Best World Cup XI")
    st.dataframe(final_xi)

    # Show team distribution
    team_counts = final_xi["team"].value_counts()
    st.markdown("### Team Composition")
    for team, count in team_counts.items():
        st.write(f"{team}: {count} players")

    if any(team_counts > 4):
        st.warning("More than 4 players from a single team found. Consider revising selection logic.")
