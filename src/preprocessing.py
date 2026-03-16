import pandas as pd


def load_data(path):
    """Load the dataset."""
    return pd.read_csv(path)


def add_day_aired(df):
    """Convert date and create day_aired column."""
    df["original_air_date"] = pd.to_datetime(df["original_air_date"])
    df["day_aired"] = df["original_air_date"].dt.day_name()
    return df


def select_columns(df):
    """Keep only required columns."""
    columns = [
        "season",
        "number_in_season",
        'number_in_series',
        "original_air_date",
        "day_aired",
        "imdb_rating",
        "us_viewers_in_millions",
        'title'
    ]
    return df[columns]


def add_is_last_episode(df):
    """Create is_last_episode column indicating the last episode of each season."""
    
    # Get last episode number per season
    last_episode_per_season = df.groupby("season")["number_in_season"].max()
    
    # Map it back to the dataframe and compare
    df["is_last_episode"] = (
        df["number_in_season"] == df["season"].map(last_episode_per_season)
    ).astype(int)
    
    return df


def create_clean_dataframe(path):
    """Full pipeline to generate cleaned dataframe."""
    df = load_data(path)
    df = add_day_aired(df)
    df = select_columns(df)
    df = add_is_last_episode(df)
    return df


def save_dataframe(df, path):
    """Save dataframe to CSV."""
    df.to_csv(path, index=False)


# Run pipeline
#df_clean = create_clean_dataframe("./data/simpsons_episodes.csv")
#save_dataframe(df_clean, "./data/simpsons_episodes_cleaned.csv")