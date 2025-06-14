import cv2
import numpy as np
import requests

def check_images_cv(page):
    broken_images = []
    img_urls = page.eval_on_selector_all("img", "elements => elements.map(e => e.src)")
    for url in img_urls:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            img_array = np.asarray(bytearray(resp.content), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is None or img.shape[0] == 0 or img.shape[1] == 0:
                broken_images.append(f"{url} (Image could not be decoded or is empty)")
        except Exception as e:
            broken_images.append(f"{url} ({str(e)})")
    return broken_images