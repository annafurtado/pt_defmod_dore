from bs4 import BeautifulSoup
import time
import json
import requests


# 1. Load scrapelist
with open("scrape_list.txt", "r", encoding="utf-8") as txt_file:
    wordlist = txt_file.readlines()

# 2. Remove skip lines and whitespaces to serve as input to url
cleaned_items = []
for item in wordlist:
    new_item = item.strip("\n")
    if " " in new_item:
        n_item = item.replace(" ", "_")
        cleaned_items.append(n_item)
    else:
        cleaned_items.append(new_item)
scrape_items = set(cleaned_items)

test_list = ["chocolate", "ter_a_faca_e_o_queijo_na_mão", "errro", "aventura"]

list_of_urls = []
for word in scrape_items:
    url = "https://pt.wiktionary.org/wiki/{}".format(word)
    list_of_urls.append(url)

# Going live
json_to_dump = []
not_found = []

for page in list_of_urls:
    try:
        r = requests.get(page)
        soup = BeautifulSoup(r.content, "html.parser")
        print("I got it!")
        raw_elements = []
        for element in soup.find_all("ol"):
            raw_elements.append(element.get_text())

        preprocessed = {
            "lemma": "",
            "gloss": []
        }

        for element in raw_elements:
            if "\n" in element:
                new_el = element.split("\n")
                preprocessed["gloss"] = new_el
            else:
                preprocessed["gloss"] = new_el
 
        title = soup.find("title")
        new_title = str(title)
        processed = new_title.strip("\n").strip("<title>").removesuffix(" - Wikcionário</")
        preprocessed["lemma"] = processed
        json_to_dump.append(preprocessed)
    except HTTPError:
        not_found.append(not_found)
        print("This page was not found: ", page)
        continue

    time.sleep(20)

print(json_to_dump)
print(not_found)

batch_counter = 0
for item in json_to_dump:
    while len(json_to_dump) > 0:
        batch_counter += 1
        print("I came back here: ", len(json_to_dump))
        if len(json_to_dump) // 100:
            batch_of_items = json_to_dump[:100]
            with open("gloss_batches/glosses_batch_{}.json".format(batch_counter), "w", encoding="utf-8") as new_file:
                json.dump(batch_of_items, new_file)
            del json_to_dump[:100]
            print("File {} processed".format(batch_counter))
            print("There are still: ", len(json_to_dump))
        else:
            print("I have ", len(json_to_dump), "json objects. I will generate only one file.")
            stop = len(json_to_dump)
            with open("gloss_batches/glosses_batch_{}.json".format(batch_counter), "w", encoding="utf-8") as new_file:
                json.dump(json_to_dump, new_file)
            del json_to_dump[:stop]

"""
Testing locally:
url_list = ["cachorro_wiki.html", "queijo_wiki.html"]

for url in url_list:
    with open(url, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
        print("file loaded!")

"""