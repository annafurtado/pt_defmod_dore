import urllib.request
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import time
import json
import requests


# 1. Load scrapelist
with open("updated_wordlist.txt", "r", encoding="utf-8") as txt_file:
    wordlist = txt_file.readlines()
print("The scrape list has been loaded.")

# 2. Remove skip lines and whitespaces to serve as input to url
cleaned_items = []
for item in wordlist:
    new_item = item.strip("\n")
    if " " in new_item:
        n_item = new_item.replace(" ", "_")
        cleaned_items.append(n_item)
    else:
        cleaned_items.append(new_item)

# 3. Count the amount of items in the wordlist and batch them if necessary
scrape_items = []
letter = input("Give me one letter to scrape: ").lower()
for word in cleaned_items:
    if word.startswith(letter):
        scrape_items.append(word)
print("We have loaded ", len(scrape_items), " items to scrape.")
# $$$$ CHANGE HERE TO DEFINE THE BATCH SIZE $$$$
edit_item = scrape_items[0:4000]

# 4. Create URLs for list of lemmas
list_of_urls = []
for word in edit_item:
    url = "https://pt.wiktionary.org/wiki/{}".format(word)
    list_of_urls.append(url)

# 5. Catch URLs that do not work
print("I am now verifying which URLs are not valid. This may take some time.")
valid_urls = []
for url in list_of_urls:
    try:
        connection = requests.head(url)
        print(connection, url)
        if connection.status_code == 404 or connection.status_code == 301:
            pass
        else:
            valid_urls.append(url)
    except:
        pass

print("We will scrape ", len(valid_urls), "items. We discarded ", (len(edit_item) - (len(valid_urls))), " items.")

# Going live
json_to_dump = []
not_found = []
batch_counter = 0
error_counter = 0

print("I will now start scrapping.")
# 6. Start the scrapping loop
for page in valid_urls:
    try:
        # get the page
        r = requests.get(page)
        soup = BeautifulSoup(r.content, "html.parser")
        print("I got the page!")

        # Find lists of definitions
        raw_elements = []
        for element in soup.find_all("ol"):
            raw_elements.append(element.get_text())

        # create the dicts containers
        preprocessed = {
            "lemma": "",
            "gloss": []
        }

        # put the definitions into the dicts
        for element in raw_elements:
            if "\n" in element:
                new_el = element.split("\n")
                preprocessed["gloss"] = new_el
            else:
                preprocessed["gloss"] = element

        # get the lemma
        title = soup.find("title")
        new_title = str(title)
        processed = new_title.strip("\n").strip("<title>").removesuffix(" - Wikcionário</")
        preprocessed["lemma"] = processed
        json_to_dump.append(preprocessed)

        time.sleep(12)

        # waits to dump file :)
        if len(json_to_dump) == 100:
            for item in json_to_dump:
                while len(json_to_dump) > 0:
                    batch_counter += 1
                    print("I came back here: ", len(json_to_dump))
                    if len(json_to_dump) // 100:
                        batch_of_items = json_to_dump[:100]
                        with open("gloss_batches/gloss_batch_{}_{}.json".format(letter, batch_counter), "w",
                                  encoding="utf-8") as new_file:
                            json.dump(batch_of_items, new_file, ensure_ascii=False)
                        del json_to_dump[:100]
                        print("File {} processed".format(batch_counter))
                        print("There are still: ", len(json_to_dump))
        else:
            continue

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

while len(json_to_dump) > 1:
    if len(json_to_dump) > 1:
        batch_counter += 1
        batch_of_items = json_to_dump[:100]
        for item in json_to_dump:
            print("I will dump the remainder json objects.")
            with open("gloss_batches/gloss_batch_{}_{}.json".format(letter, batch_counter), "w") as new_file:
                json.dump(json_to_dump, new_file, ensure_ascii=False)
            del json_to_dump[:100]
            print("I have dumped", len(json_to_dump), "objects.")

print("I will now write error reports if necessary.")

# Write reports
if len(not_found) > 0:
    with open("error_report.txt", "w") as error_file:
        for error in not_found:
            error_file.write(error)
            error_file.write("\n")
        else:
            print("no error found!")

print("I am done! I processed {} objects.".format(len(valid_urls)))