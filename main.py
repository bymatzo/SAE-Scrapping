from kworb.scraper import KworbScraper
from kworb.navigator import KworbNavigator

# 1 Initialisation du scraper et du navigateur
scraper = KworbScraper()
navigator = KworbNavigator(scraper)

# 2 Récupération des pays depuis la page /spotify/
countries = navigator.get_countries_from_spotify()

# 3 Affichage des premiers pays
print("Pays trouvés :")
for country in countries[:10]:
    print(f"{country['name']} : {country['daily_link']} + {country['weekly_link']}")

# 4 Nombre total de pays trouvés
print(f"\nTotal pays : {len(countries)}")

# 5 Récupération des artistes
artists = navigator.get_artists_from_spotify()

# Affichage des 5 premiers artistes avec leurs infos et leurs 100 premiers titres
for artist in artists[:5]:
    print(f"\n=== {artist.name} ===")
    print(f"Total streams : {artist.streams_total}")
    print(f"Streams daily : {artist.streams_daily}")
    print(f"Streams en tant que n°1 : {artist.streams_en_tant_que_numero_un}")
    print(f"Streams solo : {artist.streams_solo}")
    print(f"Streams featuring : {artist.streams_en_featuring}")
    
    print("\nTop tracks :")
    for i, track in enumerate(artist.tracks[:100], 1):  # limite à 100 tracks par artiste
        print(f"{i}. {track.title} | Total: {track.streams_total} | Daily: {track.streams_daily}")











