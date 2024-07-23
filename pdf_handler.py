import io
import PyPDF2

def extract_text_from_pdf(pdf_content: bytes) -> str:
    text = ""
    try:
        reader = PyPDF2.PdfFileReader(io.BytesIO(pdf_content))
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extract_text() or ""
    except Exception as e:
        return str(e)
    return text
