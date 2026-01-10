class Track:
    def __init__(self, title: str, link: str, streams_total: float, streams_daily: float):
        self.title = title
        self.link = link
        self.streams_total = streams_total
        self.streams_daily = streams_daily

class Artist:
    def __init__(
        self, 
        name: str,
        link: str,
        streams_total: float = 0,
        streams_daily: float = 0,
        streams_en_tant_que_numero_un: float = 0,
        streams_solo: float = 0,
        streams_en_featuring: float = 0,
        tracks: list = None,
        itunes_points: dict = None  # <-- ajout pour plateformes
    ):
        self.name = name
        self.link = link
        self.streams_total = streams_total
        self.streams_daily = streams_daily
        self.streams_en_tant_que_numero_un = streams_en_tant_que_numero_un
        self.streams_solo = streams_solo
        self.streams_en_featuring = streams_en_featuring
        self.tracks = tracks if tracks else []

        # Dictionnaire pour les points par plateforme
        self.itunes_points = itunes_points if itunes_points else {
            "Apple Music": 0,
            "Spotify": 0,
            "iTunes": 0,
            "YouTube": 0,
            "Shazam": 0,
            "Deezer": 0,
            "Top Country": "",
            "Total Points": 0
        }

class CountryTrack:
    def __init__(self, position: int, artist: str, title: str, streams: float, streams_change: float = 0.0, total: float = 0.0):
        self.position = position
        self.artist = artist
        self.title = title
        self.streams = streams          # streams du jour/semaine
        self.streams_change = streams_change  # + ou - par rapport au précédent
        self.total = total              # total cumulé


