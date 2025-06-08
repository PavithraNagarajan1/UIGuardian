def check_functionality(page):
    results = []
    links = page.query_selector_all("a")
    for link in links:
        href = link.get_attribute("href")
        if not href:
            results.append("Empty link found")
    if page.query_selector("form"):
        results.append("Form detected")
    if page.query_selector("input[type='search']"):
        results.append("Search input found")
    return results
