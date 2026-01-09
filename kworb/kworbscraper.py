import requests
from bs4 import BeautifulSoup

class KworbScraper:
    def __init__(self, base_url: str = "https://kworb.net"):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def get_page(self, path: str = "/") -> BeautifulSoup:
        """
        Récupère une page à partir d'un chemin relatif Kworb
        """
        url = self.base_url + path
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Erreur HTTP {response.status_code} : {url}")

        return BeautifulSoup(response.text, "html.parser")
