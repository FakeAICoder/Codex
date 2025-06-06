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

### Command Line Usage

Run the script from the repository root:

```bash
python src/market_map.py --max-results 5 "proptech sensor companies"
```

The script prints the categorized companies and creates a `market_map.png` image.

Category keywords can be customised in `src/codex/categories.json`.

### Web Application

A small Django backend and Node.js frontend are included.

1. Install Node.js packages:
   ```bash
   cd node && npm install
   ```
2. Run the Django API:
   ```bash
   python webapp/manage.py runserver
   ```
3. In another terminal start the Node frontend:
   ```bash
   node index.js
   ```
The frontend forwards requests to the Django API where company data is
scraped and organised before generating the market map image.
