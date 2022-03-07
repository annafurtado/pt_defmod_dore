# !/usr/bin/python
# -*- coding: utf-8 -*-

import json
import codecs
import ast
import glob

# extract objects from a Wiktionary Dump
class WikData:

    def __init__(self, file_path):
        """
        :param file_path: takes a file path given by the user
        - extracts a topic_list and a lemma_list and zip them into processed_items
        """
        self.file_path = file_path
        self.topic_list = []
        self.lemma_list = []
        self.processed_items = []

        self.clean_wik_dump()

    def clean_wik_dump(self):
        """
        :return: a list of tuples [(lemma, [domain]), ...]
        """
        processed_file_dir = glob.glob(self.file_path, recursive=True)
        print("Your file was processed :) ")

        for file in processed_file_dir:
            with codecs.open(file, "r", encoding="us-ascii") as json_file:
                for line in json_file:
                    d = ast.literal_eval(line.strip())
                    if "word" in d.keys():
                        self.lemma_list.append(d["word"])
                    for item in d["senses"]:
                        print("Found senses")
                        if "categories" in item.keys():
                            print("found category")
                            for things in item["categories"]:
                                self.topic_list.append(things.get("parents"))
        self.processed_items = list(zip(self.lemma_list, self.topic_list))
        return self.processed_items

# create the dataset container for the json_objects
class JSONDataset:
    """
    Transform wordlists and previously processed items into json_objects
    and format them in a JSON dataset
    ----> THIS CLASS SHOULD INHERIT processed_items from the previous class
    """

    def __init__(self, list_of_items):
        """
        :param takes a list of tuples [(lemma, [domain]), ...]
        """
        self.id_number = 0
        self.json_to_dump = []
        self.list_of_items = list_of_items
        self.id_list = []

        self.id_maker()

    def id_maker(self):
        """
        Assign an ID to each lemma
        :return: a list of ids (the order does not matter at this point).
        """
        for pair in self.list_of_items:
            self.id_number += 1
            label = "pt.defmod.{}".format(self.id_number)
            self.id_list.append(label)
        return self.id_list

    def add_new_lemmas(self, path_to_list):
        """
        add new lemmas from given wordlists
        :param path_to_list: the location of the lemmas to be added
        :return: a list of new words to be added into the batches
        """
        words_to_add = glob.glob(path_to_list, recursive=True)

        for w_lists in words_to_add:
            with open(list, "r") as wordlist_file:
                wordlist = wordlist_file.readlines()

        words_to_add = []
        for pair in self.list_of_items:
            for lemma in wordlist:
                if lemma not in pair:
                    print("Ops, I don't have this here!")
                    words_to_add.append(lemma)
                else:
                    continue

        #make a for loop that will add the new words into the processed_items list and return the list

    def produce_json_objects(self, vector_list):
        """
        :param vector_list: receives a list of [(lemma, [vectors])]
        - inherits id_num, lemmas, glosses and domain from other functions/classes
        :return: json objects that will be dumped in a JSON dataset
        """
        # $$$$ EDIT THIS = inherit each list from previous classes/functions
        # zip them into a dict
        items_to_dump = (list(zip(id_num, lemma, gloss, domain, vectors))

        for item in items_to_dump:
            json_dict = {}
            json_dict["id"] = item[0]
            json_dict["lemma"] = item[1]
            json_dict["gloss"] = item[2]
            json_dict["domain"] = item[3]
            json_dict["vectors"] = item[4]
            self.json_to_dump.append(json_dict)

        return self.json_to_dump

    def create_batch_files(self):
        """
        takes the list of json_objs to dump and divide them into batches of 100 definitions
        sorted in alphabetical order
        :return: files
        """
        sorted_items = sorted(self.json_to_dump, key= lambda d: d["lemma"])

        batch_counter = 0
        for item in sorted_items:
            if len(items) / 100:
                batch_counter += 1
                batch_of_items = sorted_items[:100]
                with open("data_batches/defmod_batch_{}.json".format(batch_counter), "w") as new_file:
                    json.dump(batch_of_items, new_file)
                del sorted_items[:100]
                print("File {} processed".format(batch_counter))
            else:
                continue


# instantiate the classes to make it run
start_data_cleaner = WikData("testing/*")

# just for testing
my_list = [('acanto', ['Lamiales order plants', 'List of sets', 'Plants', 'Shrubs', 'Trees', 'All sets', 'Lifeforms', 'Fundamental', 'Nature', 'All topics']), ('afelandra', ['Lamiales order plants', 'List of sets', 'Plants', 'Shrubs', 'Trees', 'All sets', 'Lifeforms', 'Fundamental', 'Nature', 'All topics']), ('branca ursina', ['Lamiales order plants', 'List of sets', 'Plants', 'Shrubs', 'Trees', 'All sets', 'Lifeforms', 'Fundamental', 'Nature', 'All topics']), ('siribeira', ['Lamiales order plants', 'List of sets', 'Plants', 'Shrubs', 'Trees', 'All sets', 'Lifeforms', 'Fundamental', 'Nature', 'All topics']), ('mangue-preto', ['Lamiales order plants', 'List of sets', 'Plants', 'Shrubs', 'Trees', 'All sets', 'Lifeforms', 'Fundamental', 'Nature', 'All topics']), ('acanto espinhoso', ['Lamiales order plants', 'List of sets', 'Plants', 'Shrubs', 'Trees', 'All sets', 'Lifeforms', 'Fundamental', 'Nature', 'All topics']), ('asistásia', ['Lamiales order plants', 'List of sets', 'Plants', 'Shrubs', 'Trees', 'All sets', 'Lifeforms', 'Fundamental', 'Nature', 'All topics']), ('tumbérgia', ['Lamiales order plants', 'List of sets', 'Plants', 'Shrubs', 'Trees', 'All sets', 'Lifeforms', 'Fundamental', 'Nature', 'All topics']), ('erva gigante', ['Lamiales order plants', 'List of sets', 'Plants', 'Shrubs', 'Trees', 'All sets', 'Lifeforms', 'Fundamental', 'Nature', 'All topics']), ('margarida-amarela', ['Lamiales order plants', 'List of sets', 'Plants', 'Shrubs', 'Trees', 'All sets', 'Lifeforms', 'Fundamental', 'Nature', 'All topics']), ('siriúba', ['Lamiales order plants', 'List of sets', 'Plants', 'Shrubs', 'Trees', 'All sets', 'Lifeforms', 'Fundamental', 'Nature', 'All topics']), ('tumbérgia-azul', ['Lamiales order plants', 'List of sets', 'Plants', 'Shrubs', 'Trees', 'All sets', 'Lifeforms', 'Fundamental', 'Nature', 'All topics'])]






