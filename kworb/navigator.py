# kworb/navigator.py

from kworb.models import Artist, Track


class KworbNavigator:
    def __init__(self, scraper):
        self.scraper = scraper

    def clean_link(self, href: str) -> str:
        """Supprime les fragments (#...)"""
        return href.split("#")[0]

    def parse_number(self, value: str) -> float:
        """
        Convertit '126,117.2' -> 126117.2
        Gère les valeurs vides
        """
        value = value.replace(",", "").strip()

        if value == "":
            return 0.0

        return float(value)
    
    def get_artists_from_spotify(self):
        soup = self.scraper.get_page("/spotify/artists.html")
        if soup is None:
            return []

        artists = []
        tbody = soup.find("tbody")
        if not tbody:
            return []

        for i, tr in enumerate(tbody.find_all("tr")):
            if i >= 200:  # limite à 200 artistes
                break

            tds = tr.find_all("td")
            if len(tds) < 6:
                continue

            a_tag = tds[0].find("a", href=True)
            if not a_tag:
                continue

            name = a_tag.get_text(strip=True)
            link = self.clean_link(a_tag["href"])

            # On scrape les tracks pour chaque artiste
            tracks = self.get_tracks_from_artist(link)

            artist = Artist(
                name=name,
                link=link,
                streams_total=self.parse_number(tds[1].get_text()),
                streams_daily=self.parse_number(tds[2].get_text()),
                streams_en_tant_que_numero_un=self.parse_number(tds[3].get_text()),
                streams_solo=self.parse_number(tds[4].get_text()),
                streams_en_featuring=self.parse_number(tds[5].get_text()),
                tracks=tracks
            )

            artists.append(artist)

        return artists



    def get_countries_from_spotify(self):
        """ Récupère les noms et liens Daily & Weekly des pays depuis /spotify/ """
        soup = self.scraper.get_page("/spotify")
        if soup is None:
            return []

        countries = []

        for tr in soup.find_all("tr"):
            tds = tr.find_all("td", class_="mp text")
            if len(tds) < 2:
                continue

            country_name = tds[0].get_text(strip=True)

            links = tds[1].find_all("a", href=True)
            daily_link = None
            weekly_link = None

            for a in links:
                href = self.clean_link(a["href"])

                if "_daily.html" in href:
                    daily_link = href
                elif "_weekly.html" in href:
                    weekly_link = href

            if daily_link or weekly_link:
                countries.append({
                    "name": country_name,
                    "daily_link": daily_link,
                    "weekly_link": weekly_link
                })

        return countries

    def get_tracks_from_artist(self, artist_url: str):
        """Récupère les titres et leurs streams d'une page artiste"""
        soup = self.scraper.get_page(artist_url)
        if soup is None:
            return []

        tracks = []

        # Trouve la table des tracks par sa classe
        table = soup.find("table", class_="addpos sortable")
        if not table:
            return []  # si table non trouvée, on retourne liste vide

        tbody = table.find("tbody")
        if not tbody:
            return []

        for i, tr in enumerate(tbody.find_all("tr")):
            if i >= 100:  # limite à 100 tracks
                break

            tds = tr.find_all("td")
            if len(tds) < 3:
                continue

            a_tag = tds[0].find("a", href=True)
            if not a_tag:
                continue

            title = a_tag.get_text(strip=True).replace("*", "").strip()
            link = a_tag["href"]

            streams_total = self.parse_number(tds[1].get_text())
            streams_daily = self.parse_number(tds[2].get_text())

            track = Track(title=title, link=link, streams_total=streams_total, streams_daily=streams_daily)
            tracks.append(track)

        return tracks




