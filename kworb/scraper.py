import requests
from bs4 import BeautifulSoup

class KworbScraper:
    def __init__(self, base_url: str = "https://kworb.net"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml"
        })

    def get_page(self, path: str = "/") -> BeautifulSoup:
        # Si path est déjà une URL absolue, on l'utilise telle quelle
        if path.startswith("http://") or path.startswith("https://"):
            url = path
        else:
            url = self.base_url.rstrip("/") + "/" + path.lstrip("/")

        response = self.session.get(url)
        if response.status_code != 200:
            raise Exception(f"Erreur HTTP {response.status_code} : {url}")

        return BeautifulSoup(response.text, "html.parser")


