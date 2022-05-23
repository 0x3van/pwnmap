import subprocess
import random
import os

from cumware.logger import Logger

import cumware


class ConsoleUtil:
    __BANNER = '''
  \x1b[96m  ___ _   _ _ __ _____      ____ _ _ __ ___   
  \x1b[96m/ __| | | | '_ ` _ \ \ /\ / / _` | '__/ _ \  \x1b[0mrevamped by %(author)s\x1b[0m
  \x1b[96m| (__| |_| | | | | | \ V  V / (_| | | |  __/  \x1b[90m@cumware
 \x1b[96m \___|\__,_|_| |_| |_|\_/\_/ \__,_|_|  \___|  \x1b[90m@ too swag\x1b[0m
  \x1b[0mv%(version)s        
'''

    @staticmethod
    def clear_screen():
        """ Clear console screen """
        subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

    @staticmethod
    def set_title(title: str):
        """ Set console title """
        title = title % {'author': cumware.__author__, 'version': cumware.__version__}
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
        print(ConsoleUtil.__BANNER.lstrip(' ').replace('##', random.choice('8o.-_#|@0!/\\?+><*`´¨') * 2) % {'version': cumware.__version__, 'author': cumware.__author__} + '\x1b[0m')
