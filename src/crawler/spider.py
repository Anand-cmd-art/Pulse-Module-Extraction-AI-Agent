import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class DocumentationSpider:
    def __init__(self, base_url: str, max_depth: int = 2):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited = set()
        self.corpus = []
        self.max_depth = max_depth

    def is_internal(self, url: str) -> bool:
        """Checks if the link belongs to the same domain."""
        return urlparse(url).netloc == self.domain

    def clean_text(self, html: str) -> str:
        """Removes headers, footers, and navbars to extract clean content."""
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup(['header', 'footer', 'nav', 'script', 'style', 'aside', 'form']):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)

    def crawl(self, url: str, depth: int = 0):
        """Recursively visits pages to gather text context."""
        if depth > self.max_depth or url in self.visited or len(self.visited) > 20:
            return
        
        self.visited.add(url)
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                text = self.clean_text(res.text)
                if len(text) > 100:  # Only save meaningful pages
                    self.corpus.append(f"SOURCE: {url}\nCONTENT: {text}")
                
                # Find next links
                soup = BeautifulSoup(res.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    link = urljoin(url, a['href']).split('#')[0]
                    if self.is_internal(link):
                        self.crawl(link, depth + 1)
        except Exception as e:
            print(f"Skipping {url}: {e}")

    def get_content(self) -> str:
        """Returns the combined text of all visited pages."""
        return "\n\n".join(self.corpus)