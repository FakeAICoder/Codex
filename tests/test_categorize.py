from codex.categorize import categorize
from codex.scraper import Company


def test_categorize_environmental():
    companies = [Company(name="GreenCorp", context="Best air quality sensors")]
    categories = categorize(companies, {"Environmental": ["air quality"]})
    assert categories == {"Environmental": {"GreenCorp"}}
