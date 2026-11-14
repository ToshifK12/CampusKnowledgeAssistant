from docling.document_converter import DocumentConverter

def extract_pages(pdf_path):
    converter = DocumentConverter()
    result = converter.convert(pdf_path)

    pages = []
    for page_no in sorted(result.document.pages.keys()):
        page_text = result.document.export_to_markdown(page_no=page_no)
        pages.append({"page": page_no, "text": page_text})
    return pages