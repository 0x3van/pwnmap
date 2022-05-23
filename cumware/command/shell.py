import importlib
import inspect
import sys
import os

from typing import Union

from cumware.util import PathUtil
from cumware.logger import Logger

from .command import Command
from .exception import UsageException


class Shell:

    class __CommandManager:

        def __init__(self, shell: "Shell"):
            self.shell = shell
            self.__commands = []

        def get_command_by_name(self, cmd_name: str) -> Union["Command", None]:
            """ Get command object by string name """
            cmd_name = cmd_name.lower()
            for cmd in self.__commands:
                if cmd_name == cmd.name.lower() or cmd.has_aliases and cmd_name in map(lambda x: x.lower(), cmd.aliases):
                    return cmd
            return None

        def get_registered_commands(self) -> list["Command"]:
            """ Get registered commands list """
            return sorted(self.__commands.copy(), key=(lambda x : x.name))

        def register_command(self, cmd: "Command"):
            """ Register command """
            if not isinstance(cmd, Command):
                raise ValueError('invalid command')
            self.__commands.append(cmd)

        def register_commands_from_path(self, path: str):
            """ Register commands from system path """
            items = os.listdir(path)

            if '__init__.py' in items:
                items.remove('__init__.py')

            for py_file_name in (x[:-3] for x in items if x.endswith('.py') and not x.startswith('-')):
                mod_path = PathUtil.sys_to_module(path, py_file_name)

                try:
                    if not importlib.import_module(mod_path):
                        continue
                except Exception:
                    continue

                for _, Class in inspect.getmembers(sys.modules[mod_path], inspect.isclass):
                    if issubclass(Class, Command) and Class != Command:
                        self.register_command(Class(self.shell))

    def __init__(self, prompt: str):
        self.__prompt = prompt
        self.__command_manager = self.__CommandManager(self)

    @property
    def prompt(self) -> str:
        """ Get shell prompt """
        return self.__prompt.rstrip(' ')

    @property
    def command_manager(self) -> "__CommandManager":
        """ Get shell command manager """
        return self.__command_manager

    def start(self):
        """ Start shell """
        try:
            while True:
                cmd_line = input(self.__prompt)
                print(end='\x1b[0m')

                if len(cmd_line) == 0:
                    continue

                cmd_name, cmd_args = self.__parse_command_line(cmd_line)

                # handle as shell command
                if cmd_name.startswith('!'):
                    cmd_line = cmd_line[1:]

                    if cmd_name.lower() == 'cd':
                        os.chdir(' '.join(cmd_args))
                    else:
                        os.system(cmd_line)
                        Logger.nl()
                else:
                    cmd = self.__command_manager.get_command_by_name(cmd_name)

                    if cmd is not None:
                        try:
                            no_newline = cmd.run(*cmd_args)

                            if not no_newline:
                                Logger.nl()

                        except UsageException as e:
                            Logger.usage('Usage: ' + cmd_name + ' ' + str(e))

                        except Exception as e:
                            Logger.error(e.args[0])
                            Logger.nl()
                    else:
                        Logger.error('Unknown command: %s' % cmd_name)

        except KeyboardInterrupt:
            Logger.nl()

        except EOFError:
            pass

    def __parse_command_line(self, cmd_line: str) -> tuple[str, list[str]]:
        """ Parse command line to command name and command arguments """
        parts = [x for x in cmd_line.split(' ') if len(x) > 0]
        cmd_name = parts[0]
        cmd_args = parts[1:]
        return cmd_name, cmd_args
