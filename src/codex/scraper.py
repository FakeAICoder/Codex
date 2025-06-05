"""HTML scraping utilities."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Iterable, List

import requests
from bs4 import BeautifulSoup

USER_AGENT = {"User-Agent": "Mozilla/5.0"}

COMPANY_PATTERN = re.compile(r"([A-Z][A-Za-z0-9&-]*(?: [A-Z][A-Za-z0-9&-]*)*)")


@dataclass
class Company:
    """Represents a company entry."""

    name: str
    context: str


def fetch(url: str) -> str | None:
    """Fetch a URL and return its text content or ``None`` on error."""
    try:
        logging.debug("Fetching %s", url)
        resp = requests.get(url, headers=USER_AGENT, timeout=10)
        resp.raise_for_status()
        return resp.text
    except Exception as exc:  # noqa: BLE001
        logging.warning("Failed fetching %s: %s", url, exc)
        return None


def extract_companies(html: str) -> List[Company]:
    """Extract companies from HTML list elements."""
    soup = BeautifulSoup(html, "html.parser")
    lines = [li.get_text(" ", strip=True) for li in soup.find_all("li")]
    companies: List[Company] = []
    for line in lines:
        for match in COMPANY_PATTERN.finditer(line):
            name = match.group(0)
            if len(name.split()) <= 4 and not name.isupper():
                companies.append(Company(name=name, context=line))
    return companies


def scrape_companies(urls: Iterable[str]) -> List[Company]:
    """Fetch all URLs and extract companies."""
    all_companies: List[Company] = []
    for url in urls:
        html = fetch(url)
        if html:
            all_companies.extend(extract_companies(html))
    return all_companies
