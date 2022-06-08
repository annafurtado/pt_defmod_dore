import urllib.request
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import time
import json
import requests
import re


exclusion_list = ["substantivo", "adjetivo", "verbo", "advérbio", "etimologia", "artigo", "numeral", "pronome",
                  "preposição", "conjunção", "interjeição", "etimologia"]

valid_urls = ["festa_dicio.html", "cachorro_dicio.html", "jaca.html", "pao-duro.html", "queijo_dicio.html",
              "cabeca_dicio.html"]

json_to_dump = []
not_found = []
batch_counter = 0
error_counter = 0

for page in valid_urls:
    with open(page, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
        print("file loaded!")

    print("I will now extract the entries.")
    raw_elements = []
    text = str(soup.find_all(class_="significado textonovo"))
    for element in text:
        n_1 = text.split("</span>")
        n_1.pop(0)
        raw_elements.append(n_1)

    # deep cleaning steps.
    l = []
    for item in raw_elements:
        n_2 = re.sub(r"\s*<\/*\w*\d*\s*>\]*", "", item)
        n_3 = re.sub(r"(<.*>)", "", n_2)
        n_4 = n_3.lower()
        l.append(n_4)

    l_1 = list(filter(None, l))

    for word in exclusion_list:
        for item in l_1:
            if word in item:
                l_1.remove(item)

    print(l_1)

    mwe = []
    processed = []
    for item in l_1:
        counter = 0
        if "[" in item:
            counter += 1
            tag = item
            ref = l_1.index(item)
            w = tag + l_1[ref+1]
            processed.append(w)
            l_1.pop(ref)
        elif "expressão" == item:
            tag = "(expressão) "
            ref = l_1.index(item)
            w = tag + l_1[ref+1]
            mwe.append(w)
            l_1.pop(ref+1)
            l_1.pop(ref)
        else:
            n_1 = item.strip()
            processed.append(n_1)
    exp = []
    for item in mwe:
        n = tuple(item.split(". "))
        exp.append(n)

    for num, item in enumerate(exp):
        print(num, item)
    """
    # "expressão" indicates MWEs embedded inside an entry of a lexical item.
    # we have to add a tag in order to separate these elements in the processing
    for item in l_1:
        if "expressão" in item:
            ref = l_1.index(item)  # the position of "expressão" in the list
            end = len(l_1)  # how many items there are in the list
            i = end - ref - 1  # how many items should we iterate through
            tag = "(expressão) "  # the tag we have to add
            for n in range(i):
                w = tag + l_1[ref + i]  # we want to add expressão to the MWE
                l_1.pop(ref + i)  # and remove the one without it
                i -= 1  # go to the previous index
                l_1.append(w)  # add the new into our list

    for item in l_1:
        if item == "expressão":
            l_1.remove(item)
        elif "[" in item:
            tag = item
            ref = l_1.index(item)  # where the tag occurs
            counter = ref
            w = tag + l_1[counter + 1]  # add the tag into the next element
            counter += 1  # for as many tags we have
            x = ref + 1
            l_1.insert(x, w)  # add the new tag
            l_1.pop(ref + 2)  # removes the wrong one
            l_1.remove(item)

    for item in l_1:
        tag = "(expressão)"
        y = item.count(tag)
        if y > 1:
            x = y - 1
            i = l_1.index(item)
            w = item.replace(tag, "", x).strip()
            l_1.insert(i + 1, w)
            n_i = l_1.index(item)
            l_1.pop(i)

    # remove pos_tags from definitions
    for pos in exclusion_list:
        for item in l_1:
            if pos in item:
                l_1.remove(item)
    
    # separate MWEs for a new lemma
    exp = []
    for item in l_1:
        if "expressão" in item:
            n = item.replace(".", ".$")
            n_1 = tuple(n.split("$"))
            exp.append(n_1)
    """
    glosses = []
    for item in l_1:
        if "expressão" in item:
            continue
        else:
            glosses.append(item)

    for tuples in exp:
        for element in tuples:
            if element.isspace():
                del element
            elif element == "" or element == " ":
                del element

    # get the lemma
    title = soup.find("title")
    new_title = str(title)
    lemma = new_title.strip().strip("<title>").removesuffix(" - Dicio, Dicionário Online de Português</").lower()

    # create the dicts for single word definitions
    for gloss in glosses:
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

    print("Glosses have been extracted and are now stored in memory. I'll wait for the next")