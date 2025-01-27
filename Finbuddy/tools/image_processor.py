import pytesseract
from PIL import Image

def image_processor(image_path: str) -> str:
    """
    Extract text or data from a graph image.
    
    Args:
        image_path (str): The file path to the image.
    
    Returns:
        str: Extracted text or information from the image.
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise ValueError(f"Failed to process the image: {e}")
