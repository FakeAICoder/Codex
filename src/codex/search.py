"""Search utilities using SerpAPI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from serpapi.core import Client


@dataclass
class SearchClient:
    """Wrapper for SerpAPI search."""

    api_key: str

    def search(self, query: str, max_results: int = 5) -> List[str]:
        client = Client(api_key=self.api_key)
        params = {
            "api_key": self.api_key,
            "engine": "google",
            "q": query,
            "num": max_results,
        }
        results = client.search(params)
        return [r["link"] for r in results.get("organic_results", [])]
