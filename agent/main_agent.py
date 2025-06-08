from playwright.sync_api import sync_playwright
from rule_checks.media_check import check_media
from rule_checks.structure_check import check_structure
from rule_checks.functionality_check import check_functionality
from rule_checks.tracking_check import check_tracking
from rule_checks.accessibility_check import check_missing_alt, check_contrast
import numpy as np

def run_agent(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        # Take screenshot for visual defect detection
        screenshot_path = "screenshot.png"
        page.screenshot(path=screenshot_path, full_page=True)

        results = {}

        # Run each check module
        results['media'] = check_media(page)
        results['structure'] = check_structure(page)
        results['functionality'] = check_functionality(page)
        results['tracking'] = check_tracking(page)
         # Accessibility checks
        results['accessibility_missing_alt'] = check_missing_alt(page)
        results['accessibility_low_contrast'] = check_contrast(screenshot_path)

        browser.close()

    return results, screenshot_path

if __name__ == "__main__":
    url = input("Enter the URL to test: ")
    results, screenshot_path = run_agent(url)
    print("Results:")
    for category, issues in results.items():
        print(f"\n{category.upper()}:")
        for issue in issues:
            print("-", issue)
    print(f"\nScreenshot saved at: {screenshot_path}")