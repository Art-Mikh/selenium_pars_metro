# https://www.youtube.com/watch?v=w7YEorllJZI&t=294s

# DOC merto API
# https://developer.metro-selleroffice.com/docs/rest-api/
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from fake_useragent import UserAgent
from dataclasses import dataclass
from random import randrange as rand
import json

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": UserAgent().random,
}


def get_source_html(url: str) -> None:
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        driver.get(url=url)  # pass the path
        time.sleep(7)  # waiting for the page to load

        while True:
            # if the block is not found, then save the received data to the file and exit the loop
            find_list = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Показать ещё')]")
            if not len(find_list):
                with open("metro.html", "w") as file:
                    file.write(driver.page_source)
                break  # exit the loop
            else:
                buttons = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Показать ещё')]")

                for btn in buttons:
                    btn.click()
                time.sleep(7)  # waiting for the page to load

    except Exception as exc:
        print(exc)
    finally:
        driver.close()
        driver.quit()


def get_items_urls(file_path: str) -> str:
    with open(file_path, 'r') as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("div", class_="product-card__content")

    urls = []
    for a in soup.find_all('a', class_="product-card-name"):
        urls.append('https://online.metro-cc.ru' + a['href'])
    print(urls)

    # save temporary results
    with open("items_urls.txt", "w") as file:
        for url in urls:
            file.write(f"{url}\n")

    return "[INFO] Urls collected successfully!"


@dataclass
class ProductData:
    id: str = ''
    name: str = ''
    reference: str = ''
    regular_price: str = ''
    promo_price: str = ''
    brand: str = ''


def get_data(file_path):
    with open(file_path) as file:
        urls_list = [url.strip() for url in file]
    #print(urls_list, len(urls_list))

    product = ProductData()

    result_list = []

    for iter, url in enumerate(urls_list):
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        print(soup)

        try:
            long_id = soup.find("p", {"class": "product-page-content__article"}).text.strip()
            product.id = long_id.split()[1] if long_id else ''
        except Exception:
            product.id = None

        try:
            product.name = soup.find("h1", {"class": "product-page-content__product-name"}).text.strip()
        except Exception:
            product.name = None

        try:
            product.reference = url.strip()
        except Exception:
            product.reference = None

        try:
            prise_list = soup.find("span", {"class": "product-price__sum"})
            #prise_list.sort()
            product.regular_price = prise_list
        except Exception:
            product.regular_price = None

        try:
            product.promo_price = soup.find("div", {"class": "product-unit-prices__old-wrapper"}).text.strip()
        except Exception:
            product.promo_price = None

        try:
            product.brand = soup.find("span", {"class": "product-attributes__list-item-value"}).text.strip()
        except Exception:
            product.brand = None

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
        time.sleep(rand(3, 5))

    # save the file as json
    with open("result.json.json", "w") as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

    return "[INFO] Data collected successfully"


def main() -> None:
    # вид ссылки на первую страницу
    # https://online.metro-cc.ru/category/ovoshchi-i-frukty/frukty?from=under_search&in_stock=1
    # вид ссылки на вторую страницу
    # https://online.metro-cc.ru/category/ovoshchi-i-frukty/frukty?from=under_search&page=2&in_stock=1
    get_source_html(url="https://online.metro-cc.ru/category/ovoshchi-i-frukty/frukty?from=under_search&in_stock=1")
    #get_items_urls(file_path="metro.html")
    #get_data(file_path="items_urls.txt")


if __name__ == "__main__":
    main()
