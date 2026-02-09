import pdfplumber
import logging

def clean_pdf_text(file_path: str) -> str:
    """
    Extracts text while stripping headers/footers by cropping the page.
    """
    clean_text = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                height = page.height
                width = page.width

                # Crop logic: ignore top 50px and bottom 50px (standard header/footer zones)
                # Ensure height is sufficient for cropping
                if height > 100:
                    bbox = (0, 50, width, height - 50)
                    try:
                        cropped_page = page.within_bbox(bbox)
                        text = cropped_page.extract_text()
                    except ValueError:
                        # Fallback if bbox invalid for some reason
                         text = page.extract_text()
                else:
                    # Page too small to crop headers/footers effectively, take full text
                    text = page.extract_text()

                if text:
                    clean_text.append(text)
    except Exception as e:
        # Logging error but returning empty string to avoid crashing the process flow
        print(f"Error processing PDF {file_path}: {e}")
        return ""

    return "\n".join(clean_text)