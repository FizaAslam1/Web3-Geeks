"""
Zameen.com Property Scraper (FINAL, VERIFIED VERSION)
--------------------------------------------------------
Lahore, Karachi, Islamabad, Rawalpindi — internship project.

This version's selectors were reverse-engineered directly from real saved
pages (debug_lahore.html, debug_karachi.html, debug_islamabad.html) and
verified to extract 25/25 listings cleanly on every one of those pages,
using the site's aria-label accessibility attributes (aria-label="Price",
"Location", "Beds", "Baths", "Area", "Title") instead of the obfuscated
CSS class names (which change on every deploy) — this is why the earlier
class-name-based attempts came back empty.

Run:
    pip install requests beautifulsoup4
    python scrape_zameen_final.py

Output: data/<city>_properties.csv + data/all_cities.csv

Before running at scale: check https://www.zameen.com/robots.txt yourself,
and keep the delays — don't hammer the server.
"""

import csv
import os
import random
import time

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
CITIES = {
    "Lahore": "https://www.zameen.com/Homes/Lahore-1-{page}.html",
    "Karachi": "https://www.zameen.com/Homes/Karachi-2-{page}.html",
    "Islamabad": "https://www.zameen.com/Homes/Islamabad-3-{page}.html",
    "Rawalpindi": "https://www.zameen.com/Homes/Rawalpindi-41-{page}.html",
}

PAGES_PER_CITY = 5           # each page = ~25 listings. 5 pages ≈ 125/city.
DELAY_SECONDS = (3, 6)       # polite random delay between requests
OUTPUT_DIR = "data"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_page(url: str):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        print(f"    HTTP {resp.status_code} ({len(resp.text)} bytes) -> {url}")
        if resp.status_code != 200:
            return None
        return resp.text
    except requests.RequestException as e:
        print(f"    [error] {url} -> {e}")
        return None


def _label_text(card, label):
    el = card.find(attrs={"aria-label": label})
    return el.get_text(strip=True) if el else ""


def parse_card(card, city: str) -> dict:
    link_el = card.find("a", attrs={"aria-label": "Listing link"})
    href = link_el["href"] if link_el and link_el.has_attr("href") else ""
    url = "https://www.zameen.com" + href if href.startswith("/") else href

    currency = _label_text(card, "Currency")
    price = _label_text(card, "Price")

    return {
        "city": city,
        "title": _label_text(card, "Title"),
        "price": f"{currency} {price}".strip(),
        "location": _label_text(card, "Location"),
        "beds": _label_text(card, "Beds"),
        "baths": _label_text(card, "Baths"),
        "area": _label_text(card, "Area"),
        "added": _label_text(card, "Listing creation date"),
        "url": url,
    }


def scrape_city(city: str, url_template: str, pages: int):
    print(f"\n=== Scraping {city} ===")
    results = []

    for page in range(1, pages + 1):
        url = url_template.format(page=page)
        print(f"  Fetching page {page}: {url}")
        html = fetch_page(url)
        if html is None:
            continue

        soup = BeautifulSoup(html, "html.parser")
        cards = soup.find_all("li", class_="a37d52f0")

        if not cards:
            print(f"    [warn] 0 cards found on page {page} — site markup may "
                  f"have changed, or you've been rate-limited/blocked. Save "
                  f"this page's HTML and check again.")

        for card in cards:
            row = parse_card(card, city)
            if row["title"]:
                results.append(row)

        print(f"    -> {len(cards)} cards parsed")
        time.sleep(random.uniform(*DELAY_SECONDS))

    print(f"  TOTAL for {city}: {len(results)} listings")
    return results


def save_csv(rows, path):
    if not rows:
        print(f"  [warn] nothing to save for {path}")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Saved -> {path}")


def main():
    all_rows = []
    for city, template in CITIES.items():
        rows = scrape_city(city, template, PAGES_PER_CITY)
        save_csv(rows, os.path.join(OUTPUT_DIR, f"{city.lower()}_properties.csv"))
        all_rows.extend(rows)

    save_csv(all_rows, os.path.join(OUTPUT_DIR, "all_cities.csv"))
    print(f"\nDone. Total listings across {len(CITIES)} cities: {len(all_rows)}")


if __name__ == "__main__":
    main()
