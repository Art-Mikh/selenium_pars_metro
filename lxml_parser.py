"""File with a class for converting HTML into a list of
addresses and prices and saving the result to a TXT file
"""
from bs4 import BeautifulSoup
from main_parser_class import MainParserClass as Main


class LXMLParser(Main):
    """Class for converting HTML into a list of addresses and
    prices and saving the result to a TXT file
    """
    @classmethod
    def main(cls, file_path: str) -> str:
        """Method to run logic of the class

        Args:
            url (str): path to HTML file
        """
        LXMLParser.check_str_parameter(file_path)
        cls.get_items_urls(file_path)

    @classmethod
    def get_items_urls(cls, file_path: str) -> str:
        """Method for obtaining a list of addresses for each found product

        Args:
            file_path (str): path to HTML file

        Returns:
            str: status message about successful completion
        """
        LXMLParser.check_str_parameter(file_path)
        src: str = cls.open_file(file_path)
        soup = BeautifulSoup(src, "lxml")
        urls: list = cls.generate_string_list(soup)
        cls.save_file(urls, file_path)
        return "[INFO] Urls collected successfully!"

    @classmethod
    def open_file(cls, file_path: str) -> str:
        """The method reads the file

        Args:
            file_path (str): path to HTML file

        Returns:
            str: lines from open file
        """
        LXMLParser.check_str_parameter(file_path)
        with open(file_path, 'r') as file:
            src = file.read()
        return src

    @classmethod
    def generate_string_list(cls, soup: BeautifulSoup) -> list:
        """The method generates a list of strings with addresses and prices

        Args:
            soup (BeautifulSoup): BeautifulSoup object with data

        Returns:
            list: list of links and prices
        """
        LXMLParser.check_bs_parameter(soup)
        urls = []
        for block in soup.find_all('div', class_="product-card__content"):
            reference = block.find('a', class_="product-card-name")
            reference = 'https://online.metro-cc.ru' + reference['href']
            for prise in block.find_all('span', class_="product-price__sum-rubles"):
                reference = f"{reference} {prise.get_text()}"
            urls.append(reference)
        return urls

    @classmethod
    def save_file(cls, urls: list, file_path: str) -> None:
        """the method saves the result to a txt file

        Args:
            urls (list): list of links and prices
        """
        LXMLParser.check_list_parameter(urls)
        LXMLParser.check_str_parameter(file_path)
        name: str = file_path.split('.')[0]
        with open(name + ".txt", "w") as file:
            for url in urls:
                file.write(f"{url}\n")
