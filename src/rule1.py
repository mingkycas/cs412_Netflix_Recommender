# src/rule1.py
import pandas as pd


def get_rule1_movies(csv_path="data/netflix_titles.csv", N=10):
    """
    Rule 1:
    - type == 'Movie'
    - rating in ['PG-13', 'TV-MA']
    - sort by date_added (most recent), fallback to release_year
    Returns: list of top N movie titles
    """
    df = pd.read_csv(csv_path)

    # Normalize column names
    df.columns = [c.strip() for c in df.columns]

    # Ensure required columns exist
    required = {"type", "rating", "date_added", "release_year", "title"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in CSV: {sorted(missing)}")

    # Normalize type and rating (safe conversions)
    df['type'] = df['type'].astype(str).str.strip().str.lower()
    df['rating'] = df['rating'].astype(str).str.strip().str.upper()

    # Keep only movie rows
    movies = df[df['type'] == 'movie'].copy()

    # Keep only specified ratings (normalized)
    allowed = {"PG-13", "TV-MA"}
    movies = movies[movies['rating'].isin(allowed)]

    # Parse date_added safely (coerce errors to NaT)
    movies['date_added_parsed'] = pd.to_datetime(movies['date_added'], errors='coerce')

    # Normalize release_year to numeric (missing -> 0)
    movies['release_year'] = pd.to_numeric(movies['release_year'], errors='coerce').fillna(0).astype(int)

    # Sort: most recent date_added first, then by release_year desc
    movies = movies.sort_values(by=['date_added_parsed', 'release_year'], ascending=[False, False])

    # Select top N unique titles preserving order
    topN = []
    seen = set()
    for t in movies['title'].dropna().tolist():
        if t in seen:
            continue
        seen.add(t)
        topN.append(t)
        if len(topN) >= N:
            break
    return topN


__all__ = ["get_rule1_movies"]
