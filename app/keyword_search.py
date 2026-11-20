from psycopg.rows import dict_row

from ingest import connect_db


def keyword_search(query, limit=20):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query must be a nonempty string.")

    if isinstance(limit, bool) or not isinstance(limit, int):
        raise ValueError("Limit must be an integer.")

    if not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100.")

    with connect_db() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                WITH search AS (
                    SELECT plainto_tsquery('simple', %s) AS terms
                )
                SELECT
                    chunks.id AS chunk_id,
                    chunks.document_id,
                    documents.title,
                    chunks.page,
                    documents.url,
                    chunks.text,
                    ts_rank(chunks.search_vector, search.terms) AS score
                FROM chunks
                JOIN documents
                    ON chunks.document_id = documents.id
                CROSS JOIN search
                WHERE chunks.search_vector @@ search.terms
                ORDER BY score DESC, chunks.id ASC
                LIMIT %s;
                """,
                (query, limit),
            )

            return cursor.fetchall()