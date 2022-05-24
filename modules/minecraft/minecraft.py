import requests
import datetime
import base64
import json

from pwnmap.module import Module
from pwnmap.util import UUIDUtil, PrintUtil


class pwnmapModule(Module):
    description = 'Get Minecraft account information by username/UUID'
    author = 'evan'
    date = '04-20-2022'

    def execute(self, username_uuid: str):
        if UUIDUtil.validate(username_uuid):
            uuid = UUIDUtil.remove_hyphen(username_uuid)
            username = self.__get_username_by_uuid(uuid)
        else:
            username = username_uuid

        res = requests.post(f'https://api.mojang.com/profiles/minecraft', json=[username])

        if len(res.json()) == 0:
            return []

        user_data = res.json()[0]

        username = user_data.get('name')
        uuid = user_data['id']
        migrated = not user_data.get('legacy', False)
        is_demo = user_data.get('demo', False)

        # * name history
        res = requests.get(f'https://api.mojang.com/user/profiles/{uuid}/names')

        name_history = []

        for name_info in res.json():
            name = name_info['name']

            changed_at_epoch = name_info.get('changedToAt')
            changed_at_date = datetime.datetime.utcfromtimestamp(changed_at_epoch / 1000).strftime('%Y-%m-%d, %H:%M:%S') if changed_at_epoch is not None else '?'

            name_history.append([name, changed_at_date])

        name_history[0][1] = 'first name'
        name_history.reverse()

        official_cape = self.__has_official_cape(uuid)
        optifine_cape = self.__has_optifine_cape(username)

        PrintUtil.pp({
            'Username'              : username,
            'UUID'                  : uuid,
            'Migrated'              : migrated,
            'Demo account'          : is_demo,
            'Optifine cape'         : optifine_cape,
            'Official cape'         : official_cape,
            'Name history'          : name_history
        })

    def __has_optifine_cape(self, username: str) -> bool:
        """ Check if Minecraft player has an Optifine cape """
        res = requests.get(f'http://s.optifine.net/capes/{username}.png')
        return res.status_code == 200

    def __has_official_cape(self, uuid: str) -> bool:
        """ Check if Minecraft player has an official cape """
        res = requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}')

        textures_b64 = res.json()['properties'][0]['value']
        textures = json.loads(base64.b64decode(textures_b64.encode()).decode())
    
        return bool(textures['textures'].get('CAPE'))

    def __get_username_by_uuid(self, uuid: str) -> str:
        """ Get username by UUID """
        res = requests.get(f'https://api.mojang.com/user/profiles/{uuid}/names')

        if len(res.json()) == 0:
            raise Exception('User not found')

        return res.json()[-1]['name']
