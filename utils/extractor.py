import pdfplumber
import re
import tempfile


def extract_text_from_pdf(pdf_file):

    text = ""

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp_file:

            tmp_file.write(
                pdf_file.read()
            )

            temp_path = tmp_file.name

        with pdfplumber.open(
            temp_path
        ) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

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