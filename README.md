# Campus Knowledge Assistant

A project to help Minot State students find answers about course prerequisites, academic policies, and course planning.

Planned answers will use university documents and include citations pointing to the source document and page.

## Current progress

The FastAPI backend runs locally. Its welcome endpoint returns:

```json
{"message": "Welcome"}
```

Document search and question answering are not implemented yet.

Three university documents have been ingested into 969 page-labeled
chunks. All chunks have 1,536-dimensional embeddings stored in Postgres.

## Local setup

You need Python 3 installed. Open a terminal in the project folder.

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Start the development server:

```bash
python -m uvicorn app.main:app --reload
```

## Try the API

- Welcome endpoint: http://127.0.0.1:8000/
- Interactive API documentation: http://127.0.0.1:8000/docs

Press Ctrl+C in the terminal to stop the server.

## Local database

The project uses Postgres 17 with pgvector.

- Container: `campus-db`
- Image: `pgvector/pgvector:pg17`
- Persistent volume: `campus-pgdata`
- Local address: `127.0.0.1:5432`
- Database: `campus_knowledge`
- Database user: `campus_user`

Database settings are stored in a local `.env` file containing:
`POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`.
This file must not be committed.

### Daily use

Open Docker Desktop and wait for its engine to start.

Start the existing database container:

```bash
docker start campus-db
```

Open the database command-line client:

```bash
docker exec -it campus-db psql -U campus_user -d campus_knowledge
```

Exit the client with `\q`. This leaves the database running.

Stop the database container when needed:

```bash
docker stop campus-db
```

The named volume preserves database files when the container is
removed, provided the volume itself is retained.

### Verified

- The database accepts connections.
- The `vector` extension is enabled.
- Python connects through Psycopg and successfully runs `SELECT 1;`.

## PDF extraction checks

The Docling parser returns text paired with PDF page numbers.

- Financial Aid Guide: 8 page records; pages 1, 2, and 4 checked.
- Student Handbook: 62 page records; page 4 checked.
- Undergraduate Catalog: 327 page records; CSCI 160 and CSCI 161
  entries on page 199 checked.

Known limitation: catalog page 84 has table extraction errors.
The total credit value is separated from its label, and some credit
values are missing in the default output. Disabling cell matching or
table reconstruction did not fully resolve this.

Page counts and successful conversion do not prove complete extraction.
Page 84 requires further handling before supporting answers from its tables.

## Text chunking

Extracted pages are split independently into chunks of up to 500
tokens, with a target overlap of 50 tokens between neighboring chunks.
Token counting uses tiktoken for text-embedding-3-small.

Each chunk retains its PDF page number. Chunks do not cross pages.

Checks completed:
- Short text produces one chunk.
- A small example preserves overlap.
- Separate pages retain their page numbers.
- The Financial Aid Guide produces 13 chunks from 8 pages.
- Its largest chunk measures 500 tokens.
- Page 3's neighboring chunks share the expected 50-token overlap.

Fixed token boundaries can split sentences. Chunking does not repair
PDF extraction errors, including the catalog page 84 table limitation.

## Document ingestion

With Docker Desktop and campus-db running, activate the virtual
environment and run:

    python ingest.py

The script reads data/document_inventory.md, processes the listed PDFs,
and stores document metadata and page-labeled chunks in Postgres.
Database credentials are read from the local, uncommitted .env file.

Repeat runs reuse documents by source URL and replace their chunks.
Each document's database replacement runs in one transaction.

Verified ingestion:
- Undergraduate Catalog: 787 chunks.
- Student Handbook: 169 chunks.
- Financial Aid Guide: 13 chunks.
- Total: 969 chunks.

Checks confirmed valid source links, positive page numbers, nonempty
text, and no catalog page 84 chunks. A stored CSCI 161 passage retained
its prerequisite and correct page-199 citation details.

Catalog page 84 is explicitly excluded because of known extraction
errors. Other extraction warnings remain; these checks do not establish
complete content accuracy.

## Embeddings

All 969 stored chunks have embeddings generated with
text-embedding-3-small, using 1,536 dimensions.

The embedding script selects only chunks whose embedding is NULL.

Preview pending work without API requests or database updates:

    python embed_chunks.py --limit 1

Generate and save embeddings for up to N pending chunks:

    python embed_chunks.py --limit N --write

Write mode sends passage text to OpenAI and incurs API charges.
Each successful save is committed separately, allowing interrupted
runs to resume by skipping completed chunks. Run one copy at a time.

Verification: 969 embedded chunks, 0 pending, and all vectors have
1,536 dimensions.

Important: ingest.py currently replaces document chunks, discarding
their existing embeddings. Re-ingestion therefore requires embedding
the replacement chunks again.

Semantic search has not been implemented yet.

## Semantic search

semantic_search(question, limit=20) embeds a question using
text-embedding-3-small and retrieves nearby passage vectors from
Postgres using cosine distance. Lower distances rank first.

Results include chunk ID, document ID, title, PDF page, source URL,
passage text, and distance.

An HNSW index supports cosine-distance search. Its definition is
verified; actual index use by the query planner has not been checked.

Manual check:
- "How do I drop a class?" returned 20 results.
- The relevant Dropping Courses passage from catalog page 22 ranked second.
- Distances were sorted and citation fields were present.

Search retrieves passages; it does not generate a final answer.
Each search makes a paid API request to embed the question.
Relevance is not guaranteed by vector distance alone.

## Keyword search

keyword_search(query, limit=20) uses PostgreSQL full-text search.

A stored generated search_vector column processes each passage with
the simple configuration and updates automatically when its text changes.
A GIN index supports term matching.

Queries use plainto_tsquery and results are ranked by ts_rank,
highest score first. All query terms must match, but they do not
need to be adjacent. This is not exact phrase matching.

Results include passage text, source title, URL, PDF page, IDs,
and a text-match score. No OpenAI API request is needed.

Manual checks:
- CSCI 160 returned 20 results.
- Its course description appeared at rank 5 on catalog page 199.
- Scores were descending and citation fields were present.
- CSCI 999999 returned an empty list.

The GIN index definition is verified; query-plan usage has not
been checked. Ranking does not guarantee answer quality.
Semantic and keyword results are not combined yet.