from bs4 import BeautifulSoup
import requests
import csv
import re

URL = "https://www.olx.ua/rabota/it-telekom-kompyutery/odessa/?page={}"
# URL = "https://www.olx.ua/rabota/it-telekom-kompyutery/?page={}"

def get_html(url, page):
    try:
        page = requests.get(url.format(page))
        return BeautifulSoup(page.content, "html.parser")
    except:
        return False

def clean(row):
    row = str(row).replace("\n", "").replace("\t", "").strip()
    return re.sub(r'\s+', ' ', row)

def all_pages():
    #страницы
    first_page = get_html(URL, 1)
    try:
        max_page = first_page.find("div", {"class": "pager"}).find_all("span")
        pages_list = []
        for i in max_page:
            try:
                i = int(i.text)
                pages_list.append(i)
            except:
                pass
        pages_list = list(set(pages_list))
    except:
        pages_list = [1]

    #проходка по страницам
    for page in range(pages_list[-1]):
        parse_page = get_html(URL, page+1)
        table = parse_page.find("table", {"id":"offers_table"})
        rows_in_table = table.find_all('tr', {"class":"wrap"})
        result = []
        for row in rows_in_table:
            name_offer = clean(row.find("h3").text)
            url_offer = row.find("h3").find("a").get("href")
            salary = clean(row.find("div", {"class": "list-item__price"}).text)
            bottom = clean(row.find("td", {"valign":"bottom"}).text)
            item = {"name_offer": name_offer, "url_offer": url_offer, "salary": salary, "bottom": bottom}
            result.append(item)
        return result


if __name__ == "__main__":
    all_pages()


