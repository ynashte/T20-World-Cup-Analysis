import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def show(df):
    st.header("Bowling Analysis – Top Wicket Takers")

    valid_wickets = df[df["wicket_type"].isin([
        "caught", "bowled", "lbw", "stumped", "hit wicket", "caught and bowled"
    ])]

    bowler_stats = df.groupby("bowler").agg(
        runs_conceded=("total_runs", "sum"),
        balls_bowled=("ball", "count")
    ).reset_index()
    bowler_stats["overs"] = bowler_stats["balls_bowled"] // 6 + (bowler_stats["balls_bowled"] % 6) / 6
    bowler_stats["economy"] = bowler_stats["runs_conceded"] / bowler_stats["overs"]

    wicket_counts = valid_wickets.groupby("bowler")["player_dismissed"].count().reset_index()
    wicket_counts.rename(columns={"player_dismissed": "wickets"}, inplace=True)

    bowler_stats = pd.merge(bowler_stats, wicket_counts, on="bowler", how="left").fillna(0)
    top_bowlers = bowler_stats.sort_values(by=["wickets", "economy"], ascending=[False, True]).head(5)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=top_bowlers, x="wickets", y="bowler", hue="economy", palette="spring", dodge=False, ax=ax)
    ax.set_title("Top 5 Wicket Takers (Hue: Economy Rate)")
    ax.set_xlabel("Wickets")
    ax.set_ylabel("Bowler")
    st.pyplot(fig)

    st.dataframe(top_bowlers[["bowler", "wickets", "economy"]].set_index("bowler"))
