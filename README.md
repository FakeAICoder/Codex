# Codex Market Map Generator

This repository contains a simple tool for generating one-page market maps from web search results. The main script lives under `src/` and uses [SerpAPI](https://serpapi.com/) to fetch Google results.

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Export your SerpAPI key:
   ```bash
   export SERPAPI_API_KEY=<your key>
   ```

## Usage

Run the script from the repository root:

```bash
python src/market_map.py --max-results 5 "proptech sensor companies"
```

The script will print a categorized list of companies and save a `market_map.png` image in the working directory.
