# Codex Market Map Generator

This tool generates a one-page market map image by fetching Google search results and scraping company names from the returned pages. It uses [SerpAPI](https://serpapi.com/) for search and BeautifulSoup for HTML parsing.

## Setup

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # for development
   ```
2. Export your SerpAPI key
   ```bash
   export SERPAPI_API_KEY=<your key>
   ```

## Usage

Run the script from the repository root:

```bash
python src/market_map.py --max-results 5 "proptech sensor companies"
```

The script prints the categorized companies and creates a `market_map.png` image.

Category keywords can be customised in `src/codex/categories.json`.
