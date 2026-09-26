"""
Zameen.com BLOG/NEWS Project Scraper (WordPress REST API)
--------------------------------------------------------
Fills the gaps the listing scraper can't: developer, amenities, and
payment plan info, by reading Zameen's "New Developments" articles
instead of individual property pages.

Why this works well:
    zameen.com/blog and zameen.com/news both run on WordPress, and
    WordPress always exposes a public JSON REST API:

        https://www.zameen.com/blog/wp-json/wp/v2/posts
        https://www.zameen.com/news/wp-json/wp/v2/posts

    This returns clean JSON (title, full HTML content, categories,
    tags) -- no obfuscated class names to reverse-engineer. Articles
    in the "new-developments" category are specifically about launched
    projects (Bahria, DHA, Zameen Developments, private developers
    etc.) and routinely include a payment-plan table, a "Location &
    Amenities" section, and the developer's name in the body text.

What this script does:
    1. Finds the "new-developments" category ID (falls back to
       scanning all posts if the category can't be found).
    2. Pages through every post in that category, for both
       /blog and /news sub-sites.
    3. Strips each post's HTML content down to plain text, then
       best-effort extracts:
         - developer        (regex over known patterns + title)
         - amenities         (text after an "Amenities" heading)
         - payment_plan_text (text around "payment plan" / "instalment")
         - city              (matched against a known city list)
    4. Saves everything to CSV -- both the extracted fields AND the
       full cleaned article text, so nothing is silently lost if the
       regex extraction misses something. Review the CSV afterward;
       treat the extracted columns as a head start, not ground truth.

Run:
    pip install requests beautifulsoup4
    python scrape_zameen_projects.py
"""

import csv
import os
import re
import time

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
SUB_SITES = {
    "blog": "https://www.zameen.com/blog/wp-json/wp/v2",
    "news": "https://www.zameen.com/news/wp-json/wp/v2",
}

CATEGORY_NAME_HINTS = ["new-developments", "new developments", "projects"]

POSTS_PER_PAGE = 100     # WordPress API max
MAX_PAGES = 20           # safety cap (20 x 100 = 2000 posts per sub-site)
DELAY_SECONDS = 1.5      # JSON API is light -- shorter delay than HTML scraping

OUTPUT_CSV = "data/zameen_projects_detailed.csv"

CITIES = ["Lahore", "Karachi", "Islamabad", "Rawalpindi", "Faisalabad",
          "Multan", "Peshawar", "Sialkot", "Gujranwala", "Bahawalpur"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def api_get(url, params=None):
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=20)
        if resp.status_code != 200:
            print(f"    [warn] HTTP {resp.status_code} -> {url}")
            return None
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        print(f"    [error] {url} -> {e}")
        return None


def find_category_id(base_url):
    """Look up the 'new-developments' (or similar) category ID for this sub-site."""
    data = api_get(f"{base_url}/categories", params={"per_page": 100})
    if not data:
        return None
    for cat in data:
        slug = cat.get("slug", "").lower()
        name = cat.get("name", "").lower()
        for hint in CATEGORY_NAME_HINTS:
            if hint in slug or hint in name:
                print(f"    Found category: {cat.get('name')} (id={cat.get('id')})")
                return cat.get("id")
    print("    [warn] No matching category found -- will scan all posts instead.")
    return None


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html or "", "html.parser")
    for tag in soup(["script", "style", "figure", "img"]):
        tag.decompose()
    text = soup.get_text("\n", strip=True)
    return text


def guess_city(text: str) -> str:
    for city in CITIES:
        if re.search(rf"\b{city}\b", text, re.IGNORECASE):
            return city
    return ""


