from os import listdir,path,makedirs
from json import dump
from csv import reader
from datetime import datetime

class JournalManager:

    root="/var/www/html/projet2018/data/clean/robot/"

    def __init__(self,_journal,_file_target,_sources):
        self._journal=_journal
        self._file_target=_file_target
        self._sources=_sources

    def already_exists(self,article):
        """create a test to see if the article entered already exists
        Arguments:
            article
        Returns:
            boolean -- False: Doesn't exist | True: Does exist
        """
        with open("hash_text.csv", "r") as f:
            csv_reader = reader(f, delimiter=",")
            already_existing_hash = csv_reader.__next__()[:-1]
        return article.id_art in already_existing_hash

    def add_to_index(self,article):
        with open("hash_text.csv", "a") as f:
            f.write(article.id_art + ",")

    def create_json(self,new=True):
        if not path.exists(self.file_target+self.sources):
            makedirs(self.file_target+self.sources)
            ii = 1
        else:
            list_file = listdir(self.file_target+self.sources)
            last_file = list_file[-1]
            delimiter = last_file.split("_")
            ii = int(delimiter[2]) + 1
        cur_date = datetime.now().date()
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
                    dump(article.to_json(), fic, ensure_ascii=False)

                ii += 1

    def _get_journal(self):
        return self._journal

    def _set_journal(self,_journal):
        self._journal=_journal

    def _get_file_target(self):
        return self._file_target

    def _set_file_target(self,_file_target):
        self._file_target=_file_target   

    def _get_sources(self):
        return self._sources

    def _set_sources(self,_sources):
        self._sources=_sources   

    journal=property(_get_journal,_set_journal)
    file_target=property(_get_file_target,_set_file_target)
    sources=property(_get_sources,_set_sources)