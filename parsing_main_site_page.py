from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from main_parser_class import MainParserClass as Main
from selenium.webdriver.common.keys import Keys



class MainSiteHTML(Main):
    @classmethod
    def main(cls, url: str) -> None:
        """Method to run logic of the class

        Args:
            url (str): address of the required website
        """
        cls.get_source_html(url)

    @classmethod
    def get_source_html(cls, url: str) -> None:
        """Method for obtaining html site data

        Args:
            url (str): address of the required website
        """
        driver = webdriver.Chrome()
        driver.maximize_window()
        try:
            driver.get(url=url)
            time.sleep(3)  # waiting for the page to load

            # Setting up geolocation for Moscow
            button = driver.find_element(By.CLASS_NAME, "header-address__receive-button")
            button.click()
            time.sleep(2)

            input = driver.find_element(By.ID, "search-input")
            input.send_keys("Москва, Малая Бронная улица, 34")
            time.sleep(4)
            input.send_keys(Keys.ENTER)
            print("кнопка нажата!")
            time.sleep(4)
            print("Адрес введен успешно!")
            save_list = driver.find_elements(By.CLASS_NAME,
                "rectangle-button"
            )
            print(len(save_list), "количество найденных")
            for numb, btn in enumerate(save_list):
                print(numb)
                try:
                    btn.click()
                    print("Нажал!")
                    break
                except Exception:
                    continue
            time.sleep(10)

            # Perform reading for Moscow
            cls.scroll_page(driver, "moscow.html")

            print("Москва кончилась")
            time.sleep(3)

            # Reload
            driver.get(url=url)

            # Setting up geolocation for St. Petersburg
            button = driver.find_element(By.CLASS_NAME, "header-address__receive-button")
            button.click()
            time.sleep(3)
            print("Жмем вторую кнопку")
            input = driver.find_element(By.ID, "search-input")
            input.clear()
            input.send_keys("Санкт-Петербург, Подольская улица, 38")

            time.sleep(4)
            input.send_keys(Keys.ENTER)
            print("кнопка нажата!")
            time.sleep(4)
            print("Адрес введен успешно!")
            save_list = driver.find_elements(By.CLASS_NAME,
                "rectangle-button"
            )
            print(len(save_list), "количество найденных")
            for numb, btn in enumerate(save_list):
                print(numb)
                try:
                    btn.click()
                    print("Нажал!")
                    break
                except Exception:
                    continue
            time.sleep(10)

            # Perform reading for St. Petersburg
            cls.scroll_page(driver, "st_petersburg.html")
            print("Получение всех продуктов завершено")
        except Exception as exc:
            print(exc)
        finally:
            driver.close()
            driver.quit()

    @classmethod
    def scroll_page(cls, driver: webdriver.Chrome, name_file: str) -> None:
        """In this method, the full list of products
        will be expanded, and then read and saved to a file

        Args:
            driver (webdriver.Chrome): object of class webdriver.Chrome
        """
        while True:
            buttons_list = cls.find_button(driver)
            """If the block is not found, then save
            the received data to the file and exit
            the loop, otherwise, click on the found button
            """
            if not len(buttons_list):
                cls.save_file(driver, name_file)
                break  # exit the loop
            else:
                cls.click_button(driver, buttons_list)

    @classmethod
    def find_button(cls, driver: webdriver.Chrome) -> list:
        """Method for searching for a button on a website

        Args:
            driver (webdriver.Chrome): object of class webdriver.Chrome

        Returns:
            list: list of found elements
        """
        return driver.find_elements(
            by=By.XPATH,
            value="//*[contains(text(), 'Показать ещё')]"
        )

    @classmethod
    def save_file(cls, driver: webdriver.Chrome, name_file: str) -> None:
        """Method for saving the file

        Args:
            driver (webdriver.Chrome): object of class webdriver.Chrome
        """
        with open(name_file, "w") as file:
            file.write(driver.page_source)

    @classmethod
    def click_button(cls, driver: webdriver.Chrome, buttons_list: list) -> None:
        """Method of pressing the buttons found

        Args:
            driver (webdriver.Chrome): object of class webdriver.Chrome
            buttons_list (list): list of web elements with buttons
        """
        for btn in buttons_list:
            btn.click()
        time.sleep(7)
