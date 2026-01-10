# kworb/navigator.py

from kworb.models import Artist, Track, CountryTrack


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
        """Récupère les noms et liens Daily & Weekly des pays depuis /spotify/ avec URLs absolues"""
        soup = self.scraper.get_page("/spotify")
        if soup is None:
            return []

        base_url = "https://kworb.net/spotify/"
        countries = []

        for i, tr in enumerate(soup.find_all("tr")):
            if i >= 50:  # limite à 50 pays
                break

            tds = tr.find_all("td", class_="mp text")
            if len(tds) < 2:
                continue

            country_name = tds[0].get_text(strip=True)

            links = tds[1].find_all("a", href=True)
            daily_link = None
            weekly_link = None

            for a in links:
                href = self.clean_link(a["href"]).strip()

                # Si c'est déjà un lien absolu, on garde, sinon on complète avec base_url
                if href.startswith("http://") or href.startswith("https://"):
                    full_href = href
                else:
                    full_href = base_url + href.lstrip("/")

                if "_daily.html" in href:
                    daily_link = full_href
                elif "_weekly.html" in href:
                    weekly_link = full_href

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
    
    def get_top_tracks_for_country(self, url: str, top_n: int = 100, table_id: str = "spotifydaily"):
        """
        Récupère les top tracks pour un pays sur la page Daily ou Weekly
        - table_id: 'spotifydaily' ou 'spotifyweekly'
        """
        soup = self.scraper.get_page(url)
        if soup is None:
            return []

        table = soup.find("table", id=table_id)
        if not table:
            return []

        tbody = table.find("tbody")
        if not tbody:
            return []

        tracks = []
        for i, tr in enumerate(tbody.find_all("tr")):
            if i >= top_n:
                break

            tds = tr.find_all("td")
            if len(tds) < 7:  # minimum requis pour daily/weekly
                continue

            # Récupération de l'artiste et titre
            artist_title_div = tds[2].find("div")
            if not artist_title_div:
                continue

            # On prend le texte et on essaie de séparer artiste et titre
            links = artist_title_div.find_all("a")
            if len(links) >= 2:
                artist_name = links[0].get_text(strip=True)
                track_title = links[1].get_text(strip=True)
            else:
                artist_name = ""
                track_title = artist_title_div.get_text(strip=True)

            # Streams principaux et total
            streams = self.parse_number(tds[6].get_text())
            streams_change = self.parse_number(tds[7].get_text()) if len(tds) > 7 else 0.0
            total = self.parse_number(tds[-1].get_text()) if len(tds) >= 11 else streams

            track = CountryTrack(
                position=i+1,
                artist=artist_name,
                title=track_title,
                streams=streams,
                streams_change=streams_change,
                total=total
            )
            tracks.append(track)

        return tracks





