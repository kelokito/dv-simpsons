import pandas as pd

# Read dataset
df = pd.read_csv("./data/simpsons_episodes.csv")

# Convert date and create day column
df["original_air_date"] = pd.to_datetime(df["original_air_date"])
df["day_aired"] = df["original_air_date"].dt.day_name()

# Keep required columns
df = df[
    [
        "season",
        "number_in_season",
        "original_air_date",
        "day_aired",
        "imdb_rating",
        "us_viewers_in_millions",
        "views",
    ]
]

# Create is_last_episode column
df["is_last_episode"] = (
    df["number_in_season"] == df.groupby("season")["number_in_season"].transform("max")
).astype(int)

# Save cleaned dataset
df.to_csv("./data/simpsons_episodes_cleaned.csv", index=False)