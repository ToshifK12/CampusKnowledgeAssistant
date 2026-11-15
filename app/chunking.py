import tiktoken

encoding = tiktoken.encoding_for_model("text-embedding-3-small")


def chunk_pages(pages, chunk_size=500, overlap=50):
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "Require chunk_size > 0 and 0 <= overlap < chunk_size"
        )

    chunks = []
    step = chunk_size - overlap

    for page in pages:
        tokens = encoding.encode(page["text"], disallowed_special=())

        for start in range(0, len(tokens), step):
            end = start + chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = encoding.decode(chunk_tokens, errors="strict")

            if chunk_text.strip():
                chunks.append({
                    "page": page["page"],
                    "text": chunk_text,
                })

            if end >= len(tokens):
                break

    return chunks