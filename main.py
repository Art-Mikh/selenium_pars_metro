from parsing_main_site_page import MainSiteHTML as det_html
from lxml_parser import LXMLParser as lxml_parser
from data_to_json import DataToJson as data_to_json


def main() -> None:
    """Calls classes to receive data in order to obtain a JSION file as a result.
    1) Creates an HTML file
    2) Uses an HTML file, returns a TXT file
    3) Uses the TXT file, returns JSON
    """
    det_html.main(
        url="https://online.metro-cc.ru/category/ovoshchi-i-" +
        "frukty/frukty?from=under_search&in_stock=1"
    )

    lxml_parser.main(file_path="moscow.html")
    lxml_parser.main(file_path="st_petersburg.html")

    data_to_json.main(file_path="moscow.txt")
    data_to_json.main(file_path="st_petersburg.txt")


if __name__ == "__main__":
    main()