def extract_developer(text: str) -> str:
    # Common phrasing: "developed by X", "X Developments", "developer, X"
    patterns = [
        r"developed by ([A-Z][A-Za-z0-9&.,\-' ]{2,50}?)(?:[.,\n]|$)",
        r"([A-Z][A-Za-z0-9&.,\-' ]{2,50}? Developments?)\b",
        r"developer[,:]?\s+([A-Z][A-Za-z0-9&.,\-' ]{2,50}?)(?:[.,\n]|$)",
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return m.group(1).strip()
    return ""


def extract_section(text: str, heading_keywords) -> str:
    """
    Grab the paragraph(s) following a line that looks like a heading
    matching one of heading_keywords (case-insensitive substring match).
    Falls back to "" if nothing found.
    """
    lines = text.split("\n")
    for i, line in enumerate(lines):
        line_clean = line.strip().lower()
        if any(kw in line_clean for kw in heading_keywords) and len(line_clean) < 60:
            # collect the next few non-empty lines as the section body
            body = []
            for follow in lines[i + 1: i + 6]:
                if follow.strip():
                    body.append(follow.strip())
                if len(body) >= 3:
                    break
            if body:
                return " | ".join(body)
    return ""


def extract_payment_plan(text: str) -> str:
    keywords = ["payment plan", "installment", "instalment", "booking amount", "down payment"]
    lower = text.lower()
    if not any(k in lower for k in keywords):
        return ""
    # grab a window of text around the first keyword hit
    idx = min((lower.find(k) for k in keywords if k in lower), default=-1)
    if idx == -1:
        return ""
    window = text[max(0, idx - 100): idx + 500].strip()
    return window.replace("\n", " | ")


def parse_post(post: dict) -> dict:
    title = clean_html(post.get("title", {}).get("rendered", ""))
    content_html = post.get("content", {}).get("rendered", "")
    text = clean_html(content_html)
    link = post.get("link", "")

    return {
        "title": title,
        "url": link,
        "city": guess_city(title + " " + text[:500]),
        "developer": extract_developer(text),
        "amenities": extract_section(text, ["amenities", "location & amenities", "features"]),
        "payment_plan_text": extract_payment_plan(text),
        "full_text": text[:3000],  # capped so the CSV stays manageable; raise if you need more
    }


def scrape_sub_site(name: str, base_url: str) -> list:
    print(f"\n=== Scraping {name} ({base_url}) ===")
    category_id = find_category_id(base_url)

    all_rows = []
    for page in range(1, MAX_PAGES + 1):
        params = {"per_page": POSTS_PER_PAGE, "page": page}
        if category_id:
            params["categories"] = category_id

        print(f"  Page {page} ...")
        data = api_get(f"{base_url}/posts", params=params)
        if not data:
            break  # no more pages, or API rejected page number (WP returns 400 past last page)

        for post in data:
            row = parse_post(post)
            row["source"] = name
            all_rows.append(row)

        print(f"    -> {len(data)} posts (running total: {len(all_rows)})")

        if len(data) < POSTS_PER_PAGE:
            break  # last page

        time.sleep(DELAY_SECONDS)

    print(f"  TOTAL for {name}: {len(all_rows)} project articles")
    return all_rows


def save_csv(rows, path):
    if not rows:
        print(f"[warn] nothing to save for {path}")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved -> {path} ({len(rows)} rows)")


def main():
    all_rows = []
    for name, base_url in SUB_SITES.items():
        all_rows.extend(scrape_sub_site(name, base_url))

    save_csv(all_rows, OUTPUT_CSV)

    # quick summary so you can see extraction quality without opening the CSV
    with_developer = sum(1 for r in all_rows if r["developer"])
    with_amenities = sum(1 for r in all_rows if r["amenities"])
    with_payment = sum(1 for r in all_rows if r["payment_plan_text"])
    print(f"\nExtraction summary:")
    print(f"  developer found:    {with_developer}/{len(all_rows)}")
    print(f"  amenities found:    {with_amenities}/{len(all_rows)}")
    print(f"  payment plan found: {with_payment}/{len(all_rows)}")
    print("\nReview data/zameen_projects_detailed.csv -- 'full_text' column has the")
    print("raw article text for anything the regex extraction missed or got wrong.")


if __name__ == "__main__":
    main()
