import socket
import re

from typing import Union

from pwnmap.module import Module
from pwnmap.util import PrintUtil
from pwnmap.type import domain


class pwnmapModule(Module):
    description = 'lookup name and address by domain name'
    author = 'evan'
    date = '25-04-2022'

    def execute(self, domain: domain):
        server = self.__get_root_server(domain)

        if server is None:
            raise Exception('Root WHOIS server not found')

        answer = self.__whois_request(f'--charset=utf-8 --show-handles {domain}', server)
        json_data = self.__whois_parse(answer)

        name = json_data.get('name')
        phone = json_data.get('phone')

        street = json_data.get('address')
        city = json_data.get('city')
        postal_code = json_data.get('postalcode')
        country = json_data.get('country')

        address = None
        
        if all((street, city, postal_code, country)):
            address = f'{street}, {city} {postal_code}, {country}' # :troll:

        if any((name, address, phone)):
            PrintUtil.pp({
                'Name'      :  name,
                'Address'   : address,
                'Phone'     : phone
            })

    def __get_root_server(self, domain: str) -> Union[str, None]:
        EXCEPTIONS = {
            '.ac.uk'        : 'whois.ja.net',
            '.ps'           : 'whois.pnina.ps',
            '.buzz'         : 'whois.nic.buzz',
            '.moe'          : 'whois.nic.moe',
            'example.com'   : 'whois.verisign-grs.com'
        }

        for ex_tld, ex_root in EXCEPTIONS.items():
            if domain.endswith(ex_tld):
                return ex_root

        answer = self.__whois_request(domain, 'whois.iana.org')

        for line in (x.strip() for x in answer.splitlines()):
            match = re.match(r'refer:\s*([^\s]+)', line)

            if match:
                return match.group(1)

        return None

    def __whois_request(self, query: str, server: str, port: int = 43) -> str:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((server, port))
        sock.send((query + '\r\n').encode())

        buf = b''

        while True:
            data = sock.recv(1024)

            if not data:
                break

            buf += data

        return buf.decode()

    def __whois_parse(self, raw_answer: str) -> dict[str: str]:
        json_answer = {}

        for line in (x.strip() for x in raw_answer.splitlines() if not x.startswith('#') and x.strip()):
            if ':' in line:
                key, value = line.split(':', 1)

                json_answer |= {key.lower(): value.lstrip(' ')}

        return json_answer
