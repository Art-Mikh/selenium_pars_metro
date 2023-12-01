from unittest import TestCase, main
from enum import Enum
from bs4 import BeautifulSoup
from data_to_json import DataToJson as to_json


class TestDataToJson(TestCase):
    """For testing methods of the DataToJson class"""

    def test_main(self) -> None:
        self.assertEqual(to_json.main(file_path="moscow.html"), None)

    def test_main_err(self) -> None:
        print(0)
        self.assertEqual(to_json.main(file_path=5), to_json.check_str_parameter(5))

    def test_main_err(self) -> None:
        with self.assertRaises(TypeError) as err:
            to_json.main(file_path=5)
        message = ErrorMessages.STR.value
        self.assertEqual(message, err.exception.args[0])

    def test_get_data(self) -> None:
        self.assertEqual(
            to_json.get_data(file_path="moscow.html"),
            "[INFO] Data collected successfully"
        )

    def test_get_list_strings(self) -> None:
        self.assertTrue(to_json.get_list_strings(file_path="moscow.html"))

    def test_get_data_err(self) -> None:
        with self.assertRaises(TypeError) as err:
            to_json.get_data(file_path=[6, 7, "test"])
        message = ErrorMessages.STR.value
        self.assertEqual(message, err.exception.args[0])

    def test_get_additional_attribute(self) -> None:
        self.assertTrue(to_json.get_additional_attribute(reference="https://ru.hexlet.io/"))

    def test_get_additional_attribute_err(self) -> None:
        with self.assertRaises(TypeError) as err:
            to_json.get_additional_attribute(reference={3: "test"})
        message = ErrorMessages.STR.value
        self.assertEqual(message, err.exception.args[0])

    def test_get_attributes(self) -> None:
        self.assertTrue(to_json.get_attributes("dfasdff.com 45 67"))

    def test_get_attributes_err(self) -> None:
        with self.assertRaises(TypeError) as err:
            to_json.get_attributes(56)
        message = ErrorMessages.STR.value
        self.assertEqual(message, err.exception.args[0])

    def test_get_id(self) -> None:
        soup = BeautifulSoup("", "lxml")
        self.assertEqual(to_json.get_id(soup), '')

    def test_get_id_err(self) -> None:
        with self.assertRaises(TypeError) as err:
            to_json.get_id([4, 6, 12])
        message = ErrorMessages.BEAUTIFULSOUP.value
        self.assertEqual(message, err.exception.args[0])

    def test_get_name(self) -> None:
        soup = BeautifulSoup("", "lxml")
        self.assertEqual(to_json.get_name(soup), '')

    def test_get_name_err(self) -> None:
        with self.assertRaises(TypeError) as err:
            to_json.get_name(876.67)
        message = ErrorMessages.BEAUTIFULSOUP.value
        self.assertEqual(message, err.exception.args[0])

    def test_get_brand(self) -> None:
        soup = BeautifulSoup("", "lxml")
        self.assertEqual(to_json.get_brand(soup), '')

    def test_get_brand_err(self) -> None:
        with self.assertRaises(TypeError) as err:
            to_json.get_brand(['45', 54, 1.23])
        self.assertEqual(ErrorMessages.BEAUTIFULSOUP.value, err.exception.args[0])

    def test_save_json(self) -> None:
        self.assertEqual(to_json.save_json["erer", "ertw"], None)

    def test_save_json_err(self) -> None:
        with self.assertRaises(TypeError) as err:
            to_json.save_json(56.8)
        message = ErrorMessages.BEAUTIFULSOUP.value
        self.assertEqual(message, err.exception.args[0])


class ErrorMessages(Enum):
    """to store error messages"""
    STR:            str = "The passed parameter must be Str"
    BEAUTIFULSOUP:  str = "The passed parameter must be BeautifulSoup"
    WEBDRIWER:      str = "The passed parameter must be webdriver"
    LIST:           str = "The passed parameter must be list"


if __name__ == "__main__":
    main()
