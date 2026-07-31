#!/usr/bin/env python3
"""Download FWC unfair dismissal decisions from 2019-2026.

Usage:
    python scripts/download_fwc_decisions.py [--start-year 2019] [--end-year 2026] [--max-decisions 100]

Requirements:
    pip install requests beautifulsoup4

Output:
    data/fwc_decisions/ — one JSON file per decision
"""

import os
import sys
import json
import time
import argparse
import logging
import hashlib
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# FWC decisions base URL
FWC_DECISIONS_URL = "https://www.fwc.gov.au/documents/decisionssigned/html/"

# Unfair dismissal keywords for filtering
UNFAIR_DISMISSAL_KEYWORDS = [
    "unfair dismissal",
    "unfairly dismissed",
    "dismissed unfairly",
    "harsh, unjust or unreasonable",
    "s 385",
    "s.385",
    "section 385",
    "Part 3-2",
    "Division 4",
    "general protections",
    "s 365",
    "s.365",
]


def get_decision_page_urls(start_year: int = 2019, end_year: int = 2026) -> list[str]:
    """Get list of decision page URLs from FWC website."""
    import requests
    from bs4 import BeautifulSoup

    urls = []

    # FWC decision index pages are organized by year
    for year in range(start_year, end_year + 1):
        index_url = f"{FWC_DECISIONS_URL}?Start={year}"
        logger.info(f"Fetching index for year {year}: {index_url}")

        try:
            response = requests.get(index_url, timeout=30, headers={
                "User-Agent": "Mozilla/5.0 (compatible; FairWorkRAGBot/1.0)"
            })
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Find decision links
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if "decisionssigned/html/" in href and href.endswith(".htm"):
                    full_url = href if href.startswith("http") else f"https://www.fwc.gov.au/{href}"
                    urls.append(full_url)

            logger.info(f"  Found {len(urls)} total decision links for {year}")
            time.sleep(1)  # Rate limiting

        except Exception as e:
            logger.error(f"  Failed to fetch index for {year}: {e}")

    return list(set(urls))


def download_decision(url: str) -> dict | None:
    """Download and parse a single FWC decision."""
    import requests
    from bs4 import BeautifulSoup

    try:
        response = requests.get(url, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (compatible; FairWorkRAGBot/1.0)"
        })
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract metadata
        title = soup.find("title")
        title_text = title.text.strip() if title else "Unknown"

        # Extract case name from title
        case_name = title_text.split("-")[0].strip() if "-" in title_text else title_text

        # Extract full text
        body = soup.find("body")
        full_text = body.get_text(separator="\n", strip=True) if body else ""

        # Extract decision date (if available in text)
        date_str = ""
        date_patterns = [
            "decision date:",
            "date of decision:",
            "date:",
            "issued:",
        ]
        for line in full_text.split("\n"):
            line_lower = line.lower().strip()
            for pattern in date_patterns:
                if pattern in line_lower:
                    date_str = line.split(":", 1)[1].strip() if ":" in line else ""
                    break
            if date_str:
                break

        # Check if unfair dismissal
        is_unfair_dismissal = any(
            keyword.lower() in full_text.lower()
            for keyword in UNFAIR_DISMISSAL_KEYWORDS
        )

        if not is_unfair_dismissal:
            logger.debug(f"  Skipping {url} — not unfair dismissal")
            return None

        # Extract member name
        member = ""
        member_patterns = [
            "member:",
            "before:",
            "presiding:",
        ]
        for line in full_text.split("\n"):
            line_lower = line.lower().strip()
            for pattern in member_patterns:
                if pattern in line_lower:
                    member = line.split(":", 1)[1].strip() if ":" in line else ""
                    break
            if member:
                break

        # Build citation from filename
        filename = url.split("/")[-1].replace(".htm", "")

        return {
            "case_name": case_name,
            "citation": filename,
            "url": url,
            "member": member,
            "decision_date": date_str,
            "full_text": full_text,
            "is_unfair_dismissal": True,
            "downloaded_at": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"  Failed to download {url}: {e}")
        return None


def save_decision(decision: dict, output_dir: Path):
    """Save decision as JSON file."""
    filename = f"{decision['citation']}.json"
    filepath = output_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(decision, f, indent=2, ensure_ascii=False)

    return filepath


def main():
    parser = argparse.ArgumentParser(description="Download FWC unfair dismissal decisions")
    parser.add_argument("--start-year", type=int, default=2019, help="Start year (default: 2019)")
    parser.add_argument("--end-year", type=int, default=2026, help="End year (default: 2026)")
    parser.add_argument("--max-decisions", type=int, default=100, help="Max decisions to download (default: 100)")
    parser.add_argument("--output-dir", type=str, default="data/fwc_decisions", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Check for existing decisions to avoid re-downloading
    existing_files = set(f.stem for f in output_dir.glob("*.json"))
    logger.info(f"Found {len(existing_files)} existing decisions")

    # Get decision URLs
    logger.info(f"Getting decision URLs for {args.start_year}-{args.end_year}...")
    urls = get_decision_page_urls(args.start_year, args.end_year)
    logger.info(f"Found {len(urls)} decision URLs")

    # Filter out already downloaded
    new_urls = [u for u in urls if u.split("/")[-1].replace(".htm", "") not in existing_files]
    logger.info(f"New URLs to download: {len(new_urls)}")

    # Download decisions
    downloaded = 0
    skipped = 0

    for i, url in enumerate(new_urls):
        if downloaded >= args.max_decisions:
            logger.info(f"Reached max decisions ({args.max_decisions}). Stopping.")
            break

        decision = download_decision(url)
        if decision:
            filepath = save_decision(decision, output_dir)
            downloaded += 1
            logger.info(f"[{downloaded}/{args.max_decisions}] Downloaded: {decision['case_name'][:60]}")
        else:
            skipped += 1

        # Rate limiting
        if (i + 1) % 10 == 0:
            time.sleep(2)

    logger.info(f"\nDone! Downloaded: {downloaded}, Skipped: {skipped}")
    logger.info(f"Output directory: {output_dir}")


if __name__ == "__main__":
    main()
