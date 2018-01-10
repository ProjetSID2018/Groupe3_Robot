# -*- coding: utf-8 -*-
# Groupe 4
# DELOEUVRE Noémie
# Céline MOTHES
# Morgan SEGUELA

import os
import json
import datetime as date

# Entree:
#   file_target: string containing the path of the folder
#   sources: string containing folder name
#   list_article: list containing new articles
#   abbreviation:string containing the journal abbreviation
# Exit:
#   one json file per item
# For each article, the function creates a json file named after it:
# art_abreviation_numeroArticle_datejour_robot. json.
# It places the json file in the folder corresponding to the journal
# if it exists otherwise it creates it.


def create_json(file_target, list_article, sources, abbreviation):
    if not os.path.exists(file_target+sources):
        os.makedirs(file_target+sources)
    i = 1
    cur_date = date.datetime.now().date()
    for article in list_article:
        file_art = file_target + sources + "art_" + abbreviation + "_"\
            + str(i) + "_" + str(cur_date) + "_robot.json"
        with open(file_art, "w", encoding="UTF-8") as fic:
            json.dump(article, fic, ensure_ascii=False)
        i += 1
