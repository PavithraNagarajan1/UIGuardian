from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

def check_missing_alt(page):
    """
    Checks for <img> tags missing alt text.
    Returns a list of image src attributes with missing/empty alt.
    """
    imgs = page.query_selector_all('img')
    missing_alt = []
    for img in imgs:
        alt = img.get_attribute('alt')
        if alt is None or alt.strip() == "":
            src = img.get_attribute('src')
            missing_alt.append(src)
    return missing_alt

def luminance(rgb):
    r, g, b = [v/255.0 for v in rgb]
    return 0.2126*r + 0.7152*g + 0.0722*b


def check_contrast(image_path, threshold=4.5):
    """
    Checks for low contrast text regions in a screenshot.
    Returns a list of dicts with text, contrast ratio, and bounding box.
    """
    img = Image.open(image_path).convert("RGB")
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    low_contrast = []
    for i, text in enumerate(data['text']):
        if text.strip() != "":
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            region = img.crop((x, y, x+w, y+h))
            text_color = region.resize((1,1)).getpixel((0,0))
            # Sample background color just above the text box
            bg_x = x
            bg_y = max(y-2, 0)
            try:
                bg_color = img.getpixel((bg_x, bg_y))
            except:
                bg_color = (255,255,255)
            L1 = luminance(text_color)
            L2 = luminance(bg_color)
            contrast = (max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)
            if contrast < threshold:
                low_contrast.append({'text': text, 'contrast': round(contrast,2), 'box': (x, y, w, h)})
    return low_contrast

# Example usage (for testing):
if __name__ == "__main__":
    # For check_contrast, provide a screenshot path
    issues = check_contrast("C:/Users/Pavithra/OneDrive/Dokumen/M.tech/sem_4/ui_guardian_project/screenshot.png")
    print("Low contrast text regions:", issues)