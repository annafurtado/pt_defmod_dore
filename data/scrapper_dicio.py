import csv
import requests
from bs4 import BeautifulSoup

wordlist = ["azul", "chocolate", "dormir"]
exclusion_list = ["substantivo", "adjetivo", "verbo", "advérbio", "etimologia", "artigo", "numeral", "pronome", "preposição", "conjunção", "interjeição"]
url_list = []


for item in wordlist:
    url = "https://www.dicio.com.br/{}/".format(item)
    url_list.append(url)
    requested_file = requests.get(url)

#try and except for a page that does not exist


with open(url, "r", encoding="utf-8") as html_file:
    soup = BeautifulSoup(html_file, "html.parser")
    print("file loaded!")

    #get the raw glosses
    raw_elements = []
    gloss = soup.find(itemprop="description")
    for element in soup.find(itemprop="description"):
        defi = element.get_text().lower()
        raw_elements.append(defi)

    #eliminate pos info
    for gloss in raw_elements:
        for element in exclusion_list:
            if element in gloss:
                raw_elements.remove(gloss)
            else:
                continue

    #get the lemma
    title = soup.find("title")
    new_title = str(title)
    lemma = new_title.strip().strip("<title>").removesuffix(" - Dicio, Dicionário Online de Português</").lower()

#prepare to write
writing_lemmas = []
for item in raw_elements:
    writing_lemmas.append(lemma)


#write the csv file
with open("pt.raw_glosses.csv", "w", newline="") as csv_file:
    field_names = ["lemma", "gloss"]
    writer = csv.writer(csv_file)
    writer.writerow(field_names)
    writer.writerow(zip(writing_lemmas, raw_elements))
    print("File Written")

