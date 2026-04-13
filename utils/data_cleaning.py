import pandas as pd

# Load the CSV file
df = pd.read_csv("D:\PycharmProjects\T20Dashboard\worldcup2025.csv")

# --- Parse and Clean Columns ---

# Convert date if available
if 'start_date' in df.columns:
    try:
        df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce', dayfirst=True)
    except Exception as e:
        print("Error parsing dates:", e)

# Split ball column into over and ball_in_over
if 'ball' in df.columns:
    df['over'] = df['ball'].astype(str).str.split('.').str[0].astype(int)
    df['ball_in_over'] = df['ball'].astype(str).str.split('.').str[1].astype(int)

# Calculate total runs for the delivery
if {'runs_off_bat', 'extras'}.issubset(df.columns):
    df['total_runs'] = df['runs_off_bat'] + df['extras']
else:
    raise ValueError("Missing 'runs_off_bat' or 'extras' columns")

# Add phase column (Powerplay, Middle, Death)
df['phase'] = pd.cut(
    df['over'],
    bins=[-1, 5, 15, 20],
    labels=['Powerplay', 'Middle', 'Death']
)

# Fill NA for common numerical fields
optional_cols = ['wides', 'noballs', 'byes', 'legbyes', 'penalty', 'runs_off_bat', 'extras']
for col in optional_cols:
    if col in df.columns:
        df[col] = df[col].fillna(0).astype(int)

# Clean up string columns (lowercase, strip)
for col in ['striker', 'non_striker', 'bowler', 'wicket_type', 'player_dismissed']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.lower()

# Optional: Preview the cleaned dataframe
print("Cleaned dataframe preview:")
print(df.head())

# Save cleaned version (optional)
df.to_csv("worldcup2025_cleaned.csv", index=False)
print("Cleaned file saved to data/worldcup2025_cleaned.csv")
