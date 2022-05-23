from cumware.command import Command

import cumware


class CreditsCommand(Command):
    name = 'credits'
    description = 'Show cumware OSINT Framework credits'
    aliases = 'credit', 'info', 'about'

    @Command.execute
    def run(self):
        print(rf'''
 ___ ____  ___ ____  
|_ _|  _ \|_ _/ ___| 
 | || |_) || |\___ \ 
 | ||  _ < | | ___) |
|___|_| \_\___|____/ 
                      

cumware version {cumware.__version__}: an open-source intelligence framework 

Developed by {cumware.__author__}

GitHub:
    https://github.com/cumware-Team/cumware-Framework.git

Twitter:
    https://www.twitter.com/elordcs
    https://www.twitter.com/infectedbrowser''')
