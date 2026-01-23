# SAE Scrapping – Analyse des données Spotify (Kworb)

## Description du projet

Ce projet a pour objectif de **collecter, traiter et analyser des données Spotify** issues du site **Kworb** à l’aide de techniques de **web scraping** et de **traitement de données en Python**.

Les données récupérées (streams, classements, pays, type daily/weekly, artistes, titres…) sont :

* nettoyées et structurées,
* exportées au format CSV pour une utilisation dans Power BI,
* analysées via une interface graphique **PowerBI** permettant :

  * de filtrer par pays,
  * de choisir le type de classement (daily / weekly),
  * de sélectionner une métrique,
  * de visualiser des graphiques,

---

## Étapes pour reproduire le projet

1. Récupérer le dossier "Dossier final" envoyer par mail et bien le copier dans C:/ pour l'utilisation du PowerBI.

2. Installer les dépendances Python (voir section librairies).

3. Lancer le script principal :

  Ouvrir le dossier "code" dans un IDE.

  Lancer le fichier "main.py".

5. Une fois toutes les données charger 3 fichiers csv sont créer dans le dossier code sous le nom : export_csv.

---

## Librairies utilisées

* **Python 3.8+**
* `pandas` → manipulation et analyse des données
* `requests` → récupération des pages web
* `beautifulsoup4` → parsing HTML (scraping)
* `os` → gestion des chemins de fichiers
* `csv` → création et modifications de fichiers csv


Installation des librairies nécessaires :

```bash
pip install requests 
pip install beautifulsoup4 
```

---

## Instructions d’exécution

1. Vérifier que Python est bien installé :

   ```bash
   python --version
   ```

2. Lancer le programme principal depuis un ide :

   ```bash
   python main.py
   ```
3. Récupérer les données :

  Une fois le code bien executer, un dossier "export_csv" sera disponible dans le meme repertoire de que le dossier du projet avec toutes les données récupérées.

4. Fonctionnalités disponibles dans le rendu PowerBI :

   * Sélection du pays
   * Choix du type (Daily / Weekly)
   * Choix de la métrique (streams / total)
   * Sélection du Top N
   * Visualisation graphique (bar chart)
   * Export CSV pour Power BI

---

Si les données PowerBI ne s'affiche pas, veuillez vous référez à la vidéo expliquant comment bien importer les données dans le PowerBi.

## Répartition des responsabilités

* **Analyse & Extraction** : Étudiant 1
* **Traitement & Export** : Étudiant 2
* **Visualisation & Interprétation** : Étudiant 3

### Détail par étudiant

* **Mateo** – *Visualisation & Interprétation*

  * Développement de l’interface PowerBI
  * Analyse et interprétation des données
  * Création des visualisations graphiques
  * Gestion des erreurs et fiabilisation du code

* **Wissem** – *Analyse & Extraction*

  * Web scraping des données Spotify via Kworb
  * Analyse de la structure des pages web
  * Structuration initiale des données brutes

* **Simon** – *Traitement & Export*

  * Nettoyage et transformation des données
  * Export des données en CSV pour Power BI
  * Organisation de l’architecture du projet
  * Tests, validation des résultats
  * Documentation et aide à la rédaction du rapport

---

## Objectifs pédagogiques

* Mise en œuvre du web scraping
* Manipulation de données avec pandas
* Création d’un rendu graphique
* Rendre des données pertinentes et parlantes 
* Structuration d’un projet Python
* Travail














