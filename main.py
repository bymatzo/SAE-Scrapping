# main.py

from kworb.scraper import KworbScraper
from kworb.navigator import KworbNavigator

scraper = KworbScraper()
navigator = KworbNavigator(scraper)

# 1) Page d'accueil
home_links = navigator.get_links("/")

# 2) Aller vers Spotify
spotify_links = navigator.filter_links(home_links, "spotify")

print("Liens Spotify :")
for link in spotify_links:
    print(link)

# 3) Explorer les pays
country_links = navigator.get_links("/spotify/country/")

print("\nPays disponibles :")
for link in country_links[:10]:
    print(link)






