import os
import argparse
import pandas as pd

# Import group members' modules
from src.rule1 import get_rule1_movies
from vectorize import build_tfidf
from cosine import get_similar_titles


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Netflix recommender runner")
    p.add_argument("-d", "--data", default="data/netflix_titles.csv", help="Path to Netflix CSV file")
    p.add_argument("-s", "--seed", default="Jeans", help="Seed title for content-based recommender")
    p.add_argument("-n", "--top", type=int, default=10, help="Top-N results to return")
    p.add_argument("-o", "--output", default="outputs", help="Output directory")
    p.add_argument("--no-rule1", action="store_true", help="Skip rule1 section")
    p.add_argument("--no-content", action="store_true", help="Skip content-based section")
    p.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    return p.parse_args()


def main():
    args = parse_args()

    DATA_PATH = args.data
    SEED_TITLE = args.seed
    TOP_N = args.top
    OUTPUT_DIR = args.output

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at '{DATA_PATH}'. Please place netflix_titles.csv in the specified path.")

    df = pd.read_csv(DATA_PATH)
    if args.verbose:
        print("Dataset loaded successfully.")
        print(f"Rows: {len(df)}, Columns: {len(df.columns)}\n")

    # Rule 1
    if not args.no_rule1:
        print("=== RULE 1: Top {n} Movies (PG-13 or TV-MA, Most Recently Added) ===\n".format(n=TOP_N))
        rule1_movies = get_rule1_movies(DATA_PATH, TOP_N)
        print(rule1_movies)
    else:
        rule1_movies = []

    # Rule 2 placeholder
    print("\n=== RULE 2: Top {n} International TV Shows ===".format(n=TOP_N))
    print("(Placeholder: waiting for rule2.py function.)\n")

    # Content-based
    if not args.no_content:
        print(f"=== CONTENT-BASED RECOMMENDER (Seed: '{SEED_TITLE}') ===\n")
        # build_tfidf returns (tfidf_matrix, titles, index_by_title, vectorizer)
        tfidf_matrix, titles, index_by_title, vectorizer = build_tfidf(df)

        try:
            top_similar = get_similar_titles(tfidf_matrix, titles, index_by_title, seed_title=SEED_TITLE, top_n=TOP_N)
            print(f"Top {TOP_N} similar titles to '{SEED_TITLE}':")
            for title, score in top_similar:
                print(f"- {title} (similarity: {score:.3f})")
        except Exception as e:
            print(" Error computing content-based recommendations:", e)

    # Save outputs
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if rule1_movies:
        pd.DataFrame(rule1_movies).to_csv(os.path.join(OUTPUT_DIR, "rule1_topN.csv"), index=False)
        print(f"\n Rule 1 results saved to {os.path.join(OUTPUT_DIR, 'rule1_topN.csv')}")

    print("\nAll selected sections executed successfully!")
    print("Remember to:")
    print("1️ Add Rule 2 function.")
    print("2️ Run again to include all three outputs before submission.")


if __name__ == "__main__":
    main()