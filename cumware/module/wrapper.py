import inspect
import os

from .module import Module


class ModuleWrapper:
    """ Module class wrapper """

    def __init__(self, path, instance):
        fixed_path = path.split(os.sep, 1)[1].replace(os.sep, '/')[:-3]

        parts = fixed_path.split('/')

        category = parts[0]

        if len(category) == len(fixed_path):
            raise Exception('module category is missing')

        self.__name = fixed_path
        self.__filename = parts[-1]
        self.__category = category
        self.__subcategory = (len(parts) == 3 and parts[1]) or None
        self.__instance = instance

    @property
    def name(self) -> str:
        """ Get module name """
        return self.__name

    @property
    def filename(self) -> str:
        """ Get module file name"""
        return self.__filename

    @property
    def category(self) -> str:
        """ Get module category """
        return self.__category

    @property
    def subcategory(self) -> str:
        """ Get module sub category """
        return self.__subcategory

    @property
    def instance(self) -> "Module":
        """ Get cumware module instance """
        return self.__instance

    @property
    def execute_method_parameters(self) -> dict[str: type]:
        """ Get parameters of execute method """
        return inspect.getfullargspec(self.instance.execute).annotations
