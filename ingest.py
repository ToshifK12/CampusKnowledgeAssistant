import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

from app.pdf_parser import extract_pages
from app.chunking import chunk_pages


PROJECT_DIR = Path(__file__).resolve().parent
PDF_DIR = PROJECT_DIR / "data" / "pdfs"
INVENTORY_PATH = PROJECT_DIR / "data" / "document_inventory.md"

EXCLUDED_PAGES = {
    "minot_undergraduate_catalog_2026-27.pdf": {84},
}

load_dotenv(PROJECT_DIR / ".env")


def connect_db():
    return psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


def read_inventory():
    documents = []
    seen_filenames = set()
    seen_urls = set()

    for line in INVENTORY_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line.startswith("|"):
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]

        if cells[0] == "Filename":
            continue

        if all(cell and set(cell) <= set("-: ") for cell in cells):
            continue

        if len(cells) != 6 or not all(cells):
            raise ValueError(f"Invalid inventory row: {line}")

        filename, title, department, year, url, access_level = cells

        if Path(filename).name != filename:
            raise ValueError(f"Expected a filename, not a path: {filename}")

        if filename in seen_filenames or url in seen_urls:
            raise ValueError(f"Duplicate inventory entry: {filename}")

        if not (PDF_DIR / filename).is_file():
            raise FileNotFoundError(f"Missing PDF: {filename}")

        seen_filenames.add(filename)
        seen_urls.add(url)

        documents.append({
            "filename": filename,
            "title": title,
            "department": department,
            "year": year,
            "url": url,
            "access_level": access_level,
        })

    if not documents:
        raise ValueError("The inventory contains no document records.")

    return documents


def save_document(conn, document):
    result = conn.execute(
        """
        INSERT INTO documents
            (title, department, year, url, access_level)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (url) DO UPDATE SET
            title = EXCLUDED.title,
            department = EXCLUDED.department,
            year = EXCLUDED.year,
            access_level = EXCLUDED.access_level
        RETURNING id;
        """,
        (
            document["title"],
            document["department"],
            document["year"],
            document["url"],
            document["access_level"],
        ),
    )

    return result.fetchone()[0]


def ingest_document(document):
    filename = document["filename"]
    pdf_path = PDF_DIR / filename

    print(f"Processing: {filename}", flush=True)
    pages = extract_pages(str(pdf_path))

    excluded = EXCLUDED_PAGES.get(filename, set())
    included_pages = [
        page for page in pages
        if page["page"] not in excluded
    ]

    chunks = chunk_pages(included_pages)

    if not chunks:
        raise ValueError(f"No nonempty chunks extracted from {filename}")

    with connect_db() as conn:
        document_id = save_document(conn, document)

        conn.execute(
            "DELETE FROM chunks WHERE document_id = %s;",
            (document_id,),
        )

        with conn.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO chunks (document_id, page, text)
                VALUES (%s, %s, %s);
                """,
                [
                    (document_id, chunk["page"], chunk["text"])
                    for chunk in chunks
                ],
            )

    print(
        f"Saved document {document_id}: {len(chunks)} chunks. "
        f"Excluded pages: {sorted(excluded)}",
        flush=True,
    )


def main():
    documents = read_inventory()

    for document in documents:
        ingest_document(document)

    print(f"Finished ingesting {len(documents)} documents.")


if __name__ == "__main__":
    main() 