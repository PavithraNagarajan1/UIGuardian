def check_tracking(page):
    results = []
    tracked_requests = []

    def log_request(request):
        tracked_requests.append(request)

    # Hook request events
    page.on("request", log_request)

    # Reload the page to capture requests
    page.reload(wait_until="networkidle")

    found_utag = any("utag.js" in req.url for req in tracked_requests)
    if not found_utag:
        results.append("Tracking script (utag.js) not found or failed")

    return results
