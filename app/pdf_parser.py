from docling.document_converter import DocumentConverter


def extract_pages(pdf_path):
    converter = DocumentConverter()
    initial = converter.convert(pdf_path)
    page_numbers = sorted(initial.document.pages.keys())

    pages = []

    for page_no in page_numbers:
        result = converter.convert(
            pdf_path,
            page_range=(page_no, page_no),
        )
        pages.append({
            "page": page_no,
            "text": result.document.export_to_markdown(),
        })

    return pages