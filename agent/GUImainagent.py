import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
from playwright.sync_api import sync_playwright
from rule_checks.media_check import check_media
from rule_checks.structure_check import check_structure
from rule_checks.functionality_check import check_functionality
from rule_checks.tracking_check import check_tracking
from rule_checks.accessibility_check import check_missing_alt, check_contrast
from rule_checks.check_images_cv import check_images_cv
import os
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"C:\Users\Pavithra\AppData\Local\ms-playwright"
def run_agent(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        screenshot_path = "screenshot.png"
        page.screenshot(path=screenshot_path, full_page=True)
        results = {}
        results['media'] = check_media(page)
        results['structure'] = check_structure(page)
        results['functionality'] = check_functionality(page)
        results['tracking'] = check_tracking(page)
        results['accessibility_missing_alt'] = check_missing_alt(page)
        results['accessibility_low_contrast'] = check_contrast(screenshot_path)
        results['broken_images_cv'] = check_images_cv(page)
        browser.close()
    return results, screenshot_path

def run_agent_thread(url):
    try:
        results, screenshot_path = run_agent(url)
        output_text.delete(1.0, tk.END)
        for category, issues in results.items():
            output_text.insert(tk.END, f"\n{category.upper()}:\n")
            if not issues:
                output_text.insert(tk.END, "  No issues found.\n")
            else:
                for issue in issues:
                    output_text.insert(tk.END, f"  - {issue}\n")
        output_text.insert(tk.END, f"\nScreenshot saved at: {screenshot_path}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_run():
    url = url_entry.get()
    if not url.startswith("http"):
        messagebox.showerror("Error", "Please enter a valid URL (starting with http or https).")
        return
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Running checks, please wait...\n")
    Thread(target=run_agent_thread, args=(url,), daemon=True).start()

# --- Tkinter GUI setup ---
root = tk.Tk()
root.title("UI Guardian Agent")

tk.Label(root, text="Enter URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)
run_button = tk.Button(root, text="Run Agent", command=on_run)
run_button.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, width=100, height=30)
output_text.pack(padx=10, pady=10)

root.mainloop()