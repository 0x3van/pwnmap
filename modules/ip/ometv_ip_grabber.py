import ipaddress
import datetime
import kamene.all as kamene

from cumware.module import Module
from cumware.util import GeoIP

# truly amazing code 
class cumwareModule(Module):
    description = 'Grab IP-addresses on Ome.TV'
    author = 'evan'
    date = '05-01-2022'

    def execute(self, network_interface: str):
        self.__cached_user_ids = []

        print(f'\n{"IP-address":<15} {"Port":<5} {"User ID":<9} {"Time":<8} Location')
        print(f'{"----------":<15} {"----":<5} {"-------":<9} {"----":<8} --------')
        
        kamene.sniff(iface=network_interface, store=False, prn=self.__packet_handler)

    def __packet_handler(self, pkt):
        STUN_BINDING_REQUEST_PACKET_HEADER = b'\x00\x01\x00\x4c\x21\x12\xa4\x42'

        if kamene.UDP in pkt and kamene.Raw in pkt:
            ip_version = kamene.IPv6 if kamene.IPv6 in pkt else kamene.IP

            target_ip = pkt[ip_version].dst

            pkt_data = pkt[kamene.Raw].load

            if pkt_data[:8] == STUN_BINDING_REQUEST_PACKET_HEADER and not ipaddress.ip_address(target_ip).is_private:
                user_id_offset = pkt_data.find(b':')
                user_id = (pkt_data[user_id_offset - 4:user_id_offset] + b':' + pkt_data[user_id_offset:user_id_offset + 4]).decode()

                if not user_id in self.__cached_user_ids:
                    self.__cached_user_ids.append(user_id)

                    geoip_data = GeoIP.lookup(target_ip)
        
                    dport = pkt[ip_version].dport

                    now = datetime.datetime.now()
                    time = now.strftime('%H:%M:%S')


                    print(f'{target_ip:<15} {dport:<5} {user_id:<9} {time:8} {geoip_data.country}, {geoip_data.city}')
