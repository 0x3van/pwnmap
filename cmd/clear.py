from cumware.command import Command
from cumware.util import ConsoleUtil


class ClearCommand(Command):
    name = 'clear'
    description = 'Clear screen'
    aliases = 'cls',

    @Command.execute
    def run(self):
        ConsoleUtil.clear_screen()
        ConsoleUtil.print_banner()
        return True
