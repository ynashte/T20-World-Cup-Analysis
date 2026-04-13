import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("D:/PycharmProjects/T20Dashboard/data/worldcup2025_cleaned.csv")

# Normalize strings
for col in ['striker', 'non_striker', 'bowler', 'wicket_type', 'player_dismissed']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.lower()

# Valid wicket types
valid_wickets = df[df["wicket_type"].isin([
    "caught", "bowled", "lbw", "stumped", "hit wicket", "caught and bowled"
])]

# Batter Stats
batter_stats = df.groupby("striker").agg(
    runs=("runs_off_bat", "sum"),
    balls_faced=("ball", "count")
).reset_index()
batter_stats["strike_rate"] = (batter_stats["runs"] / batter_stats["balls_faced"]) * 100
top_batters = batter_stats.sort_values("runs", ascending=False).head(5)

# Bowler Stats
bowler_stats = df.groupby("bowler").agg(
    runs_conceded=("total_runs", "sum"),
    balls_bowled=("ball", "count")
).reset_index()
bowler_stats["overs"] = bowler_stats["balls_bowled"] // 6 + (bowler_stats["balls_bowled"] % 6) / 6
bowler_stats["economy"] = bowler_stats["runs_conceded"] / bowler_stats["overs"]

# Add wickets
wicket_counts = valid_wickets.groupby("bowler")["player_dismissed"].count().reset_index()
wicket_counts.rename(columns={"player_dismissed": "wickets"}, inplace=True)
bowler_stats = pd.merge(bowler_stats, wicket_counts, on="bowler", how="left").fillna(0)
top_bowlers = bowler_stats.sort_values(by=["wickets", "economy"], ascending=[False, True]).head(5)

# Top Batters Plot
plt.figure(figsize=(8, 5))
sns.barplot(x="runs", y="striker", data=top_batters, hue="strike_rate", palette="autumn")
plt.title("🏏 Top 5 Run Scorers in T20 World Cup 2025 (Hue = SR)")
plt.xlabel("Runs")
plt.ylabel("Batsman")
plt.legend(title="Strike Rate")
plt.tight_layout()
plt.show()

# Top Bowlers Plot
plt.figure(figsize=(8, 5))
sns.barplot(x="wickets", y="bowler", data=top_bowlers, hue="economy", palette="Wistia")
plt.title("🎯 Top 5 Wicket Takers in T20 World Cup 2025 (Hue = Economy)")
plt.xlabel("Wickets")
plt.ylabel("Bowler")
plt.legend(title="Economy Rate")
plt.tight_layout()
plt.show()
