import inspect
# fixed 
from abc import ABC, abstractmethod

from .exception import UsageException, ArgumentValueError
from .argument import _Optional


class Command(ABC):
    __slots__ = ('shell',)

    def __init__(self, shell):
        if not issubclass(self.__class__, Command):
            raise NotImplementedError('you cannot instantiate this class')

        self.shell = shell

    @property
    @abstractmethod
    def name(self) -> str:
        """ Command instance name """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """ Command instance description """
        pass

    @abstractmethod
    def run(self, *args):
        """ Abstract run method """
        pass

    @property
    def aliases(self) -> list[str]:
        """ Command instance name aliases """
        return ()

    @property
    def has_aliases(self) -> bool:
        """ Check if Command instance has aliases """
        return hasattr(self, 'aliases')

    @staticmethod
    def execute(fn):
        def _wrapper(*fn_args):
            required_args = inspect.getfullargspec(fn).annotations

            if len(fn_args) - 1 < len(required_args):
                raise UsageException(' '.join(f'<{arg_name.replace("__", "/").replace("_", " ")}>' for arg_name in required_args.keys()))

            kwargs = {'self': fn_args[0]}
            fn_args = fn_args[1:]

            def __is_optional(pt):
                return isinstance(pt, tuple) and isinstance(pt[0], _Optional)

            for i, (param_name, param_type) in enumerate(required_args.items()):
                if i > len(fn_args):
                    if __is_optional(param_type) is True:
                        kwargs[param_name] = None

                        for param_name1 in list(required_args.keys())[i:]:
                            kwargs[param_name1] = None
                        break

                    raise UsageException(' '.join(f'<{arg_name.replace("__", "/").replace("_", " ")}>' for arg_name in required_args.keys()))

                if __is_optional(param_type) is True:
                    param_type = param_type[1]

                if param_type == tuple or param_type == list:  # used for starred expression
                    kwargs[param_name] = param_type(fn_args[i:])
                    break

                param_value = ' '.join(list(map(str, fn_args[i:]))) if i == len(required_args.items()) - 1 else fn_args[i]

                try:
                    kwargs[param_name] = param_type(param_value)
                except ValueError:
                    raise ArgumentValueError('Invalid value for argument \'%s\'. Was expecting type \'%s\'' % (param_name, param_type.__name__))

            return fn(**kwargs)
        return _wrapper
