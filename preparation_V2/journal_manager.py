import os
import json
import csv
import datetime as date

class JournalManager:

    root="/var/www/html/projet2018/data/clean/robot/"

    def __init__(self,journal,file_target,sources):
        self.journal=journal
        self.file_target=file_target
        self.sources=sources

    def already_exists(self,article):
        """create a test to see if the article entered already exists
        Arguments:
            article
        Returns:
            boolean -- False: Doesn't exist | True: Does exist
        """
        with open("hash_text.csv", "r") as f:
            csv_reader = csv.reader(f, delimiter=",")
            already_existing_hash = csv_reader.__next__()[:-1]
        return article.id_art in already_existing_hash

    def add_to_index(self,article):
        with open("hash_text.csv", "a") as f:
            f.write(article.id_art + ",")

    def create_json(self,new=True):
        """
        Entree:
            new:boolean
        Exit:
            one json file per item

        For each article, the function creates a json file named after it:
            art_abreviation_numeroArticle_datejour_robot. json.
        It places the json file in the folder corresponding to the journal
        if it exists otherwise it creates it.
        """
        if not os.path.exists(self.file_target+self.sources):
            os.makedirs(self.file_target+self.sources)
            ii = 1
        else:
            list_file = os.listdir(self.file_target+self.sources)
            last_file = list_file[-1]
            delimiter = last_file.split("_")
            ii = int(delimiter[2]) + 1
        cur_date = date.datetime.now().date()
        list_article= self.journal.find_list_article(new)
        for article in list_article:
            if not self.already_exists(article):
                self.add_to_index(article)
                if "/" in self.sources:
                    file_art = self.file_target + self.sources + "art_" + self.journal.abbreviation + "_"\
                        + str(ii) + "_" + str(cur_date) + "_robot.json"
                else:
                    file_art = self.file_target + self.sources + "/" + "art_" + self.journal.abbreviation\
                    + "_" + str(ii) + "_" + str(cur_date) + "_robot.json"
                with open(file_art, "w", encoding="UTF-8") as fic:
                    json.dump(article.to_json(), fic, ensure_ascii=False)

                ii += 1
