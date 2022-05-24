import requests
import json
import pwnmap

from pwnmap.module import Module
from pwnmap.logger import Logger
from pwnmap.util import BoxUtil


class pwnmapModule(Module):
    description = 'Grab all connections a user may have and search for databreaches.'
    author = 'evan'
    date = '04-10-2022'

    def execute(self, userID: str):
        results  = []

        endpoint = f'https://discord.com/api/v9/users/{userID}/profile'

        formated = requests.get(url=endpoint, headers={'authorization': json.load(open('config.json'))['discord_token']}).json()

        apiKey   = pwnmap.__app__.config.APIKeys.weleakinfo

        username = formated['user']['username']+'#'+formated['user']['discriminator']
        accounts = formated['connected_accounts']


        Logger.info(f'Searching for {len(accounts)} accounts\'s')

        for account in accounts:
            try:
                r = requests.get(f'https://api.weleakinfo.to/api?value={account["name"]}&type=email&key={apiKey}').json()
                
                if not r['result']:
                    return

                for x in r['result']:
                    sources = x["sources"]
                    if len(sources) > 0:
                        sources = ', '.join(sources)
                    else:
                        sources = 'Unknown Source'
                    results.append([x['line'], sources])
                    
            except Exception as e:
                pass


        BoxUtil.boxify(
            [
                {'Login': x, 'Database': db}
                for x, db in results
            ],
            title='Lookup results',
            show_keys=True
        )