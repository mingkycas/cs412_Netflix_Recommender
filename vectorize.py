# TF-IDF vectorization 

from __future__ import annotations
from typing import Dict, List, Tuple
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Combine relevant text features into a single text string (listed_in + description)
def combine_text_features(df: pd.DataFrame) -> pd.Series:
    listed_in = df.get("listed_in", "").fillna("").astype(str).str.lower()
    description = df.get("description", "").fillna("").astype(str).str.lower()
    return listed_in + " " + description

# Create TF-IDF features for content-based recommendations
def build_tfidf(
    df: pd.DataFrame,
    *,
    stop_words: str = "english",
    min_df: int = 2,
    ngram_range: tuple[int, int] = (1, 2),
):
    """ Build TF-IDF matrix from DataFrame text features.

    Args:
        df: DataFrame with columns ['title','listed_in','description']
        stop_words: TfidfVectorizer stop words
        min_df: ignore terms that appear in fewer than min_df docs
        ngram_range: n-gram range for TF-IDF (default: unigrams+bigrams) """

    required = {"title", "listed_in", "description"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}")

    content = combine_text_features(df)
    vectorizer = TfidfVectorizer(
        stop_words=stop_words,
        min_df=min_df,
        ngram_range=ngram_range,
    )
    tfidf_matrix = vectorizer.fit_transform(content)

    titles: List[str] = df["title"].fillna("").astype(str).tolist()
    index_by_title: Dict[str, int] = {}
    for i, t in enumerate(titles):
        key = t.strip().lower()
        if key and key not in index_by_title:
            index_by_title[key] = i

    return tfidf_matrix, titles, index_by_title, vectorizer
