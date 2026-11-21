from app.search import semantic_search
from app.keyword_search import keyword_search


def validate_positive_integer(name, value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer.")


def reciprocal_rank_fusion(result_lists, limit=20, k=60):
    validate_positive_integer("limit", limit)
    validate_positive_integer("k", k)

    combined = {}

    for source, results in result_lists.items():
        seen = set()

        for rank, result in enumerate(results, start=1):
            chunk_id = result["chunk_id"]

            if chunk_id in seen:
                continue

            seen.add(chunk_id)

            if chunk_id not in combined:
                combined[chunk_id] = {
                    "chunk_id": chunk_id,
                    "document_id": result["document_id"],
                    "title": result["title"],
                    "page": result["page"],
                    "url": result["url"],
                    "text": result["text"],
                    "rrf_score": 0.0,
                    "source_ranks": {},
                }

            combined[chunk_id]["rrf_score"] += 1.0 / (k + rank)
            combined[chunk_id]["source_ranks"][source] = rank

    ranked = sorted(
        combined.values(),
        key=lambda item: (-item["rrf_score"], item["chunk_id"]),
    )

    return ranked[:limit]


def hybrid_search(question, limit=20, candidate_limit=20, k=60):
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question must be a nonempty string.")

    validate_positive_integer("limit", limit)
    validate_positive_integer("candidate_limit", candidate_limit)
    validate_positive_integer("k", k)

    if not limit <= candidate_limit <= 100:
        raise ValueError("Require limit <= candidate_limit <= 100.")

    semantic_results = semantic_search(question, limit=candidate_limit)
    keyword_results = keyword_search(question, limit=candidate_limit)

    return reciprocal_rank_fusion(
        {
            "semantic": semantic_results,
            "keyword": keyword_results,
        },
        limit=limit,
        k=k,
    )