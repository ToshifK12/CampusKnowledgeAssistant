# Campus Knowledge Assistant

A project to help Minot State students find answers about course prerequisites, academic policies, and course planning.

Planned answers will use university documents and include citations pointing to the source document and page.

## Current progress

The FastAPI backend runs locally. Its welcome endpoint returns:

```json
{"message": "Welcome"}
```

Document search and question answering are not implemented yet.

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