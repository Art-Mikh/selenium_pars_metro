import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
from dataclasses import dataclass
from random import randint as rand
import json
from main_parser_class import MainParserClass as Main

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/" +
    "avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": UserAgent().random,
}


@dataclass
class ProductData:
    id: str = ''
    name: str = ''
    reference: str = ''
    regular_price: str = ''
    promo_price: str = ''
    brand: str = ''


class DataToJson(Main):
    @classmethod
    def main(cls, file_path: str) -> None:
        cls.get_data(file_path)

    @classmethod
    def get_data(cls, file_path) -> str:
        with open(file_path) as file:
            urls_list = [url.strip() for url in file]

        product = ProductData()

        result_list: set = []
        result_list.append(file_path.split('.')[0])

        for iter, url in enumerate(urls_list):
            # Парс строка
            url_list = url.split()
            reference = url_list[0]
            regular = promo = ''
            if len(url_list) == 3:
                promo = url_list[1]
                regular = url_list[2]
            else:
                regular = url_list[1]

            response = requests.get(url=reference, headers=headers)            
            soup = BeautifulSoup(response.text, "lxml")

            product.id = cls.get_id(soup)
            product.name = cls.get_name(soup)
            product.reference = reference.strip()
            product.regular_price = regular.strip()
            product.promo_price = promo.strip()
            product.brand = cls.get_brand(soup)

            result_list.append(
                {
                    "id товара": product.id,
                    "наименование": product.name,
                    "ссылка на товар": product.reference,
                    "регулярная цена": product.regular_price,
                    "промо цена": product.promo_price,
                    "бренд": product.brand
                }
            )
            print(iter, product)
            time.sleep(2 + rand(1, 3))

        # save the file as json
        cls.save_json(result_list)

        return "[INFO] Data collected successfully"

    @classmethod
    def get_id(cls, soup: BeautifulSoup) -> str:
        try:
            long_id = soup.find("p", {"class": "product-page-content__article"}).text.strip()
            return long_id.split()[1] if long_id else ''
        except Exception:
            return None

    @classmethod
    def get_name(cls, soup: BeautifulSoup) -> str:
        try:
            return soup.find(
                "h1", {"class": "product-page-content__product-name"}
            ).text.strip()
        except Exception:
            return None

    @classmethod
    def get_brand(cls, soup: BeautifulSoup) -> str:
        try:
            brand = ''
            table = soup.find('ul', class_="product-attributes__list")
            for ind, li in enumerate(table.findAll('li')):
                d = li.find_all("span", string="Бренд")
                if ind == 5:
                    brand = li.find('a').get_text()

            return brand.strip()
        except Exception:
            return None

    @classmethod
    def save_json(cls, data_collection: list | set) -> None:
        with open("result.json.json", "a") as file:
            json.dump(data_collection, file, indent=4, ensure_ascii=False)
