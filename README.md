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