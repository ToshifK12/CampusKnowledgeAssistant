from psycopg.rows import dict_row

from ingest import connect_db
from app.embeddings import embed_text


def semantic_search(question, limit=20):
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question must be a nonempty string.")

    if isinstance(limit, bool) or not isinstance(limit, int):
        raise ValueError("Limit must be an integer.")

    if not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100.")

    question_embedding = embed_text(question)

    vector_text = (
        "[" + ",".join(str(value) for value in question_embedding) + "]"
    )

    with connect_db() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT
                    chunks.id AS chunk_id,
                    chunks.document_id,
                    documents.title,
                    chunks.page,
                    documents.url,
                    chunks.text,
                    chunks.embedding <=> %s::vector AS distance
                FROM chunks
                JOIN documents
                    ON chunks.document_id = documents.id
                WHERE chunks.embedding IS NOT NULL
                ORDER BY chunks.embedding <=> %s::vector
                LIMIT %s;
                """,
                (vector_text, vector_text, limit),
            )

            return cursor.fetchall()