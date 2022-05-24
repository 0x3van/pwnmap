import sys

from pwnmap.command import Command


class ExitCommand(Command):
    name = 'exit'
    description = 'Exit pwnmap OSINT Framework. fuck you for leaving me.'
    aliases = 'q', 'quit'

    @Command.execute
    def run(self):
        sys.exit(0)
