import pwnmap

from pwnmap.command import Command
from pwnmap.util import BoxUtil


class SearchCommand(Command):
    name = 'search'
    description = 'Search for module'

    @Command.execute
    def run(self, keywords: str):
        keywords = keywords.lower()

        mods = []

        for i, mod in enumerate(pwnmap.__app__.modules.get_registered_modules()):
            check = any([
                all([x in mod.name.lower() for x in keywords.split(' ')]),
                all([x in  mod.instance.description.lower() for x in keywords.split(' ')])
            ])

            if check is True:
                mods.append((i + 1, mod))

        BoxUtil.boxify(
            [
                {
                    '#': index,
                    'Name': mod.name,
                    'Date': mod.instance.date,
                    'Author': mod.instance.author,
                    'Description': mod.instance.description
                }
                for index, mod in mods
            ],
            title='Modules',
            show_keys=True,
            thicc_border=False
        )
