import pandas as pd

def load_data(path):
    """Load dataset from CSV."""
    return pd.read_csv(path)


def print_info(df):
    """Print dataframe info."""
    print(df.info())


def print_null_values(df):
    """Print number of null values per column."""
    print("\nNull values per column:")
    print(df.isnull().sum())


def print_unique_values(df):
    """Print number of unique values per column."""
    print("\nUnique values per column:")
    print(df.nunique())


def count_outliers_iqr(df, column):
    """Count outliers in a column using the IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return len(outliers)


def print_outliers(df, columns):
    """Print number of outliers for selected columns."""
    print("\nNumber of outliers (IQR method):")
    for col in columns:
        print(f"{col}: {count_outliers_iqr(df, col)}")


def main():
    df = load_data("./data/simpsons_episodes_cleaned.csv")

    print_info(df)
    print_null_values(df)
    print_unique_values(df)

    columns_to_check = ["imdb_rating", "us_viewers_in_millions", "views"]
    print_outliers(df, columns_to_check)


if __name__ == "__main__":
    main()