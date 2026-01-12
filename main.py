import time
import random

from kworb.scraper import KworbScraper
from kworb.navigator import KworbNavigator
from kworb.export import (
    export_artists_csv,
    export_tracks_csv,
    export_country_tracks_csv
)

# =========================================
# 1️⃣ Initialisation
# =========================================
scraper = KworbScraper()
navigator = KworbNavigator(scraper)

# =========================================
# 2️⃣ Récupération des pays Spotify
# =========================================
countries = navigator.get_countries_from_spotify()
print(f"✅ {len(countries)} pays récupérés")

# =========================================
# 3️⃣ Récupération des artistes Spotify
# =========================================
artists = navigator.get_artists_from_spotify()
print(f"✅ {len(artists)} artistes récupérés")

# =========================================
# 4️⃣ Récupération des points iTunes / plateformes
# =========================================
navigator.get_itunes_points(artists)
print("✅ Points plateformes récupérés")

# =========================================
# 5️⃣ Export artistes & tracks artistes
# =========================================
export_artists_csv(artists)
export_tracks_csv(artists)
print("✅ Exports artists.csv et tracks.csv terminés")

# =========================================
# 6️⃣ Top tracks par pays (Daily & Weekly)
# =========================================
countries_top_tracks = []

for country in countries:
    country_name = country["name"]
    daily_link = country.get("daily_link")
    weekly_link = country.get("weekly_link")

    print(f"🌍 Scraping {country_name}")

    # ⏳ Pause anti-scraping (IMPORTANT)
    time.sleep(random.uniform(2.5, 4.5))

    daily_tracks = navigator.get_top_tracks_for_country(
        daily_link,
        top_n=100,
        table_id="spotifydaily"
    ) if daily_link else []

    weekly_tracks = navigator.get_top_tracks_for_country(
        weekly_link,
        top_n=100,
        table_id="spotifyweekly"
    ) if weekly_link else []

    countries_top_tracks.append({
        "country_name": country_name,
        "type": "daily",
        "tracks": daily_tracks
    })

    countries_top_tracks.append({
        "country_name": country_name,
        "type": "weekly",
        "tracks": weekly_tracks
    })

# =========================================
# 7️⃣ Export top tracks pays
# =========================================
export_country_tracks_csv(countries_top_tracks)
print("✅ Export country_tracks.csv terminé")

print("\n🎉 SCRAPING TERMINÉ AVEC SUCCÈS")


if __name__ == "__main__":
    launch_tkinter_dashboard()



