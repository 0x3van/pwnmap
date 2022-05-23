import cumware

from cumware.command import Command
from cumware.command.exception import UsageException, ArgumentValueError


def custom_usage_decorator(fn):
    def _wrapper(*fn_args):
        if len(fn_args) - 1 >= 1:
            module = fn_args[1]

            mod = cumware.__app__.modules.get_module(module)

            if len(fn_args) - 1 < 1 + len(mod.execute_method_parameters):
                raise UsageException(mod.name + ' ' + ' '.join(f'<{arg_name.replace("__", "/").replace("_", " ")}>' for arg_name in mod.execute_method_parameters.keys()))

            for i, (mod_param_name, mod_param_type) in enumerate(mod.execute_method_parameters.items()):
                mod_param_value = fn_args[2 + i]  # +2 offset bcuz: self, module name

                try:
                    mod_param_type(mod_param_value)
                except ValueError:
                    raise ArgumentValueError('Invalid value for argument \'%s\'. Was expecting type \'%s\'' % (mod_param_name, mod_param_type.__name__))
        return fn(*fn_args)
    return _wrapper


class UseCommand(Command):
    name = 'use'
    description = 'Use module'
    aliases = 'select', 'pick', 'run', 'execute'

    @custom_usage_decorator
    @Command.execute
    def run(self, module: str, module_arguments: tuple):
        mod = cumware.__app__.modules.get_module(module)
    
        kwargs = {}

        required_args = mod.execute_method_parameters.keys()

        for i, arg_name in enumerate(required_args):
            kwargs |= {arg_name: module_arguments[i]}

            if i == len(required_args) - 1:
                kwargs[arg_name] = ' '.join(str(arg) for arg in module_arguments[i:])

        return mod.instance.execute(**kwargs)