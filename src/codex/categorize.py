"""Categorize companies based on keywords."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Set

from .scraper import Company

CONFIG_PATH = Path(__file__).with_name("categories.json")


def load_categories(config_path: Path = CONFIG_PATH) -> Dict[str, List[str]]:
    with config_path.open() as f:
        return json.load(f)


def categorize(
    companies: Iterable[Company], config: Dict[str, List[str]] | None = None
) -> Dict[str, Set[str]]:
    if config is None:
        config = load_categories()
    result: Dict[str, Set[str]] = {}
    for company in companies:
        lower = company.context.lower()
        category = "Other"
        for cat, keywords in config.items():
            if any(k in lower for k in keywords):
                category = cat
                break
        result.setdefault(category, set()).add(company.name)
    return result
