from codex.scraper import extract_companies

HTML = """
<html><body><ul>
<li>Alpha Corp provides solutions.</li>
<li>Beta Inc is cool.</li>
</ul></body></html>
"""


def test_extract_companies_basic():
    companies = extract_companies(HTML)
    names = [c.name for c in companies]
    assert "Alpha Corp" in names
    assert "Beta Inc" in names
