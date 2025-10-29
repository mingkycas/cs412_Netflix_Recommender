# rule_based_2.py
import pandas as pd
import os

def implement_rule_2_international_tv_shows(data_path='netflix_titles.csv'):
    """
    Implements Rule 2: Identify the Top 10 International TV Shows
    (non-United States and not co-produced with the US) from the dataset.

    The 'Top 10' is based on the first 10 matching entries in the file order.

    Args:
        data_path (str): The file path to the Netflix titles CSV dataset.

    Returns:
        list of dicts: A list of the top 10 international TV shows with
                      their title, country, release_year, and rating.
    """

    if not os.path.exists(data_path):
        print(f"⚠️ Error: Dataset not found at {data_path}. Returning hardcoded data.")
        return [
            {"title": "Blood & Water", "country": "South Africa", "release_year": 2021, "rating": "TV-MA"},
            {"title": "Kota Factory", "country": "India", "release_year": 2021, "rating": "TV-MA"},
            # Add more sample entries if needed
        ]

    # Try reading the dataset safely
    try:
        df = pd.read_csv(data_path, encoding='utf-8-sig')
    except Exception as e:
        print(f"⚠️ Error reading file: {e}")
        return []

    required_cols = {'type', 'title', 'country', 'release_year', 'rating'}
    if not required_cols.issubset(df.columns):
        print("⚠️ Missing one or more required columns in dataset.")
        return []

    # 1. Filter for TV Shows only
    tv_shows = df[df['type'].str.lower() == 'tv show'].copy()

    # 2. Remove entries with no country listed
    tv_shows = tv_shows[tv_shows['country'].notna()]

    # 3. Exclude shows that include 'United States' in the country list
    non_us_mask = ~tv_shows['country'].str.lower().str.contains('united states', na=False)
    international_tv_shows = tv_shows[non_us_mask].copy()

    # 4. Select the first 10
    top_10 = international_tv_shows.head(10)

    # 5. Select and clean up columns
    top_10 = top_10[['title', 'country', 'release_year', 'rating']].fillna('N/A')

    # 6. Convert to list of dictionaries
    output_list = top_10.to_dict('records')

    return output_list


if __name__ == '__main__':
    top_shows = implement_rule_2_international_tv_shows()
    print("\n--- Top 10 International TV Shows (Rule 2) ---")
    for i, show in enumerate(top_shows, 1):
        print(f"{i}. {show['title']} ({show['country']}) - {show['release_year']} ({show['rating']})")
