import pwnmap

from pwnmap.command import Command
from pwnmap.util import BoxUtil


class ModulesCommand(Command):
    name = 'modules'
    description = 'Show modules'
    aliases = 'mods',

    @Command.execute
    def run(self):
        BoxUtil.boxify(
            [
                {
                    '#': 1 + i,
                    'Name': mod.name,
                    'Date': mod.instance.date,
                    'Author': mod.instance.author,
                    'Description': mod.instance.description
                }
                for i, mod in enumerate(pwnmap.__app__.modules.get_registered_modules())
            ],
            title='Modules',
            show_keys=True,
            thicc_border=False
        )
