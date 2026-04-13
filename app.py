import streamlit as st
from modules import batting_analysis, bowling_analysis, mvp_analysis, advanced_viz, best_xi_selector
import pandas as pd

st.set_page_config(page_title="T20 World Cup 2024 Dashboard", layout="wide")
st.title("T20 World Cup 2024 Insights Dashboard")

# Sidebar
st.sidebar.title("Navigation")
module = st.sidebar.radio("Select Module", [
    "Batting Analysis",
    "Bowling Analysis",
    "MVP per Team",
    "Advanced Visuals",
    "Best World Cup XI Selector"
])


# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("data/worldcup2025_cleaned.csv")
    for col in ['striker', 'non_striker', 'bowler', 'wicket_type', 'player_dismissed']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
    return df

df = load_data()

# Route to modules
if module == "Batting Analysis":
    batting_analysis.show(df)
elif module == "Bowling Analysis":
    bowling_analysis.show(df)
elif module == "MVP per Team":
    mvp_analysis.show(df)
elif module == "Advanced Visuals":
    advanced_viz.show(df)
if module == "Best World Cup XI Selector":
    best_xi_selector.show(df)



