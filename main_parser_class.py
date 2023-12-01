"""The main architectural interface class for
working with website parsing.
Each class must have a main method that
will run all the logic inside the handler classes.
"""
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome


class ErrorMixin:
    @staticmethod
    def check_str_parameter(string: str) -> None:
        if not isinstance(string, str):
            raise TypeError("The passed parameter must be Str")

    @staticmethod
    def check_bs_parameter(bs: BeautifulSoup) -> None:
        test = BeautifulSoup("html text", "lxml")
        if type(bs) != type(test):
            raise TypeError("The passed parameter must be BeautifulSoup")

    @staticmethod
    def check_wd_parameter(wd: webdriver) -> None:
        #test = webdriver.Chrome()
        # test.close()
        # test.quit()
        if not isinstance(wd, Chrome):
            raise TypeError("The passed parameter must be webdriver")

    @staticmethod
    def check_list_parameter(_list: list) -> None:
        if not isinstance(_list, list):
            raise TabError("The passed parameter must be list")


class MainParserClass(ABC, ErrorMixin):
    """The main architectural interface
    class for working with website parsing
    """
    @abstractmethod
    def main():
        """method to run logic of any class"""
        pass
