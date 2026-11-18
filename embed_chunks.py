import argparse

from ingest import connect_db
from app.embeddings import embed_text, DIMENSIONS


def get_pending_chunks(conn, limit=1):
    return conn.execute(
        """
        SELECT id, text
        FROM chunks
        WHERE embedding IS NULL
        ORDER BY id
        LIMIT %s;
        """,
        (limit,),
    ).fetchall()


def save_embedding(conn, chunk_id, embedding):
    if len(embedding) != DIMENSIONS:
        raise ValueError("Unexpected embedding dimensions.")

    vector_text = "[" + ",".join(str(value) for value in embedding) + "]"

    result = conn.execute(
        """
        UPDATE chunks
        SET embedding = %s::vector
        WHERE id = %s AND embedding IS NULL;
        """,
        (vector_text, chunk_id),
    )

    if result.rowcount != 1:
        raise RuntimeError(
            f"Chunk {chunk_id} was removed or already has an embedding."
        )


def main():
    parser = argparse.ArgumentParser(
        description="Generate and store missing chunk embeddings."
    )
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    if args.limit <= 0:
        parser.error("--limit must be greater than zero.")

    with connect_db() as conn:
        pending = get_pending_chunks(conn, args.limit)

    print(f"Selected {len(pending)} chunks without embeddings.")

    if not args.write:
        print("Preview only: no API requests or database updates.")
        print("Use --write to generate and save embeddings.")
        return

    for chunk_id, text in pending:
        print(f"Embedding chunk {chunk_id}...", flush=True)
        embedding = embed_text(text)

        with connect_db() as conn:
            save_embedding(conn, chunk_id, embedding)

        print(f"Saved chunk {chunk_id}: {len(embedding)} dimensions.")

    print("Finished.")


if __name__ == "__main__":
    main()