import urllib.request
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import time
import json
import requests
import re
import random


exclusion_list = ["substantivo", "adjetivo", "verbo", "advérbio", "etimologia", "artigo", "numeral", "pronome",
                  "preposição", "conjunção", "interjeição"]

# 1. Load the wordlist file
with open("missing_items.txt", "r", encoding="utf-8") as txt_file:
    wordlist = txt_file.readlines()
print("The scrapelist has been loaded.")

# 2. Remove skip lines and whitespaces to serve as input to url
cleaned_items = []
for item in wordlist:
    new_item = item.strip("\n")
    if " " in new_item:
        n_item = new_item.replace(" ", "_")
        cleaned_items.append(n_item)
    else:
        cleaned_items.append(new_item)

# 3. Make scraping batches
scrape_items = []
letter = input("Give me one letter to scrape: ").lower()
for word in cleaned_items:
    if word.startswith(letter):
        scrape_items.append(word)
print("We have loaded ", len(scrape_items), " items to scrape.")
# $$$$ CHANGE HERE TO DEFINE THE BATCH SIZE $$$$
edit_item = scrape_items[0:4000]


# 4. Prepare wordlist to become URLs
def url_maker(word_list):
    """
    #:param word_list: takes raw wordlist from a file
    #-> preprocesses the words
    #:return: a url list ready to be checked
"""
    cleaned_list = []
    for word in word_list:
        n_1 = word.strip("\n")
        n_2 = n_1.replace(" ", "_")
        n_3 = n_2.replace("ã", "a")
        n_4 = n_3.replace("à", "a")
        n_5 = n_4.replace("á", "a")
        n_6 = n_5.replace("â", "a")
        n_7 = n_6.replace("é", "e")
        n_8 = n_7.replace("ê", "e")
        n_9 = n_8.replace("í", "i")
        n_10 = n_9.replace("ó", "o")
        n_11 = n_10.replace("ô", "o")
        n_12 = n_11.replace("õ", "o")
        n_13 = n_12.replace("ö", "o")
        n_14 = n_13.replace("ú", "u")
        n_15 = n_14.replace("û", "u")
        n_16 = n_15.replace("ü", "u")
        n_17 = n_16.replace("ç", "c")
        cleaned_list.append(n_17)

    url_list = []
    for item in cleaned_list:
        url = "https://www.dicio.com.br/{}/".format(item)
        url_list.append(url)
    return url_list


list_of_urls = url_maker(edit_item)
print("I'll now check which URLs are valid.")

# 5. Validate URLs
valid_urls = []
for url in list_of_urls:
    try:
        connection = requests.head(url)
        print(connection.status_code, url)
        if connection.status_code == 404 or connection.status_code == 301:
            pass
        else:
            valid_urls.append(url)
    except:
        pass

print("We will scrape ", len(valid_urls), "items. We discarded ", (len(scrape_items) - (len(valid_urls))), " items.")

# Setting the stage to go live
json_to_dump = []
not_found = []
batch_counter = 0
error_counter = 0
n = 0

# 6. Start scrapping
for page in list_of_urls:
    try:
        r = requests.get(page)
        soup = BeautifulSoup(r.content, "html.parser")
        print("I got the page!")

        r_num = random.randint(10, 15)

        # get the raw glosses
        print("I will now extract the entries, if any.")
        text = str(soup.find_all(class_="significado textonovo"))
        n_1 = text.split("</span>")
        n_1.pop(0)

        # deep cleaning steps.
        l = []
        for item in n_1:
            n_2 = re.sub(r"\s*<\/*\w*\d*\s*>\]*", "", item)
            n_3 = re.sub(r"(<.*>)", "", n_2)
            n_4 = n_3.lower()
            l.append(n_4)

        l_1 = list(filter(None, l))

        for word in exclusion_list:
            for item in l_1:
                if word in item:
                    l_1.remove(item)

        mwe = []
        processed = []
        for item in l_1:
            counter = 0
            if "[" in item:
                counter += 1
                tag = item
                ref = l_1.index(item)
                w = tag + l_1[ref + 1]
                processed.append(w)
                l_1.pop(ref)
            elif "expressão" == item:
                tag = "(expressão) "
                ref = l_1.index(item)
                w = tag + l_1[ref + 1]
                mwe.append(w)
                l_1.pop(ref + 1)
                l_1.pop(ref)
            else:
                n_1 = item.strip()
                processed.append(n_1)

        exp = []
        for item in mwe:
            new = tuple(item.split(". "))
            exp.append(n)

        # get the lemma
        title = soup.find("title")
        new_title = str(title)
        lemma = new_title.strip().strip("<title>").removesuffix(" - Dicio, Dicionário Online de Português</").lower()

        n += 1

        # create the dicts for single word definitions
        for gloss in processed:
            new_dict = {}
            new_dict["lemma"] = lemma
            new_dict["gloss"] = gloss
            json_to_dump.append(new_dict)

        # create dicts for mwes
        for tuples in exp:
            new_dict = {}
            new_dict["lemma"] = tuples[0]
            new_dict["gloss"] = tuples[1]
            json_to_dump.append(new_dict)

        print(n, "I have now", len(json_to_dump), "defs", page)
        time.sleep(r_num)

        # waits to dump file :)
        if len(json_to_dump) >= 100:
            for item in json_to_dump:
                print("I have", len(json_to_dump), "definitions")
                if len(json_to_dump) // 100:
                    batch_counter += 1
                    batch_of_items = json_to_dump[:100]
                    with open("gloss_batches/gloss_batch_{}_{}.json".format(letter, batch_counter),
                                  "w", encoding="utf8") as new_file:
                        json.dump(batch_of_items, new_file, ensure_ascii=False)
                    del json_to_dump[:100]
                    print("<--------- $$$$ --------> ")
                    print("File {} processed".format(batch_counter))
                    print("There are still: ", len(json_to_dump))

    except IndexError:
        print("This page got me an error: ", page)
        not_found.append(page)
        pass

    except TypeError:
        print("This page got me an error: ", page)
        not_found.append(page)
        pass

    except requests.ConnectTimeout:
        not_found.append(page)
        print("This page had a problem: ", page)
        time.sleep(200)
        pass

    except requests.HTTPError:
        not_found.append(page)
        print("This page was not found: ", page)
        pass

    finally:
        print("I'm done. Proceeding to the next.")

print("I still have: ", json_to_dump)
if len(json_to_dump) > 1:
    batch_counter += 1
    stop = len(json_to_dump)
    for item in json_to_dump:
        print("I will dump the remainder json objects.")
        with open("gloss_batches/gloss_batch_{}_{}.json".format(letter, batch_counter), "w",
                  encoding="utf8") as new_file:
            json.dump(json_to_dump, new_file, ensure_ascii=False)
        del json_to_dump[:stop]
        print("I have dumped the remainder objects.")

# Write reports
print("I will now write error reports if necessary.")
if len(not_found) > 0:
    with open("error_report_{}.txt".format(letter), "w") as error_file:
        for error in not_found:
            error_file.write(error)
            error_file.write("\n")

print("If errors were found, they are found in a file.")

print("I am done! I processed {} objects.".format(len(valid_urls)))
