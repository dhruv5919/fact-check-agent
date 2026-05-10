import pymupdf as fitz
import re


def extract_text_from_pdf(pdf_file):

    text = ""

    try:

        pdf_bytes = pdf_file.read()

        doc = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        for page in doc:

            page_text = page.get_text()

            text += page_text

        return text

    except Exception as e:

        return f"ERROR: {str(e)}"


def extract_claims(text):

    sentences = re.split(
        r'(?<=[.!?]) +',
        text
    )

    claims = []

    pattern = (
        r'\d+%|'
        r'\$\d+|'
        r'\b(19|20)\d{2}\b|'
        r'million|'
        r'billion'
    )

    for sentence in sentences:

        if re.search(
            pattern,
            sentence,
            re.IGNORECASE
        ):

            claims.append(sentence)

    return claims