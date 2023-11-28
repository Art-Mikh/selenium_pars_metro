# DOC merto API
# https://developer.metro-selleroffice.com/docs/rest-api/
from parsing_main_site_page import MainSiteHTML as det_html_site
from lxml_parser import LXMLParser as lxml_parser
from data_to_json import DataToJson as data_to_json


def main() -> None:
    # вид ссылки на первую страницу
    # https://online.metro-cc.ru/category/ovoshchi-i-frukty/frukty?from=under_search&in_stock=1
    det_html_site.main(
        url="https://online.metro-cc.ru/category/ovoshchi-i-" +
        "frukty/frukty?from=under_search&in_stock=1"
    )
    lxml_parser.main(file_path="moscow.html")
    lxml_parser.main(file_path="st_petersburg.html")
    data_to_json.main(file_path="moscow.txt")
    data_to_json.main(file_path="st_petersburg.txt")


if __name__ == "__main__":
    main()
