import urllib.request
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import time
import json
import requests

valid_urls = ["velho_wiki.html"]

json_to_dump = []
not_found = []
batch_counter = 0
error_counter = 0

for page in valid_urls:
    with open(page, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
        print("file loaded!")

    raw_elements = []
    for element in soup.find_all("ol"):
        raw_elements.append(element.get_text())

    print(soup.get_text())


