import pytest
from src.utils.helpers import validate_url, normalize_url

def test_validate_url_valid():
    assert validate_url("https://help.instagram.com") == True
    assert validate_url("http://example.com/docs") == True

def test_validate_url_invalid():
    assert validate_url("not-a-url") == False
    assert validate_url("ftp://invalid-scheme.com") == False
    assert validate_url("") == False

def test_normalize_url():
    # Should remove trailing slash
    assert normalize_url("https://example.com/") == "https://example.com"
    # Should keep path but remove fragment
    assert normalize_url("https://example.com/doc#section1") == "https://example.com/doc"
    # Should handle spaces
    assert normalize_url(" https://example.com ") == "https://example.com"