import requests
import time
import random
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class KworbScraper:
    def __init__(self, base_url: str = "https://kworb.net"):
        self.base_url = base_url

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml"
        })

        retries = Retry(
            total=5,
            backoff_factor=1.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get_page(self, path: str = "/") -> BeautifulSoup:
        if path.startswith("http://") or path.startswith("https://"):
            url = path
        else:
            url = self.base_url.rstrip("/") + "/" + path.lstrip("/")

        try:
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erreur requête : {url}")
            print(e)
            return None

        if response.text.strip() == "":
            print("⚠️ Page vide – possible blocage")

        return BeautifulSoup(response.text, "html.parser")

        



