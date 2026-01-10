from kworb.scraper import KworbScraper
from kworb.navigator import KworbNavigator
from kworb.export import export_artists_csv, export_tracks_csv, export_country_tracks_csv

# 1 Initialisation du scraper et du navigateur
scraper = KworbScraper()
navigator = KworbNavigator(scraper)

# 2 Récupération des pays
countries = navigator.get_countries_from_spotify()

# 3 Affichage des premiers pays
print("Pays trouvés :")
for country in countries[:10]:
    print(f"{country['name']} : {country['daily_link']} + {country['weekly_link']}")

# 4 Nombre total de pays
print(f"\nTotal pays : {len(countries)}")

# 5 Récupération des artistes
artists = navigator.get_artists_from_spotify()

# 6 Affichage des 5 premiers artistes
for artist in artists[:5]:
    print(f"\n=== {artist.name} ===")
    print(f"Total streams : {artist.streams_total}")
    print(f"Streams daily : {artist.streams_daily}")
    print(f"Streams en tant que n°1 : {artist.streams_en_tant_que_numero_un}")
    print(f"Streams solo : {artist.streams_solo}")
    print(f"Streams featuring : {artist.streams_en_featuring}")

    print("\nTop tracks :")
    for i, track in enumerate(artist.tracks[:10], 1):
        print(f"{i}. {track.title} | Total: {track.streams_total} | Daily: {track.streams_daily}")

# 7 Top tracks pour les 3 premiers pays
for country in countries[:3]:
    print(f"\n=== {country['name']} ===")

    daily_link = country.get("daily_link")
    weekly_link = country.get("weekly_link")

    print(f"Daily link used: {daily_link}")
    print(f"Weekly link used: {weekly_link}")

    try:
        daily_tracks = navigator.get_top_tracks_for_country(daily_link, top_n=100, table_id="spotifydaily") if daily_link else []
    except Exception as e:
        print(f"Erreur scraping Daily: {e}")
        daily_tracks = []

    try:
        weekly_tracks = navigator.get_top_tracks_for_country(weekly_link, top_n=100, table_id="spotifyweekly") if weekly_link else []
    except Exception as e:
        print(f"Erreur scraping Weekly: {e}")
        weekly_tracks = []

    print("\n-- Daily Top 5 --")
    for track in daily_tracks[:5]:
        print(f"{track.position}. {track.artist} - {track.title} | Streams: {track.streams:,} | Total: {track.total:,}")

    print("\n-- Weekly Top 5 --")
    for track in weekly_tracks[:5]:
        print(f"{track.position}. {track.artist} - {track.title} | Streams: {track.streams:,} | Total: {track.total:,}")

# Après avoir récupéré les artistes depuis Spotify
artists = navigator.get_artists_from_spotify()

# On complète avec les points iTunes / plateformes
navigator.get_itunes_points(artists)

# Affichage exemple pour le 1er artiste
artist = artists[0]
print(f"\n=== {artist.name} ===")
print(f"Total streams: {artist.streams_total}")
print(f"Streams daily: {artist.streams_daily}")
print("Points par plateforme:")
for platform, points in artist.itunes_points.items():
    print(f"{platform}: {points}")






# Après avoir récupéré les artistes et leurs points iTunes
export_artists_csv(artists)
export_tracks_csv(artists)

# Pour les top tracks pays
countries_top_tracks = []
for country in countries:
    daily_tracks = navigator.get_top_tracks_for_country(country['daily_link'], top_n=100) if country['daily_link'] else []
    weekly_tracks = navigator.get_top_tracks_for_country(country['weekly_link'], top_n=100) if country['weekly_link'] else []

    countries_top_tracks.append({"country_name": country["name"], "type": "daily", "tracks": daily_tracks})
    countries_top_tracks.append({"country_name": country["name"], "type": "weekly", "tracks": weekly_tracks})

export_country_tracks_csv(countries_top_tracks)



