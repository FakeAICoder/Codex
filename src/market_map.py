"""Generate a simple market map of companies in a niche sector."""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

from codex.categorize import categorize, load_categories
from codex.scraper import scrape_companies
from codex.search import SearchClient
from codex.visualize import create_market_map
from codex.figma import send_to_figma


def build_market_map(
    sector_query: str,
    max_results: int = 5,
    api_key: str | None = None,
    output: str | Path = "market_map.png",
) -> None:
    """Fetch company lists and build a market map image."""
    key = api_key or os.environ.get("SERPAPI_API_KEY")
    if not key:
        raise RuntimeError("SERPAPI_API_KEY environment variable not set")
    search_query = f"{sector_query} list"
    search_client = SearchClient(api_key=key)
    urls = search_client.search(search_query, max_results=max_results)
    companies = scrape_companies(urls)
    categories = categorize(companies, load_categories())
    create_market_map(categories, output=output)
    send_to_figma(categories)
    for cat, names in categories.items():
        logging.info("%s (%d companies)", cat, len(names))
        for n in sorted(names):
            logging.info(" - %s", n)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a market map for a given sector"
    )
    parser.add_argument(
        "query",
        nargs="*",
        default=["proptech", "sensor", "companies"],
        help="sector search terms",
    )
    parser.add_argument("--api-key", dest="api_key", help="SerpAPI key (optional)")
    parser.add_argument(
        "--max-results", type=int, default=5, help="number of Google results to parse"
    )
    parser.add_argument("--output", default="market_map.png", help="output image path")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

    query_str = " ".join(args.query)
    build_market_map(
        query_str,
        max_results=args.max_results,
        api_key=args.api_key,
        output=args.output,
    )


if __name__ == "__main__":
    main()
