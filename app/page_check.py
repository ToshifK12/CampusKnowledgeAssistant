from docling.document_converter import DocumentConverter

result = DocumentConverter().convert(
    "data/pdfs/minot_student_handbook_2026-27.pdf"
)

item = result.document.texts[463]
print("ITEM REFERENCE:", item.self_ref)
print("ITEM 463 TEXT:", repr(item.text))
print("ITEM 463 ORIGINAL:", repr(item.orig))

for source in item.prov:
    print("SOURCE:", source.page_no, source.charspan)

converter = DocumentConverter()

for page_no in (14, 15):
    isolated = converter.convert(
        "data/pdfs/minot_student_handbook_2026-27.pdf",
        page_range=(page_no, page_no),
    )
    print("ISOLATED PAGE:", page_no)
    print(isolated.document.export_to_markdown())