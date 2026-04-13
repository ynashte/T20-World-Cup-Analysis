import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def show(df):
    st.header("Batting Analysis – Top Run Scorers")

    # Calculate stats
    bat_stats = df.groupby("striker").agg(
        runs=("runs_off_bat", "sum"),
        balls=("ball", "count")
    ).reset_index()
    bat_stats["strike_rate"] = (bat_stats["runs"] / bat_stats["balls"]) * 100
    top_batters = bat_stats.sort_values("runs", ascending=False).head(5)

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=top_batters, x="runs", y="striker", hue="strike_rate", palette="Wistia", dodge=False, ax=ax)
    ax.set_title("Top 5 Run Scorers (Hue: Strike Rate)")
    ax.set_xlabel("Runs")
    ax.set_ylabel("Batsman")
    st.pyplot(fig)

    st.dataframe(top_batters.set_index("striker"))
