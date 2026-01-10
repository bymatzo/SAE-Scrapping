class Track:
    def __init__(self, title: str, link: str, streams_total: float, streams_daily: float):
        self.title = title
        self.link = link
        self.streams_total = streams_total
        self.streams_daily = streams_daily

class Artist:
    def __init__(self, name: str, link: str, streams_total: float, streams_daily: float,
                 streams_en_tant_que_numero_un: float, streams_solo: float, streams_en_featuring: float,
                 tracks=None):
        self.name = name
        self.link = link
        self.streams_total = streams_total
        self.streams_daily = streams_daily
        self.streams_en_tant_que_numero_un = streams_en_tant_que_numero_un
        self.streams_solo = streams_solo
        self.streams_en_featuring = streams_en_featuring
        self.tracks = tracks or []  # liste de Track

class CountryTrack:
    def __init__(self, position: int, artist: str, title: str, streams: float, streams_change: float = 0.0, total: float = 0.0):
        self.position = position
        self.artist = artist
        self.title = title
        self.streams = streams          # streams du jour/semaine
        self.streams_change = streams_change  # + ou - par rapport au précédent
        self.total = total              # total cumulé


