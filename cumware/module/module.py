from abc import ABC, abstractproperty, abstractmethod


class Module(ABC):
    """ cumware module blueprint """


    @abstractproperty
    def description(self):
        """ Module description """
        pass

    @abstractproperty
    def author(self):
        """ Module author """
        pass

    @abstractproperty
    def date(self):
        """ Module date"""
        pass

    def __init__(self):
        if not issubclass(self.__class__, Module):
            raise NotImplementedError('You cannot instantiate this class')

    @abstractmethod
    def execute(self, **kwargs):
        """ Abstract execute method. This method will contain the actual code of the specific module """
        pass
