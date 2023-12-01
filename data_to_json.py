"""This file contains the logic for reading links andproduct prices from the txt file.
Based on the received links, a “requests” request is
executed to obtain the main attributes of the product.
The query results are collected into a list and written to a json file
"""
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
from random import randint as rand
import json
from main_parser_class import MainParserClass as Main

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/" +
    "avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": UserAgent().random,
}


@dataclass
class ProductAttributes:
    """Stores product attributes"""
    REFERENCE: str = ''
    REGULAR:   str = ''
    PROMO:     str = ''


class DataToJson(Main):
    """The class for obtaining links and prices from a TXT file and creating
    requests to the site in order to obtain output data for recording in json.
    """
    @classmethod
    def main(cls, file_path: str) -> None:
        """Method to run logic of the class

        Args:
            url (str): path to TXT file
        """
        DataToJson.check_str_parameter(file_path)
        cls.get_data(file_path)

    @classmethod
    def get_data(cls, file_path: str) -> str:
        """Receives data from TXT and executes requests on
        the received links to save the result in a JSON file

        Args:
            file_path (_type_): path to TXT file

        Returns:
            str: method success message
        """
        DataToJson.check_str_parameter(file_path)
        urls_list: list = cls.get_list_strings(file_path)

        result_list: list = []
        result_list.append(file_path.split('.')[0])  # Сity name is added

        for url in urls_list:
            prod_attr: ProductAttributes = cls.get_attributes(url)
            soup: BeautifulSoup = cls.get_additional_attribute(prod_attr.REFERENCE)

            # Filling the list of products for uploading in json
            result_list.append(
                {
                    "id товара": cls.get_id(soup),
                    "наименование": cls.get_name(soup),
                    "ссылка на товар": prod_attr.REFERENCE.strip(),
                    "регулярная цена": prod_attr.REGULAR.strip(),
                    "промо цена": prod_attr.PROMO.strip(),
                    "бренд": cls.get_brand(soup)
                }
            )
            time.sleep(1 + rand(1, 2))

        cls.save_json(result_list)
        return "[INFO] Data collected successfully"

    @classmethod
    def get_list_strings(cls, file_path: str) -> list:
        """Returns a list of lines read from a file at the specified path

        Args:
            file_path (str): path to TXT file

        Returns:
            list: list of strings
        """
        DataToJson.check_str_parameter(file_path)
        with open(file_path) as file:
            return [url.strip() for url in file]

    @classmethod
    def get_additional_attribute(cls, reference: str) -> BeautifulSoup:
        """obtaining additional product parameters via "requests"

        Args:
            reference (str): link to product page

        Returns:
            BeautifulSoup: object with HTML
        """
        DataToJson.check_str_parameter(reference)
        print(reference)
        response = requests.get(url=reference, headers=headers)
        return BeautifulSoup(response.text, "lxml")

    @classmethod
    def get_attributes(cls, attribute_string: str) -> ProductAttributes:
        """Returns the attributes of an object obtained
        from a string containing a link to the site and prices

        Args:
            attribute_string (str): line containing link and prices

        Returns:
            ProductAttributes: Returns the ProductAttributes
            object containing product attributes
        """
        DataToJson.check_str_parameter(attribute_string)
        url_list: list = attribute_string.split()

        prod_attr = ProductAttributes()

        prod_attr.REFERENCE = url_list[0]
        if len(url_list) == 3:
            prod_attr.PROMO = url_list[1]
            prod_attr.REGULAR = url_list[2]
        else:
            prod_attr.REGULAR = url_list[1]
        return prod_attr

    @classmethod
    def get_id(cls, soup: BeautifulSoup) -> str:
        """Getting product 'ID' from HTML

        Args:
            soup (BeautifulSoup): object containing HTML

        Returns:
            str: found product ID
        """
        DataToJson.check_bs_parameter(soup)
        try:
            long_id = soup.find("p", {"class": "product-page-content__article"}).text.strip()
            return long_id.split()[1] if long_id else ''
        except Exception:
            return ''

    @classmethod
    def get_name(cls, soup: BeautifulSoup) -> str:
        """Getting product 'Name' from HTML

        Args:
            soup (BeautifulSoup): object containing HTML

        Returns:
            str: found product 'Name'
        """
        DataToJson.check_bs_parameter(soup)
        try:
            return soup.find(
                "h1", {"class": "product-page-content__product-name"}
            ).text.strip()
        except Exception:
            return ''

    @classmethod
    def get_brand(cls, soup: BeautifulSoup) -> str:
        """Getting product 'Brand' from HTML

        Args:
            soup (BeautifulSoup): object containing HTML

        Returns:
            str: found product 'Brand'
        """
        DataToJson.check_bs_parameter(soup)
        result_list = []
        try:
            brand = ''
            table = soup.find('ul', class_="product-attributes__list")

            # Save all product attributes to select the last one
            for li in table.findAll('li'):
                result_list.append(li)
            brand = result_list[-1].find('a').get_text()

            return brand.strip()
        except Exception:
            return ''

    @classmethod
    def save_json(cls, data_collection: list) -> None:
        """Saves a list of product attributes to a json file

        Args:
            data_collection (list): list with product attributes
        """
        DataToJson.check_list_parameter(data_collection)
        with open("result.json", "a") as file:
            json.dump(data_collection, file, indent=4, ensure_ascii=False)
