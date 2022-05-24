from pwnmap.command import Command
from pwnmap.util import BoxUtil
from pwnmap.logger import Logger


class HelpCommand(Command):
    name = 'help'
    description = 'Show list of available commands'
    aliases = '?',

    @Command.execute
    def run(self):
        BoxUtil.boxify(
            [
                {
                    'Name': cmd.name,
                    'Description': cmd.description
                }
                for cmd in self.shell.command_manager.get_registered_commands()
            ],
            title='Commands',
            show_keys=True
        )

        Logger.nl()
        Logger.info('Use prefix \'!\' to run OS shell commands.')
