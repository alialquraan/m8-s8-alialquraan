"""Module 8 — Tuesday Stretch (Honors Track): Query Router.

Build a routing layer that classifies an incoming query into one of three
types and dispatches it to a different retrieval pipeline:
    factoid (rare entity, date, figure) -> BM25
    semantic (paraphrastic, descriptive) -> dense
    mixed / unknown -> hybrid (alpha=0.5)
"""

from __future__ import annotations
import re

import weaviate

from retrieval_helpers import bm25_search, dense_search, hybrid_search


def classify_query(query: str) -> str:
    """Return one of "factoid", "semantic", "mixed".

    Two valid implementations are accepted (pick one and explain in
    routing_report.md):

      Rule-based: heuristics over query length, presence of named entities
      (regex for capitalized multi-word phrases), presence of digits,
      exact-phrase quotes.

      Embedding-similarity-based: maintain three labeled exemplar query sets
      (10 each); embed the incoming query; classify to the nearest exemplar
      centroid in embedding space.
    """
    # TODO: implement either rule-based or embedding-based classifier
    query = query.strip()
    q = query.lower()

    words = query.split()

    # Factoid indicators
    has_digits = bool(re.search(r"\d", query))
    has_quotes = '"' in query or "'" in query

    # Capitalized multi-word phrase (named entity heuristic)
    has_named_entity = bool(
        re.search(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b", query)
    )

    if has_digits or has_quotes or has_named_entity:
        return "factoid"

    if len(words) <= 4:
        return "factoid"

    semantic_keywords = [
        "explain",
        "describe",
        "difference",
        "compare",
        "meaning",
        "concept",
        "relationship",
        "advantages",
        "benefits",
        "similar",
        "how",
        "why",
    ]

    if any(keyword in q for keyword in semantic_keywords):
        return "semantic"

    if len(words) >= 8:
        return "semantic"

    return "mixed"


def routed_search(client: weaviate.Client, query: str, k: int, embedder) -> list[str]:
    """Dispatch to BM25 / dense / hybrid based on classify_query(query).

    Return the ordered list of doc_id strings, length <= k.
    """
    # TODO: kind = classify_query(query)
    # TODO: dispatch:
    #         "factoid"  -> bm25_search(client, query, k)
    #         "semantic" -> dense_search(client, query, k, embedder)
    #         else       -> hybrid_search(client, query, k, embedder, alpha=0.5)
    kind = classify_query(query)

    if kind == "factoid":
        return bm25_search(client, query, k)

    if kind == "semantic":
        return dense_search(client, query, k, embedder)

    return hybrid_search(
        client,
        query,
        k,
        embedder,
        alpha=0.5,
    )
