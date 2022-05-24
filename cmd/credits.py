from pwnmap.command import Command

import pwnmap


class CreditsCommand(Command):
    name = 'credits'
    description = 'Show pwnmap OSINT Framework credits'
    aliases = 'credit', 'info', 'about'

    @Command.execute
    def run(self):
        print(rf'''
 ___ ____  ___ ____  
|_ _|  _ \|_ _/ ___| 
 | || |_) || |\___ \ 
 | ||  _ < | | ___) |
|___|_| \_\___|____/ 
                      

pwnmap version {pwnmap.__version__}: an open-source intelligence framework 

Developed by {pwnmap.__author__}

GitHub:
    https://github.com/pwnmap-Team/pwnmap-Framework.git

Twitter:
    https://www.twitter.com/elordcs
    https://www.twitter.com/infectedbrowser''')
