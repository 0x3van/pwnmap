from cumware.command import Command
from cumware.util import PrintUtil, GeoIP
from cumware.type import IPv4Address


class IPLookupCommand(Command):
    name = 'iplookup'
    description = 'Lookup IP-address'
    aliases = 'ipl',

    @Command.execute
    def run(self, ip: IPv4Address):
        geoip_data = GeoIP.lookup(ip)

        PrintUtil.pp({
            'Hostname'                  : geoip_data.hostname,
            'City'                      : geoip_data.city,
            'Region'                    : geoip_data.region,
            'Country'                   : geoip_data.country,
            'Internet service provider' : geoip_data.org
        })
