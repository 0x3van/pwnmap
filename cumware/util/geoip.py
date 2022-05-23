import requests


class GeoIP:

    API_URL = 'http://ipinfo.io/%(ip)s'

    def __init__(self, json_data: dict):
        for k, v in json_data.items():
            setattr(self, k, v)

    @classmethod
    def lookup(cls, ip_address: str) -> "GeoIP":
        res = requests.get(cls.API_URL % {'ip': ip_address})
        return cls(res.json())

    def __getattr__(self, name: str) -> object:
        return getattr(self, name) if hasattr(self, name) is True else 'FAILED'

