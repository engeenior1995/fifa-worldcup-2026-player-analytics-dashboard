"""
FIFA World Cup 2026 - Player Performance Dataset
Data Cleaning Script
Author: Muhammad Zarq Ali

This script loads the raw dataset, performs cleaning, and exports
a cleaned CSV ready for analysis and dashboard use.
"""

import pandas as pd
import numpy as np

RAW_PATH = "data/raw_data.csv"
CLEAN_PATH = "data/cleaned_fifa_wc2026_player_performance.csv"


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def fix_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    # Dates
    df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")

    # Categorical columns -> category dtype (saves memory, speeds up dashboard filters)
    cat_cols = [
        "nationality", "team", "position", "preferred_foot", "club_name",
        "stadium", "city", "opponent_team", "tournament_stage", "match_result",
    ]
    for c in cat_cols:
        if c in df.columns:
            df[c] = df[c].astype("category")

    # Ensure numeric columns are numeric (coerce guards against stray strings)
    exclude = set(cat_cols + ["player_id", "player_name", "match_id", "match_date"])
    for c in df.columns:
        if c not in exclude:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    # Numeric performance stats: a missing value for an event-based stat
    # (e.g. saves for an outfield player) legitimately means "0 occurrences".
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Categorical/text columns: fill with explicit "Unknown" flag rather than dropping rows
    obj_cols = df.select_dtypes(include=["object", "category"]).columns
    for c in obj_cols:
        if df[c].isnull().sum() > 0:
            if str(df[c].dtype) == "category" and "Unknown" not in df[c].cat.categories:
                df[c] = df[c].cat.add_categories(["Unknown"])
            df[c] = df[c].fillna("Unknown")

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"Removed {before - after} duplicate rows.")
    return df


def cap_outliers(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """Cap extreme outliers using the IQR method (1.5x rule) for a
    small set of skew-prone metrics, without deleting any rows."""
    for c in cols:
        if c not in df.columns:
            continue
        q1, q3 = df[c].quantile(0.25), df[c].quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        df[c] = df[c].clip(lower=lower, upper=upper)
    return df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["goal_contributions"] = df["goals"] + df["assists"]
    df["shot_conversion_rate"] = np.where(
        df["shots"] > 0, (df["goals"] / df["shots"]).round(3), 0
    )
    df["dribble_success_rate"] = np.where(
        df["dribbles_attempted"] > 0,
        (df["successful_dribbles"] / df["dribbles_attempted"]).round(3),
        0,
    )
    df["match_month"] = df["match_date"].dt.strftime("%Y-%m")
    return df


def run_pipeline():
    print("Loading raw data...")
    df = load_data(RAW_PATH)
    print(f"Initial shape: {df.shape}")

    df = clean_column_names(df)
    df = remove_duplicates(df)
    df = fix_dtypes(df)
    df = handle_missing_values(df)

    outlier_candidates = ["market_value_eur", "top_speed_kmh", "distance_covered_km"]
    df = cap_outliers(df, outlier_candidates)

    df = add_derived_columns(df)

    print(f"Final shape: {df.shape}")
    print(f"Remaining nulls: {df.isnull().sum().sum()}")

    df.to_csv(CLEAN_PATH, index=False)
    print(f"Cleaned dataset saved to: {CLEAN_PATH}")
    return df


if __name__ == "__main__":
    run_pipeline()
