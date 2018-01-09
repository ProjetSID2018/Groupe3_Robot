# Groupe 4
# Réalisé par BENJEBRIA Sofian, DELOEUVRE Noémie, SEGUELA Morgan

import os
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re

# Chemin à modifier : cible où l'on va stocker les fichier json
fileTarget = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Projet_inter_promo/"

list_category = ["france/politique", "france/societe", "monde-libre",
                 "france/economie", "culture", "people", "sports", "hi-tech",
                 "sciences", "ledito"]

# On parcours tous les thèmes du site Le Gorafi et pour chaque thème on
# récupère les articles de 6 pages (120 articles par thème).
 
file_json = []
for cat in list_category:
    # On récupère les flux URL pour chaque page d'article.
    # Chaque article codé en HTML est analysé avec beautiful soup.
    for i in range(2, 8):
        url_rss_gorafi = "http://www.legorafi.fr/category/" + cat + "/page/" + str(i) + "/feed/"
        req = requests.get(url_rss_gorafi)
        data = req.text
        soup = BeautifulSoup(data, "lxml")
        items = soup.find_all("item")
        article_gorafi = []

        # On récupère tous les articles pour une page donnée
        for item in items:
            article_gorafi.append(re.search(r"<link/>(.*)", str(item))[1])

        # Récupération des variables nécessaires à la création du fichier json
        for article in article_gorafi:
            req = requests.get(article)
            data = req.text
            soup = BeautifulSoup(data, "lxml")
            balise_title = soup.title.get_text()
            sep = balise_title.split("—")
            title = sep[0]
            newspaper = sep[1]
            author = []

            # Récupération de l'auteur et de la date de publication
            for span in soup.find_all('span'):
                if span.get("class") == ['context']:
                    author.append(span.a.get_text())
                    for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', str(span)):
                        date_p = valeur.group(0)

            # Récupération du thème
            for ul in soup.find_all('ul'):
                if ul.get("class") == ['post-categories']:
                    for li in ul.find_all('li'):
                        theme = li.get_text()
            contents = ""

            # Récupération du contenu de l'article
            for div in soup.find_all('div'):
                if div.get("class") == ['content']:
                    for p in div.find_all('p'):
                        contents += p.get_text() + " "

            new_article = {
                    "title": title,
                    "newspaper": newspaper,
                    "author": author,
                    "date_publi": date_p,
                    "theme": theme,
                    "content": contents
            }
            file_json.append(new_article)

sources = "LeGorafi_articles/"
cur_date = date.datetime.now().date()

if not os.path.exists(fileTarget+sources):
    os.makedirs(fileTarget+sources)

i = 1
# Chaque article est exporté en format json et nommé de la forme suivante :
# art_lg_numero_datejour_robot.json
for article in file_json:
    file_art = fileTarget + sources + "art_lg_" + str(i) + "_" + str(cur_date) + "_robot.json"
    with open(file_art, "w", encoding="UTF-8") as fic:
        json.dump(article, fic, ensure_ascii=False)
    i += 1
