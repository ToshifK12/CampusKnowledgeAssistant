CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    department TEXT NOT NULL,
    url TEXT NOT NULL CONSTRAINT documents_url_unique UNIQUE,
    access_level TEXT NOT NULL,
    year TEXT NOT NULL
);

CREATE TABLE chunks (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_id BIGINT NOT NULL REFERENCES documents(id),
    page INTEGER NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(1536),
    search_vector TSVECTOR
    GENERATED ALWAYS AS (to_tsvector('simple', text)) STORED
);

CREATE INDEX chunks_embedding_hnsw
ON chunks USING hnsw (embedding vector_cosine_ops);

CREATE INDEX chunks_search_vector_gin
ON chunks USING gin (search_vector);