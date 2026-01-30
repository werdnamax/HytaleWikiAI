from bs4 import BeautifulSoup
import requests
import json
import os

__author__ = "Andrew Flerchinger"
__sources__ = ["Hytale Wiki", "https://hytalewiki.org/", "GPT-5.2"]
__Date__ = "2026-01-30"


def scrape_webpage(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    os.makedirs("output", exist_ok=True)
    data = {"url": url, "html": soup.prettify()}

    # Save to JSON file might change later. 
    out_path = os.path.join("output", f"{os.path.basename(url)}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return out_path


def main():
    test_url = "https://hytalewiki.org"
    scrape_webpage(test_url)
    
# rn the trigger file might change later.
if __name__ == "__main__":
    main()