# export.py
import csv
import os

EXPORT_DIR = "exports_csv"

# Crée le dossier s'il n'existe pas
os.makedirs(EXPORT_DIR, exist_ok=True)


def export_artists_csv(artists, filename="artists.csv"):
    """
    Exporte les artistes avec leurs infos et points iTunes/plateformes
    """
    filepath = os.path.join(EXPORT_DIR, filename)
    headers = [
        "name", "link", "streams_total", "streams_daily",
        "streams_en_tant_que_numero_un", "streams_solo", "streams_en_featuring",
        "Total Points", "Apple Music", "Spotify", "iTunes", "YouTube", "Shazam", "Deezer", "Top Country"
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for artist in artists:
            row = {
                "name": artist.name,
                "link": artist.link,
                "streams_total": artist.streams_total,
                "streams_daily": artist.streams_daily,
                "streams_en_tant_que_numero_un": artist.streams_en_tant_que_numero_un,
                "streams_solo": artist.streams_solo,
                "streams_en_featuring": artist.streams_en_featuring,
            }
            # Ajouter les points iTunes si disponibles
            if hasattr(artist, "itunes_points") and artist.itunes_points:
                row.update({
                    "Total Points": artist.itunes_points.get("Total Points", 0),
                    "Apple Music": artist.itunes_points.get("Apple Music", 0),
                    "Spotify": artist.itunes_points.get("Spotify", 0),
                    "iTunes": artist.itunes_points.get("iTunes", 0),
                    "YouTube": artist.itunes_points.get("YouTube", 0),
                    "Shazam": artist.itunes_points.get("Shazam", 0),
                    "Deezer": artist.itunes_points.get("Deezer", 0),
                    "Top Country": artist.itunes_points.get("Top Country", "")
                })
            else:
                row.update({
                    "Total Points": 0,
                    "Apple Music": 0,
                    "Spotify": 0,
                    "iTunes": 0,
                    "YouTube": 0,
                    "Shazam": 0,
                    "Deezer": 0,
                    "Top Country": ""
                })
            writer.writerow(row)


def export_tracks_csv(artists, filename="tracks.csv"):
    """
    Exporte toutes les tracks des artistes, lien via artist_name
    """
    filepath = os.path.join(EXPORT_DIR, filename)
    headers = ["artist_name", "title", "link", "streams_total", "streams_daily"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for artist in artists:
            for track in artist.tracks:
                writer.writerow({
                    "artist_name": artist.name,
                    "title": track.title,
                    "link": track.link,
                    "streams_total": track.streams_total,
                    "streams_daily": track.streams_daily
                })


def export_country_tracks_csv(countries_top_tracks, filename="country_tracks.csv"):
    """
    countries_top_tracks = [
        {"country_name": "Global", "type": "daily", "tracks": [CountryTrack,...]},
        ...
    ]
    """
    filepath = os.path.join(EXPORT_DIR, filename)
    headers = ["country_name", "type", "position", "artist", "title", "streams", "streams_change", "total"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for entry in countries_top_tracks:
            country_name = entry["country_name"]
            type_ = entry["type"]  # daily ou weekly
            tracks = entry["tracks"]
            for track in tracks:
                writer.writerow({
                    "country_name": country_name,
                    "type": type_,
                    "position": track.position,
                    "artist": track.artist,
                    "title": track.title,
                    "streams": track.streams,
                    "streams_change": track.streams_change,
                    "total": track.total
                })
