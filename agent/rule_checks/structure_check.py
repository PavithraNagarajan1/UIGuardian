from urllib.parse import urljoin

def check_structure(page):
    results = []

    # ✅ Check header
    header = page.query_selector("header")
    if not header:
        results.append("Missing header")
    else:
        header_links = header.query_selector_all("a")
        for link in header_links:
            href = link.get_attribute("href")
            if href and not href.startswith("javascript:"):
                full_url = urljoin(page.url, href)
                try:
                    response = page.request.get(full_url)
                    if response.status != 200:
                        results.append(f"Broken header link: {full_url} (Status: {response.status})")
                except Exception as e:
                    results.append(f"Error loading header link: {full_url}")

    # ✅ Check footer
    footer = page.query_selector("footer")
    if not footer:
        results.append("Missing footer")
    else:
        footer_links = footer.query_selector_all("a")
        for link in footer_links:
            href = link.get_attribute("href")
            if href and not href.startswith("javascript:"):
                full_url = urljoin(page.url, href)
                try:
                    response = page.request.get(full_url)
                    if response.status != 200:
                        results.append(f"Broken footer link: {full_url} (Status: {response.status})")
                except Exception:
                    results.append(f"Error loading footer link: {full_url}")

    # ✅ Check favicon
    rel_values = ["icon", "shortcut icon", "apple-touch-icon", "mask-icon"]
    favicon_found = False

    for rel in rel_values:
        locator = page.locator(f"link[rel='{rel}']")
        count = locator.count()

        for i in range(count):
            href = locator.nth(i).get_attribute("href")
            if href:
                favicon_url = urljoin(page.url, href)
                try:
                    response = page.request.get(favicon_url)
                    if response.status == 200:
                        favicon_found = True
                        break
                except Exception:
                    continue

        if favicon_found:
            break

    if not favicon_found:
        results.append("Missing or inaccessible favicon")

    return results
