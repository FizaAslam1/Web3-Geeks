"""
Clean up zameen_projects_detailed.csv
--------------------------------------------------------
Keeps only rows that actually have at least one useful extracted
field (developer / amenities / payment_plan_text), drops duplicate
articles, and writes a smaller, ready-to-use CSV for the knowledge
base.

Run:
    python clean_zameen_projects.py
"""

import csv

INPUT_CSV = "data/zameen_projects_detailed.csv"
OUTPUT_CSV = "data/zameen_projects_clean.csv"


def main():
    with open(INPUT_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Loaded {len(rows)} rows from {INPUT_CSV}")

    seen_titles = set()
    cleaned = []

    for row in rows:
        title = row["title"].strip()

        # drop duplicates (same article title seen in blog + news)
        if title in seen_titles:
            continue

        # keep only rows with at least one useful extracted field
        has_developer = bool(row["developer"].strip())
        has_amenities = bool(row["amenities"].strip())
        has_payment = bool(row["payment_plan_text"].strip())

        if not (has_developer or has_amenities or has_payment):
            continue

        seen_titles.add(title)
        cleaned.append(row)

    print(f"Kept {len(cleaned)} rows after filtering + de-duplication")

    if cleaned:
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=cleaned[0].keys())
            writer.writeheader()
            writer.writerows(cleaned)
        print(f"Saved -> {OUTPUT_CSV}")

    # quick breakdown so you can see what's inside the clean file
    with_dev = sum(1 for r in cleaned if r["developer"].strip())
    with_amen = sum(1 for r in cleaned if r["amenities"].strip())
    with_pay = sum(1 for r in cleaned if r["payment_plan_text"].strip())
    with_city = sum(1 for r in cleaned if r["city"].strip())
    print("\nBreakdown of clean file:")
    print(f"  developer filled:    {with_dev}/{len(cleaned)}")
    print(f"  amenities filled:    {with_amen}/{len(cleaned)}")
    print(f"  payment plan filled: {with_pay}/{len(cleaned)}")
    print(f"  city filled:         {with_city}/{len(cleaned)}")


if __name__ == "__main__":
    main()
