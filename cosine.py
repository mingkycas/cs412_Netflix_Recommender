# cosine similarity implementation

from __future__ import annotations
from typing import Dict, List, Tuple
import numpy as np
from difflib import get_close_matches
from sklearn.metrics.pairwise import cosine_similarity

# rank titles by cosine similarity to a seed title (exclude the seed itself).
def get_similar_titles(
    tfidf_matrix,
    titles: List[str],  # titles aligned with tfidf_matrix rows
    index_by_title: Dict[str, int],
    seed_title: str,
    top_n: int = 10,
) -> List[Tuple[str, float]]:
   
    key = seed_title.strip().lower()
    if key not in index_by_title:
        suggestions = get_close_matches(key, [t.lower() for t in titles], n=5, cutoff=0.6)
        hint = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
        raise ValueError(f"Seed title '{seed_title}' not found in dataset.{hint}")

    seed_idx = index_by_title[key]
    sim = cosine_similarity(tfidf_matrix[seed_idx], tfidf_matrix).flatten()

    # exclude the seed (and exact duplicate titles)
    same_title_mask = np.array([t.strip().lower() == key for t in titles])
    sim[same_title_mask] = -1.0

    n = min(top_n, int((sim > -1.0).sum()))
    if n == 0:
        return []

    # get top-N indices and sort by similarity descending
    top_idx = np.argpartition(sim, -n)[-n:]
    top_idx = top_idx[np.argsort(sim[top_idx])[::-1]]
    return [(titles[i], float(sim[i])) for i in top_idx]
