from unittest.mock import patch

from market_map import build_market_map


@patch("codex.search.SearchClient.search")
@patch("codex.scraper.fetch")
def test_build_market_map(mock_fetch, mock_search, tmp_path):
    mock_search.return_value = ["http://example.com"]
    html = "<ul><li>Gamma Co does energy solutions</li></ul>"
    mock_fetch.return_value = html
    out_file = tmp_path / "out.png"
    build_market_map("gamma", max_results=1, api_key="k", output=out_file)
    assert out_file.exists()
