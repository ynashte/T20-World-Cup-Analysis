import streamlit as st
import pandas as pd

def show(df):
    st.header("Player Impact Analysis")

    # Batting Impact = Runs * Strike Rate Context
    bat = df.groupby(["match_id", "striker"]).agg(
        runs=("runs_off_bat", "sum"),
        balls=("ball", "count")
    ).reset_index()
    bat["strike_rate"] = (bat["runs"] / bat["balls"]) * 100
    bat["batting_impact"] = bat["runs"] * (bat["strike_rate"] / 100)

    # Bowling Impact = Wickets × (6 / Economy)
    valid_wickets = df[df["wicket_type"].isin([
        "caught", "bowled", "lbw", "stumped", "hit wicket", "caught and bowled"
    ])]
    bowl = df.groupby(["match_id", "bowler"]).agg(
        runs_conceded=("total_runs", "sum"),
        balls_bowled=("ball", "count")
    ).reset_index()
    bowl["overs"] = bowl["balls_bowled"] // 6 + (bowl["balls_bowled"] % 6) / 6
    bowl["economy"] = bowl["runs_conceded"] / bowl["overs"]
    wickets = valid_wickets.groupby(["match_id", "bowler"])["player_dismissed"].count().reset_index()
    wickets.rename(columns={"player_dismissed": "wickets"}, inplace=True)

    bowl = pd.merge(bowl, wickets, on=["match_id", "bowler"], how="left").fillna(0)
    bowl["bowling_impact"] = bowl["wickets"] * (6 / bowl["economy"])

    # Merge batting and bowling impact
    bat.rename(columns={"striker": "player"}, inplace=True)
    bowl.rename(columns={"bowler": "player"}, inplace=True)

    total_impact = pd.merge(bat[["match_id", "player", "batting_impact"]],
                            bowl[["match_id", "player", "bowling_impact"]],
                            on=["match_id", "player"], how="outer").fillna(0)
    total_impact["total_impact"] = total_impact["batting_impact"] + total_impact["bowling_impact"]

    top_impacts = total_impact.groupby("player")["total_impact"].sum().reset_index()
    top_impacts = top_impacts.sort_values(by="total_impact", ascending=False).head(10)

    st.subheader("Top 10 Most Impactful Players")
    st.bar_chart(top_impacts.set_index("player"))
    st.dataframe(top_impacts.set_index("player"))
