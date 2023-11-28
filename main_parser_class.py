"""The main architectural interface class for
working with website parsing.
Each class must have a main method that
will run all the logic inside the handler classes.
"""
from abc import ABC, abstractmethod


class MainParserClass(ABC):
    """The main architectural interface
    class for working with website parsing
    """
    @abstractmethod
    def main():
        """method to run logic of any class"""
        pass
