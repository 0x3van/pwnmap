import os


class PathUtil:

    @staticmethod
    def sys_to_module(*args) -> str:
        """ Convert system path to Python module path """
        return os.path.join(*[x[:-3] if x.endswith('.py') else x for x in args]).replace(os.path.sep, '.')
