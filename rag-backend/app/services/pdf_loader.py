import fitz
import pytesseract

from PIL import Image


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_pdf_text(pdf_path):

    document = fitz.open(pdf_path)

    pages = []

    for page_num in range(len(document)):

        page = document.load_page(page_num)

        text = page.get_text()

        # If no text found -> OCR
        if not text.strip():

            pix = page.get_pixmap()

            img = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            text = pytesseract.image_to_string(img)

        pages.append({
            "page": page_num + 1,
            "text": text
        })

    return pages