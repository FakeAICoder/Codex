# Codex Market Map Generator

This repository contains a simple tool for generating one-page market maps from web search results. The main script lives under `src/` and uses [SerpAPI](https://serpapi.com/) to fetch Google results.

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Export your SerpAPI key and optionally your OpenAI key:
   ```bash
   export SERPAPI_API_KEY=<your key>
   export OPENAI_API_KEY=<your OpenAI key>
   ```

If SerpAPI returns a 401 error when running the script, verify that your API key is valid and has remaining quota.

## Usage

Run the script from the repository root. If an OpenAI key is provided, the
results will be refined using GPT for more accurate categorization:

```bash
python src/market_map.py --max-results 5 "proptech sensor companies" \
    --openai-key $OPENAI_API_KEY
```

The script will print a categorized list of companies and save a `market_map.png` image in the working directory.
