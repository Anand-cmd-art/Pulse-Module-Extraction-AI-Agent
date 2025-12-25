import re
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """Validates if the string is a proper HTTP/HTTPS URL."""
    if not url:
        return False
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except ValueError:
        return False

def normalize_url(url: str) -> str:
    """Removes trailing slashes and fragments to standardize the URL."""
    if not url:
        return ""
    parsed = urlparse(url.strip())
    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return clean_url[:-1] if clean_url.endswith('/') else clean_url