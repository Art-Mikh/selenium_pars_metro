"""The file that implements the logic for
receiving HTML data from the main page of the site
"""
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
        cls.get_source_html(
            url=url,
            file_path="moscow.html",
            address="Москва, Малая Бронная улица, 34"
        )
        cls.get_source_html(
            url=url,
            file_path="st_petersburg.html",            
            # "Санкт-Петербург, Подольская улица, 38"
            address="Санкт-Петербург, Малодетскосельский проспект, 7"
        )

    @classmethod
    def get_source_html(
        cls,
        url: str,
        file_path: str,
        address: str
    ) -> None:
        """Method for obtaining html site data

        Args:
            url (str): address of the required website
        """
        driver = webdriver.Chrome()
        driver.maximize_window()
        try:
            driver.get(url=url)
            time.sleep(3)  # waiting for the page to load
            cls.open_address_entry_window(driver)
            cls.enter_addresses(driver, address)
            cls.click_save_button(driver)
            cls.scroll_page(driver, file_path)
            time.sleep(3)
        except Exception as exc:
            print(exc)
        finally:
            driver.close()
            driver.quit()

    @classmethod
    def open_address_entry_window(cls, driver: webdriver.Chrome) -> None:
        """Opens the address entry window

        Args:
            driver (webdriver.Chrome): webdriver.Chrome object with HTML
        """
        button = driver.find_element(By.CLASS_NAME, "header-address__receive-button")
        button.click()
        time.sleep(2)

    @classmethod
    def enter_addresses(cls, driver: webdriver.Chrome, address: str) -> None:
        """_summary_

        Args:
            driver (webdriver.Chrome): webdriver.Chrome object with HTML
            address (str): the address where we are looking for products
        """
        input = driver.find_element(By.ID, "search-input")
        input.clear()  # Clearing an input field
        input.send_keys(address)  # Filling in the address
        time.sleep(4)
        input.send_keys(Keys.ENTER)
        time.sleep(4)

    @classmethod
    def click_save_button(cls, driver: webdriver.Chrome) -> None:
        """clicks on the “save” button to close the
        address entry window and save the search parameters

        Args:
            driver (webdriver.Chrome): webdriver.Chrome object with HTML
        """
        # Get the list of "Сохранить" buttons
        save_list = driver.find_elements(
            By.CLASS_NAME,
            "rectangle-button"
        )

        # Find the actual "Сохранить" button
        for btn in save_list:
            try:
                btn.click()
                break
            except Exception:
                continue
        time.sleep(10)

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
