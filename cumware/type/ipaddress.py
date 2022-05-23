import socket
import ipaddress


class IPv4Address(str):
    """ IPAddress type string object """

    def __init__(self, ip):
        try:
            ipaddress.ip_address(ip)
        except Exception:
            try:
                socket.gethostbyname(ip)
            except Exception:
                raise ValueError('Invalid IP-address')
