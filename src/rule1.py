# src/rule1.py
import argparse
import sys
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

def _parse_args(argv):
    p = argparse.ArgumentParser(description="Rule 1: top N recently added PG-13 or TV-MA movies")
    p.add_argument("--csv", "-c", default="data/netflix_titles.csv", help="Path to CSV file")
    p.add_argument("--top", "-n", type=int, default=10, help="Number of top titles to return")
    return p.parse_args(argv)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    args = _parse_args(argv)
    try:
        top = get_rule1_movies(csv_path=args.csv, N=args.top)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    print(f"Top {len(top)} Movies (Rule 1):")
    for i, t in enumerate(top, 1):
        print(f"{i}. {t}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
