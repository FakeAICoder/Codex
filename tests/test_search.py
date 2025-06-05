from unittest.mock import patch

from codex.search import SearchClient


def test_search_client_parses_links():
    with patch("codex.search.Client") as mock_cls:
        instance = mock_cls.return_value
        instance.search.return_value = {
            "organic_results": [{"link": "http://example.com"}]
        }
        client = SearchClient(api_key="dummy")
        links = client.search("query")
        assert links == ["http://example.com"]
        instance.search.assert_called_once()
