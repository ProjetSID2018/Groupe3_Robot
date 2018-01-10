# -*- coding: utf-8 -*-
# Groupe 4
# Céline
import os
import json
import datetime as date

# Entree :
#   file_target : chaine de caractere contenant le  chemin du dossier
#   sources : chaine de caractere contenant nom du dossier
#   list_article : liste contenant les nouveaux articles
#   abbreviation : chaine de caractere contenant l'abréviation du journal
# Sortie :
#   un fichier json par article
# Pour chaque article, la fonction crée un fichier json qui a pour nom :
#   art_abreviation_numeroArticle_datejour_robot.json.
# Elle le place dans le dossier correspondant au nom du journal,
# s'il n'existe pas elle le crée


def create_json(file_target, list_article, sources, abbreviation):
    cur_date = date.datetime.now().date()
    if not os.path.exists(file_target+sources):
        os.makedirs(file_target+sources)
    i = 1
    # Chaque article est exporté en format json et nommé de la forme suivante :
    # art_lg_numero_datejour_robot.json
    for article in list_article:
        file_art = file_target + sources + "art_" + abbreviation + "_"\
            + i + "_" + str(cur_date) + "_robot.json"
        with open(file_art, "w", encoding="UTF-8") as fic:
            json.dump(article, fic, ensure_ascii=False)
        i += 1
