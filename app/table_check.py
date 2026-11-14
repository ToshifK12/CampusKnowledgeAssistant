# Diagnostic experiment for catalog page 84.
# Disabling table structure did not fully fix extraction.
# Not used by the main PDF parser.

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

options = PdfPipelineOptions()
options.do_table_structure = False

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=options)
    }
)

result = converter.convert(
    "data/pdfs/minot_undergraduate_catalog_2026-27.pdf",
    page_range=(84, 84)
)
print(result.status)
print(result.document.export_to_markdown(page_no=84))