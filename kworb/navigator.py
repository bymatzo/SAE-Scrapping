# kworb/navigator.py
import time
import random
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
    
    def parse_artist_streams(self, value: str) -> int:
        """
        Kworb - table ARTISTS uniquement
        Toutes les valeurs sont en MILLIONS
        """
        if value is None or value == "":
            return 0

        value = str(value).strip()
        value = value.replace(" ", "").replace("\u202f", "").replace("\xa0", "")

        try:
            numeric = float(value.replace(",", ""))
            return int(numeric * 1_000_000)
        except ValueError:
            return 0


    
    def get_artists_from_spotify(self):
        soup = self.scraper.get_page("/spotify/artists.html")
        if soup is None:
            return []

        artists = []
        tbody = soup.find("tbody")
        if not tbody:
            return []

        for i, tr in enumerate(tbody.find_all("tr")):
            if i >= 50:  # limite à 50 artistes
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
                streams_total=self.parse_artist_streams(tds[1].get_text()),
                streams_daily=self.parse_artist_streams(tds[2].get_text()),
                streams_en_tant_que_numero_un=self.parse_artist_streams(tds[3].get_text()),
                streams_solo=self.parse_artist_streams(tds[4].get_text()),
                streams_en_featuring=self.parse_artist_streams(tds[5].get_text()),

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
            if i >= 30:  # limite à 35 pays
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
        """
        Récupère les titres et leurs streams depuis une page artiste Kworb
        - Limite à 30 tracks
        - Temporisation anti-scraping
        - Gestion des erreurs réseau
        """

        try:
            soup = self.scraper.get_page(artist_url)
        except Exception as e:
            print(f"[SKIP ARTIST] {artist_url} → {e}")
            return []

        if soup is None:
            return []

        tracks = []

        # Table des tracks
        table = soup.find("table", class_="addpos sortable")
        if not table:
            print(f"[NO TABLE] {artist_url}")
            return []

        tbody = table.find("tbody")
        if not tbody:
            return []

        for i, tr in enumerate(tbody.find_all("tr")):
            if i >= 30:
                break

            tds = tr.find_all("td")
            if len(tds) < 3:
                continue

            a_tag = tds[0].find("a", href=True)
            if not a_tag:
                continue

            title = a_tag.get_text(strip=True).replace("*", "").strip()
            link = a_tag["href"].strip()

            try:
                streams_total = self.parse_number(tds[1].get_text())
                streams_daily = self.parse_number(tds[2].get_text())
            except Exception:
                streams_total = 0
                streams_daily = 0

            track = Track(
                title=title,
                link=link,
                streams_total=streams_total,
                streams_daily=streams_daily
            )

            tracks.append(track)

        return tracks

    
    def get_top_tracks_for_country(self, url: str, top_n: int = 100, table_id: str = "spotifydaily"):
        """
        Récupère les top tracks Spotify Daily ou Weekly (Kworb)
        """
        tracks = []

        if not url:
            return tracks

        try:
            soup = self.scraper.get_page(url)
        except Exception as e:
            print(f"⚠️ Erreur requête : {url}")
            print(e)
            return tracks

        if soup is None:
            return tracks

        # ✅ Daily → table avec ID
        if table_id == "spotifydaily":
            table = soup.find("table", id="spotifydaily")

        # ✅ Weekly → table sans ID (classe seulement)
        else:
            table = soup.find("table", class_="sortable")

        if not table:
            print(f"[NO TABLE] {url}")
            return tracks

        tbody = table.find("tbody")
        if not tbody:
            return tracks

        for i, tr in enumerate(tbody.find_all("tr")):
            if i >= top_n:
                break

            tds = tr.find_all("td")
            if len(tds) < 7:
                continue

            # Artiste + titre
            artist_title_div = tds[2].find("div")
            if not artist_title_div:
                continue

            links = artist_title_div.find_all("a")
            artist_name = links[0].get_text(strip=True) if len(links) >= 1 else ""
            track_title = links[1].get_text(strip=True) if len(links) >= 2 else ""

            try:
                streams = self.parse_number(tds[6].get_text())
                streams_change = self.parse_number(tds[7].get_text()) if len(tds) > 7 else 0
                total = self.parse_number(tds[-1].get_text())
            except Exception:
                streams = streams_change = total = 0

            track = CountryTrack(
                position=i + 1,
                artist=artist_name,
                title=track_title,
                streams=streams,
                streams_change=streams_change,
                total=total
            )

            tracks.append(track)

        return tracks



    
    def get_itunes_points(self, artists: list):
        """
        Récupère les points par plateforme depuis https://kworb.net/itunes/
        et les associe aux objets Artist existants.
        """
        url = "https://kworb.net/itunes/"
        soup = self.scraper.get_page(url)
        if soup is None:
            return

        tbody = soup.find("tbody")
        if not tbody:
            return

        for tr in tbody.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) < 12:
                continue

            a_tag = tds[2].find("a", href=True)
            if not a_tag:
                continue

            artist_name = a_tag.get_text(strip=True)

            # On récupère les points par plateforme
            itunes_points = {
                "Total Points": int(tds[3].get_text(strip=True).replace(",", "")),
                "Apple Music": int(tds[4].get_text(strip=True).replace(",", "")),
                "Spotify": int(tds[5].get_text(strip=True).replace(",", "")),
                "iTunes": int(tds[6].get_text(strip=True).replace(",", "")),
                "YouTube": int(tds[7].get_text(strip=True).replace(",", "")),
                "Shazam": int(tds[8].get_text(strip=True).replace(",", "")),
                "Deezer": int(tds[9].get_text(strip=True).replace(",", "")),
                "Top Country": tds[10].get_text(strip=True)
            }

            # On associe les points à l'artiste correspondant
            for artist in artists:
                if artist.name.lower() == artist_name.lower():
                    artist.itunes_points = itunes_points
                    break






