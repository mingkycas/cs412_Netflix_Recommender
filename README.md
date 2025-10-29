# CS412 — Fifth Laboratory Activity: Recommender Systems Comparison


This repository contains a minimal implementation for the course lab: two recommender systems (Rule-Based and Content-Based) using the provided `netflix_titles.csv` dataset. 

---

### Implementation Requirements

The implementation shall consist of these components:

1) Rule-Based Recommender System

- Implement business rules that generate recommendations using dataset columns such as `type`, `listed_in`, `date_added`, `release_year`, and `rating`.
- Required rules (each rule implemented as its own function returning a list of top-N titles):
	- Rule 1: Recommend the top N movies (where `type == 'Movie'`) that were most recently added (`date_added`) and whose `rating` is either `PG-13` or `TV-MA`.
	- Rule 2: Recommend the top N TV shows (where `type == 'TV Show'`) categorized under an "International TV Shows" entry in the `listed_in` column.

2) Content-Based Filtering Recommender System

- Combine relevant item features (for example: `description` and `listed_in`) into a single textual content representation per item.
- Use TF-IDF vectorization to turn combined text into feature vectors.
- Use cosine similarity to compute similarity between items.
- Implement a simulated user preference by accepting a seed title (e.g., "Zodiac" or "The Queen's Gambit") and display the top N similar items, excluding the seed itself.

---

## Project files

- `main.py` — Runner script. Use it to run rule-based and content-based sections.
- `vectorize.py` — TF-IDF building utilities (combine text features + build vectorizer).
- `cosine.py` — Cosine similarity ranking helper.
- `src/rule1.py` — Example implementation of Rule 1.
- `src/rulebased2.py` — Example implementation of Rule 2 (Top 10 International TV Shows).
- `data/netflix_titles.csv` — Dataset (place it in `data/` before running; do not commit large datasets unless instructed).

## Quick usage

Install dependencies (if needed):

```powershell
pip install -r requirements.txt
```

Run with defaults (top-10 outputs, seed="Jeans"):

```powershell
python .\main.py
```

Common examples:

```powershell
# top-5 recommendations for seed "The Matrix"
python .\main.py --seed "The Matrix" --top 5

# use a different CSV and output folder
python .\main.py -d .\data\netflix_titles_sample.csv -o .\my_outputs

# run only content-based (skip rule1)
python .\main.py --no-rule1
 
# run only Rule 2 (international TV shows) and skip other sections:
```powershell
python .\main.py --no-rule1 --no-content
```

---

## Notes about Rule 2 and outputs

- Rule 2 has been implemented in `src/rulebased2.py` and is now invoked by `main.py`. It returns a list of dictionaries (title, country, release_year, rating) and `main.py` prints the top-N results.
- The script saves Rule 1's results to the output directory as `outputs/rule1_topN.csv` by default. The `outputs/` folder is intentionally not tracked by git (add to `.gitignore`) to avoid committing generated artifacts.
```

---
