"""Generate a simple market map of companies in a niche sector."""

import os
import re
import json
from typing import Iterable, List, Tuple

import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from serpapi.core import Client
import openai

USER_AGENT = {"User-Agent": "Mozilla/5.0"}

# API key for SerpAPI is read from the SERPAPI_API_KEY environment variable.
# The key is intentionally not stored in this repository. Set the variable
# before running the script or provide it via the ``--api-key`` command-line
# option.
SERPAPI_KEY = os.environ.get("SERPAPI_API_KEY")
# Optional OpenAI key for refining results
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")


def search_results(query: str, max_results: int = 5, api_key: str | None = None) -> List[str]:
    """Return the first ``max_results`` result links for ``query``."""

    key = api_key or SERPAPI_KEY
    if not key:
        raise RuntimeError(
            "SERPAPI_API_KEY environment variable not set; specify --api-key"
        )

    params = {
        "api_key": key,
        "engine": "google",
        "q": query,
        "num": max_results,
    }
    client = Client(api_key=key)
    results = client.search(params)
    links = []
    for r in results.get("organic_results", []):
        links.append(r["link"])
    return links


def extract_companies(url: str) -> List[Tuple[str, str]]:
    """Scrape potential company names from list items and paragraphs."""
    try:
        resp = requests.get(url, headers=USER_AGENT, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed fetching {url}: {e}")
        return []
    soup = BeautifulSoup(resp.text, 'html.parser')
    lines = [li.get_text(" ", strip=True) for li in soup.find_all('li')]
    lines += [p.get_text(" ", strip=True) for p in soup.find_all('p')]
    companies = []
    for line in lines:
        for match in re.finditer(r'([A-Z][A-Za-z0-9&-]*(?: [A-Z][A-Za-z0-9&-]*)*)', line):
            name = match.group(0)
            if len(name.split()) <= 4 and not name.isupper():
                companies.append((name, line))
    return companies


def categorize(companies: Iterable[Tuple[str, str]]):
    """Assign each company to a simple category based on keyword heuristics."""

    categories: dict[str, set[str]] = {}
    for name, text in companies:
        lower = text.lower()
        cat = 'Other'
        if any(k in lower for k in ['air quality', 'climate', 'environment']):
            cat = 'Environmental'
        elif any(k in lower for k in ['occupancy', 'people counting']):
            cat = 'Occupancy'
        elif 'energy' in lower or 'hvac' in lower:
            cat = 'Energy'
        elif any(k in lower for k in ['security', 'motion', 'safety']):
            cat = 'Security'
        categories.setdefault(cat, set()).add(name)
    return categories


def refine_with_gpt(categories: dict[str, set[str]], query: str, api_key: str | None = None) -> dict[str, set[str]]:
    """Use OpenAI's GPT to refine and validate the categorized companies.

    If no API key is provided and the ``OPENAI_API_KEY`` environment variable is
    not set, the original ``categories`` mapping is returned unchanged.
    """

    key = api_key or OPENAI_KEY
    if not key:
        return categories

    openai.api_key = key

    lines = []
    for cat, names in categories.items():
        lines.append(f"{cat}: {', '.join(sorted(names))}")

    prompt = (
        "Refine the following company categories for the market map about '"
        f"{query}'. Remove irrelevant companies and ensure they are grouped into"
        " appropriate categories. Return valid JSON mapping category names to"
        " arrays of company names.\n\n" + "\n".join(lines)
    )

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful research assistant that organizes companies",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        data = json.loads(resp.choices[0].message["content"])
        return {cat: set(names) for cat, names in data.items()}
    except Exception as e:
        print("GPT refinement failed:", e)
        return categories


def create_market_map(categories: dict[str, set[str]], output: str = "market_map.png"):
    """Render the market map as a PNG image."""

    fig, ax = plt.subplots(figsize=(8, 6))
    y = 0
    for cat, names in categories.items():
        ax.text(0.05, 0.9 - y * 0.15, cat, fontsize=12, fontweight="bold")
        for i, name in enumerate(sorted(names)):
            ax.text(0.1, 0.88 - (y * 0.15 + i * 0.04), name, fontsize=10)
        y += 1

    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(output)


def build_market_map(
    sector_query: str,
    max_results: int = 5,
    api_key: str | None = None,
    output: str = "market_map.png",
    openai_key: str | None = None,
) -> None:
    """Fetch company lists and build a market map image."""

    search_query = f"{sector_query} list"
    urls = search_results(search_query, max_results=max_results, api_key=api_key)
    all_companies: List[Tuple[str, str]] = []
    for url in urls:
        all_companies.extend(extract_companies(url))
    categories = categorize(all_companies)
    categories = refine_with_gpt(categories, sector_query, api_key=openai_key)
    create_market_map(categories, output=output)
    print(f"Market map saved to {output}")
    for cat, names in categories.items():
        print(f"\n{cat} ({len(names)} companies):")
        for n in sorted(names):
            print(" -", n)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a market map for a given sector")
    parser.add_argument("query", nargs="*", default=["proptech", "sensor", "companies"], help="sector search terms")
    parser.add_argument("--api-key", dest="api_key", help="SerpAPI key (optional)")
    parser.add_argument("--max-results", type=int, default=5, help="number of Google results to parse")
    parser.add_argument("--output", default="market_map.png", help="output image path")
    parser.add_argument("--openai-key", dest="openai_key", help="OpenAI API key (optional)")
    args = parser.parse_args()

    query_str = " ".join(args.query)
    build_market_map(
        query_str,
        max_results=args.max_results,
        api_key=args.api_key,
        output=args.output,
        openai_key=args.openai_key,
    )

