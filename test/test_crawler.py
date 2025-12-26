import pytest
from unittest.mock import MagicMock, patch
from src.crawler.spider import DocumentationSpider

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.status_code = 200
    # FIX: Added more text to pass the >100 char limit in spider.py
    mock.text = """
    <html>
        <nav>Menu</nav>
        <header>Header</header>
        <main>
            <h1>Real Content</h1>
            <p>This is documentation.</p>
            <p>We need to add a lot of text here to make sure the crawler accepts this page.</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt.</p>
            <p>The spider ignores pages with less than 100 characters to avoid empty pages.</p>
        </main>
        <footer>Footer</footer>
    </html>
    """
    return mock

@patch('requests.get')
def test_crawler_clean_text(mock_get, mock_response):
    mock_get.return_value = mock_response
    
    spider = DocumentationSpider("https://example.com")
    spider.crawl("https://example.com")
    
    # Check if noise (nav, header, footer) was removed
    cleaned_text = spider.get_content()
    
    assert "Menu" not in cleaned_text
    assert "Header" not in cleaned_text
    assert "Real Content" in cleaned_text

@patch('requests.get')
def test_crawler_recursion_limit(mock_get, mock_response):
    mock_get.return_value = mock_response
    
    spider = DocumentationSpider("https://example.com", max_depth=1)
    # Simulate a loop or deep crawl
    spider.crawl("https://example.com", depth=2)
    
    # Should not trigger a request because depth 2 > max_depth 1
    assert mock_get.call_count == 0