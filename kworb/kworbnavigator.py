class KworbNavigator:
    def __init__(self, scraper):
        self.scraper = scraper

    def get_links(self, path: str):
        """
        Récupère tous les liens internes Kworb depuis une page
        """
        soup = self.scraper.get_page(path)

        links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]

            # on garde uniquement les liens internes
            if href.startswith("/") and not href.startswith("//"):
                links.add(href)

        return sorted(links)

    def filter_links(self, links, keyword: str):
        """
        Filtre les liens contenant un mot-clé
        """
        return [link for link in links if keyword in link]
