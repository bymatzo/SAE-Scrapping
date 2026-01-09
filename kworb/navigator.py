# kworb/navigator.py

class KworbNavigator:
    def __init__(self, scraper):
        self.scraper = scraper

    def clean_link(self, href: str) -> str:
        """Supprime les fragments (#...)"""
        return href.split("#")[0]

    def get_countries_from_spotify(self):
        """
        Récupère les noms et liens des pays depuis /spotify/
        """
        soup = self.scraper.get_page("/spotify")
        if soup is None:
            return []

        countries = []

        # On cherche tous les td de class 'mp text'
        for td in soup.find_all("td", class_="mp text"):
            a_tag = td.find("a", href=True)
            if a_tag:
                link = self.clean_link(a_tag["href"])
                name = a_tag.get_text(strip=True)
                countries.append({"name": name, "link": link})

        return countries


