import subprocess
import random
import os

from pwnmap.logger import Logger

import pwnmap


class ConsoleUtil:
    __BANNER = '''
  \x1b[96m  _ ____      ___ __  _ __ ___   __ _ _ __   
  \x1b[96m | '_ \ \ /\ / / '_ \| '_ ` _ \ / _` | '_ \   \x1b[0mrevamped by %(author)s\x1b[0m
  \x1b[96m | |_) \ V  V /| | | | | | | | | (_| | |_) |  \x1b[90m@pwnmap
 \x1b[96m  | .__/ \_/\_/ |_| |_|_| |_| |_|\__,_| .__/   \x1b[90m@ too swag\x1b[0m
 \x1b[96m  | |                                 | |     \x1b[90m@ dwi\x1b[0m
 \x1b[96m  |_|                                 |_|      \x1b[90m@ \x1b[0m                                      
  \x1b[0mv%(version)s                                  \x1b[90m@ \x1b[0m
'''

    @staticmethod
    def clear_screen():
        """ Clear console screen """
        subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

    @staticmethod
    def set_title(title: str):
        """ Set console title """
        title = title % {'author': pwnmap.__author__, 'version': pwnmap.__version__}
        if os.name == 'nt':
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        else:
            print('\x1b]0;' + title, end='\a')

    @staticmethod
    def yn_prompt(prompt: str) -> bool:
        """ Spawn Yes/No prompt """
        while True:
            answer = input(prompt)
            
            if len(answer) == 0:
                continue

            answer = answer.lower()

            if answer.startswith('y'):
                return True

            elif answer.startswith('n'):
                return False

            Logger.warning('Input must be either Yes or No')

    @staticmethod
    def print_banner():
        """ Print banner """
        print(ConsoleUtil.__BANNER.lstrip(' ').replace('##', random.choice('8o.-_#|@0!/\\?+><*`´¨') * 2) % {'version': pwnmap.__version__, 'author': pwnmap.__author__} + '\x1b[0m')
