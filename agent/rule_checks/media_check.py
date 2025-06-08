def check_media(page):
    results = []
    images = page.query_selector_all("img")
    for img in images:
        src = img.get_attribute("src")
        if not src or "data:image" in src:
            results.append(f"Broken or missing image: {src}")
    return results
