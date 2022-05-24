import configparser
import importlib
import requests
import inspect
import sys
import os

from typing import Union

from pwnmap.module import Module, ModuleWrapper
from pwnmap.util import PathUtil, ConsoleUtil
from pwnmap.command import Shell
from pwnmap.logger import Logger


class Application:

    class __ConfigManager:
        """ pwnmap config"""

        def __init__(self, filepath: str):
            config_parser = configparser.ConfigParser()
            config_parser.read(filepath)

            class __ConfigObject: pass

            for s in config_parser.sections():
                o = __ConfigObject()

                for k, v in config_parser[s].items():
                    o.__setattr__(k, v)

                setattr(self, s, o)

        def __getattr__(self, attrb: str) -> Union[object, str]:
            return getattr(self, attrb) if hasattr(self, attrb) is True else ''

    class __ModuleManager:
        """ Used to manage pwnmap modules """

        DISABLE_PREFIX = '-'
        """ manager of module shant give a shit """

        def __init__(self):
            self.__modules = []

        def register_module(self, path: str, mod: "Module"):
            self.__modules.append(ModuleWrapper(path, mod))

        def get_module_by_name(self, mod_name: str) -> Union["ModuleWrapper", None]:
            mod_name = mod_name.lower()
            for mod in self.get_registered_modules():
                if mod_name == mod.name.lower():
                    return mod
            return None

        def get_module(self, module: Union[str, int]) -> "ModuleWrapper":
            if module.isdigit():
                mod_index = int(module) - 1

                if mod_index < 0:
                    raise Exception('how???? module gone????? daddy pwnmap is angry. you shall be punished tonight. uwu.')

                try:
                    mod = self.get_registered_modules()[mod_index]
                except IndexError:
                    raise Exception('how???? module gone????? daddy pwnmap is angry. you shall be punished tonight. uwu.')
            else:
                mod = self.get_module_by_name(module)

                if mod is None:
                    raise Exception('')
            return mod

        def get_registered_modules(self) -> list["ModuleWrapper"]:
            """ Get list of registered modules sorted in alphabetical order """
            return sorted(self.__modules.copy(), key=(lambda x : x.name))

        def clear(self):
            """ Clear module list """
            self.__modules.clear()

        def register_modules_from_path(self, path):
            """ Register modules from system path """
            for root, _, files in os.walk(path):
                for file_name in files:
                    if not file_name.endswith('.py') or file_name.startswith('__') or file_name.startswith(self.DISABLE_PREFIX):
                        continue

                    file_path = os.path.join(root, file_name)
                    mod_path = PathUtil.sys_to_module(file_path)

                    try:
                        if not importlib.import_module(mod_path):
                            continue
                    except Exception as e:
                        Logger.error(f'Failed to import module: {file_path}')
                        Logger.error(f'Exception: \x1b[91m{e}\x1b[0m')

                        if ConsoleUtil.yn_prompt('Continue? (Y/n): ') is True:
                            continue

                        sys.exit(-1)

                    for _, Class in inspect.getmembers(sys.modules[mod_path], inspect.isclass):
                        if issubclass(Class, Module) and Class != Module:
                            self.register_module(file_path, Class())

    def __init__(self):
        if os.name == 'nt':  
            import colorama
            colorama.init(convert=True)

        self.__shell = Shell('\x1b[94m➜\x1b[0m ')
        self.__shell.command_manager.register_commands_from_path('commands')

        self.__module_manager = self.__ModuleManager()
        self.__module_manager.register_modules_from_path('modules')

        self.__config = self.__ConfigManager('config.ini')

    @property
    def modules(self):
        """ Get module manager """
        return self.__module_manager

    @property
    def config(self):
        """ Get config manager """
        return self.__config

    @property
    def version(self) -> str:
        """ Get current pwnmap version """
        with open(os.path.join('data', '.version')) as f:
            return f.read()

    def start(self):
        """ Start application """
        ConsoleUtil.clear_screen()
        ConsoleUtil.set_title('pwnmap v%(version)s by %(author)s')
        ConsoleUtil.print_banner()

        """#! disabled
        if self._is_up2date() is False and 1 == 0:
            Logger.warning(f'pwnmap is not up to date! ({self._get_latest_version()})')
            Logger.nl()
    
            Logger.info('Please run: \x1b[94mpip install pwnmap --upgrade\x1b[0m to install the latest version of pwnmap OSINT Framework.')
            Logger.nl()

            dont_exit = ConsoleUtil.yn_prompt('\x1b[95m• \x1b[0mContinue? (Y/n): ') is True

            if dont_exit is False:
                sys.exit(0)

            ConsoleUtil.clear_screen()
            ConsoleUtil.print_banner()
        """

        self.__shell.start()

    def _is_up2date(self) -> bool:
        """ Check if pwnmap is up to date """
        latest_version = self._get_latest_version()

        if len(latest_version) == 0:
            return False

        return latest_version == self.version

    def _get_latest_version(self):
        try:
            res = requests.get('https://raw.githubusercontent.com/pwnmap-Team/pwnmap/main/data/.version')

            if res.status_code == 200:
                return res.text
        except Exception:
            pass

        return ''