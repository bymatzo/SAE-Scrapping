from kworb.scraper import KworbScraper
from kworb.navigator import KworbNavigator

# 1️⃣ Initialisation du scraper et du navigateur
scraper = KworbScraper()
navigator = KworbNavigator(scraper)

# 2️⃣ Récupération des pays depuis la page /spotify/
countries = navigator.get_countries_from_spotify()

# 3️⃣ Affichage des premiers pays
print("Pays trouvés :")
for country in countries[:10]:
    print(f"{country['name']} -> {country['link']}")

# 4️⃣ Nombre total de pays trouvés
print(f"\nTotal pays : {len(countries)}")









