import json
import logging
from pathlib import Path
from typing import Dict, Set

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from codex.categorize import categorize, load_categories
from codex.scraper import scrape_companies
from codex.search import SearchClient
from codex.visualize import create_market_map


@csrf_exempt
def search(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    data = json.loads(request.body.decode())
    query = data.get("query", "")
    client = SearchClient(api_key="dummy")
    urls = client.search(f"{query} list")
    companies = scrape_companies(urls)
    cats = categorize(companies, load_categories())
    serial = {k: sorted(v) for k, v in cats.items()}
    return JsonResponse({"categories": serial})


@csrf_exempt
def generate(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    data = json.loads(request.body.decode())
    categories: Dict[str, Set[str]] = {
        k: set(v) for k, v in data.get("categories", {}).items()
    }
    out = Path("web_map.png")
    create_market_map(categories, output=out)
    logging.info("map generated at %s", out)
    return JsonResponse({"map": str(out)})


# Create your views here.
