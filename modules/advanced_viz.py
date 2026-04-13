import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show(df):
    st.title("Advanced Visualizations – India Focus 🇮🇳")

    # Normalize key fields
    df["striker"] = df["striker"].astype(str).str.lower().str.strip()
    df["bowler"] = df["bowler"].astype(str).str.lower().str.strip()
    df["batting_team"] = df["batting_team"].astype(str).str.strip()
    df["bowling_team"] = df["bowling_team"].astype(str).str.strip()

    india_bat_df = df[df["batting_team"].str.lower() == "india"]
    india_bowl_df = df[df["bowling_team"].str.lower() == "india"]

    # 1️⃣ Bar Chart: Top 5 Indian Batters (Runs)
    st.subheader("Top 5 Indian Batters – Total Runs")
    top_indian_batters = (
        india_bat_df.groupby("striker")["runs_off_bat"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=top_indian_batters, x="striker", y="runs_off_bat", palette="bone", ax=ax1)
    ax1.set_title("Top 5 Run Scorers – India")
    ax1.set_xlabel("Batter")
    ax1.set_ylabel("Total Runs")
    st.pyplot(fig1)

    # 2️⃣ Pie Chart: Shot Distribution of Selected Indian Batter
    st.subheader("Shot Type Distribution – Indian Batter")
    batter_choice = st.selectbox("Select Indian Batter", sorted(india_bat_df["striker"].unique()))
    batter_data = india_bat_df[india_bat_df["striker"] == batter_choice]
    shot_counts = batter_data["runs_off_bat"].value_counts().sort_index()
    labels = ['Dot', '1', '2', '3', '4', '6']
    sizes = [shot_counts.get(i, 0) for i in [0, 1, 2, 3, 4, 6]]

    fig2, ax2 = plt.subplots()
    ax2.pie(sizes, labels=labels,startangle=140)
    ax2.set_title(f"Shot Type Distribution – {batter_choice.title()}")
    st.pyplot(fig2)

    # 3️⃣ Line Chart: Indian Bowler Economy over Overs
    st.subheader("Economy Over Overs – Indian Bowler")
    india_bowl_df["over"] = india_bowl_df["ball"].astype(str).str.extract(r'^(\d+)').astype(int)
    bowler_choice = st.selectbox("Select Indian Bowler", sorted(india_bowl_df["bowler"].unique()))
    bowler_data = india_bowl_df[india_bowl_df["bowler"] == bowler_choice]

    economy_by_over = (
        bowler_data.groupby("over")["total_runs"]
        .sum()
        .div(bowler_data.groupby("over")["ball"].count() / 6)
        .reset_index(name="economy")
    )

    fig3, ax3 = plt.subplots()
    sns.lineplot(data=economy_by_over, x="over", y="economy", marker="o", ax=ax3)
    ax3.set_title(f"{bowler_choice.title()} – Economy Over Overs")
    ax3.set_xlabel("Over")
    ax3.set_ylabel("Economy Rate")
    st.pyplot(fig3)

    # 4️⃣ Scatter Plot: Jasprit Bumrah vs Teams – Runs Conceded
    st.subheader("Jasprit Bumrah – Runs Conceded per Match vs Teams")
    bumrah_df = df[df["bowler"] == "jj bumrah"]

    team_runs = (
        bumrah_df.groupby(["batting_team", "match_id"])["total_runs"]
        .sum()
        .reset_index()
        .rename(columns={"batting_team": "opponent_team"})
    )

    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=team_runs,
        x="match_id",
        y="total_runs",
        hue="opponent_team",
        palette="tab10",
        s=120,
        ax=ax4
    )

    ax4.set_title("Jasprit Bumrah – Runs Conceded per Match vs Opponent Teams")
    ax4.set_xlabel("Match ID")
    ax4.set_ylabel("Runs Conceded")
    ax4.legend(title="Opponent Team", bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig4)
