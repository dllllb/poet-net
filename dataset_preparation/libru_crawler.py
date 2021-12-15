import requests
from bs4 import BeautifulSoup
import time
import json
import sys
import re

# Collected manually
PUSHKIN_PAGES = ["http://lib.ru/LITRA/PUSHKIN/p2.txt",
                 "http://lib.ru/LITRA/PUSHKIN/p3.txt",
                 "http://lib.ru/LITRA/PUSHKIN/p4.txt",
                 "http://lib.ru/LITRA/PUSHKIN/balda.txt",
                 "http://lib.ru/LITRA/PUSHKIN/saltan.txt",
                 "http://lib.ru/LITRA/PUSHKIN/zhenih.txt",
                 "http://lib.ru/LITRA/PUSHKIN/carewna.txt",
                 "http://lib.ru/LITRA/PUSHKIN/stihi.txt",
                 "http://lib.ru/LITRA/PUSHKIN/and.txt"]

LERMONTOV_PAGES = ["http://lib.ru/LITRA/LERMONTOW/l1.txt",
                   "http://lib.ru/LITRA/LERMONTOW/pss1.txt",
                   "http://lib.ru/LITRA/LERMONTOW/pss2.txt"
                   "http://lib.ru/LITRA/LERMONTOW/ispoved.txt"
                   "http://lib.ru/LITRA/LERMONTOW/julio.txt"
                   "http://lib.ru/LITRA/LERMONTOW/plennik.txt"
                   "http://lib.ru/LITRA/LERMONTOW/Korsar.txt"
                   "http://lib.ru/LITRA/LERMONTOW/kalashnikow.txt"
                   "http://lib.ru/LITRA/LERMONTOW/mcyri.txt"
                   "http://lib.ru/LITRA/LERMONTOW/demon.txt"
                   "http://lib.ru/LITRA/LERMONTOW/orsha.txt"
                   "http://lib.ru/LITRA/LERMONTOW/ispancy.txt"]


def get_author_pages_list():
    """
    All major poetry authors
    :return:
    """
    url = "http://lib.ru/POEZIQ/"
    poetry_page = requests.get(url)
    soup = BeautifulSoup(poetry_page.content, 'lxml')
    all_refs = []
    # Manually selected values
    start_index, end_index = 28, 321
    for current_a in soup.find_all('a')[start_index:end_index]:
        if "href" in current_a.attrs:
            ref = current_a.attrs["href"]
            # Some links don't have http://lib.ru in the begining
            # added manually for later processing
            if not ref.startswith("http"):
                ref = url + ref
            all_refs.append(ref)
    # Some authors are hosted on lib.ru and easy to process
    lib_ru_pages = [elem for elem in all_refs if elem.startswith("http://lib.ru")]
    # Other authors have separate pages which are harder to parse
    other_author_pages = [elem for elem in all_refs if not elem.startswith("http://lib.ru")]
    return lib_ru_pages, other_author_pages


def extract_book_pages(author_page_url):
    """
    Extracts all books url from author page
    """
    page = requests.get(author_page_url)
    if page.status_code != 200:
        raise ValueError(f"Failed load page {author_page_url}")
    soup = BeautifulSoup(page.content, 'lxml')
    results = []
    for elem in soup.find_all("a"):
        if "href" in elem.attrs and elem.attrs["href"].endswith("txt"):
            results.append((elem.b.text, author_page_url + elem.attrs["href"]))
    return results


def process_author_page(author_page_url):
    book_pages = extract_book_pages(author_page_url)
    res = []
    for elem in book_pages:
        res.append((elem[0], process_poems_page(elem[1])))
        # Sleep to dodge a ban for frequent requests
        time.sleep(10)
    return res


def extract_text(block):
    """
    Text are located one by one with name "ul"
    here we just iterate over sibling blocks
    """
    block = block.next_sibling
    # Sometimes we cannot obtain data at all
    if block is None:
        return None
    res = []
    while (block is not None) and (isinstance(block, BeautifulSoup.element.NavigableString) or (block.name != "ul")):
        if isinstance(block, BeautifulSoup.element.NavigableString):
            res.append(str(block))
        block = block.next_sibling
    return "".join(res)


def process_poems_page(url):
    """
    Searches for text blocks and pass them to extract_text function
    """
    page = requests.get(url)
    if page.status_code != 200:
        raise ValueError(f"Failed to load page {url}")
    soup = BeautifulSoup(page.content, "lxml")
    all_records = soup.find_all("ul")
    all_poems = []
    for record in all_records:
        # Take title from page if it possible
        if record.h2 is not None:
            title = record.h2.text
        else:
            title = ""
        text = extract_text(record)
        text = post_process_text(text)
        if text:
            all_poems.append((title, text))
    return all_poems


def crawl_poetry():
    author_pages = get_author_pages_list()
    poetry_authors = [process_author_page(author_page) for author_page in author_pages]
    pushkin_pages = [(url, process_poems_page(url)) for url in PUSHKIN_PAGES]
    lermontov_pages = [(url, process_poems_page(url)) for url in LERMONTOV_PAGES]
    poetry_authors.extend([pushkin_pages, lermontov_pages])
    return poetry_authors


def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


def post_process_text(text):
    """
    Post process texts. Removing non cyrrilic, empty lines
    Remove phrases not connecting to poetry text
    """

    text = text.split("\n\n")
    new_lines = []
    for elem in text:
        lines = elem.lstrip().split('\n')
        if len(lines) > 1:
            block = []
            for line in lines:
                line = line.lower()
                if not has_cyrillic(line):
                    continue
                if not (line.lstrip().startswith("Перевод") or line.lstrip().startswith("перевод") or line.lstrip().startswith("(фрагмент)")):
                    block.append(line.lstrip())
            new_lines.append("\n".join(block))
    return "\n\n".join(new_lines)


def save_data(data, data_location):
    with open(data_location, "w") as data_file:
        json.dump(data, data_file)


def main():
    data = crawl_poetry()
    save_data(data, sys.argv[1])


if __name__ == '__main__':
    main()
