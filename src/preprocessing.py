import pandas as pd

def load_data(path):
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
    last_episode_per_season = df.groupby("season")["number_in_season"].max()
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



def count_outliers_iqr(df, column):
    """Count outliers in a column using the IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers, len(outliers), lower_bound, upper_bound
