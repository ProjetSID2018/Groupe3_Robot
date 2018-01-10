# Groupe 4
# Réalisé par BENJEBRIA Sofian, DELOEUVRE Noémie, SEGUELA Morgan

import os
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re

# Chemin à modifier : cible où l'on va stocker les fichier json
file_target = "/var/www/html/projet2018/data/clean/robot/" + str(date.datetime.now().date()) +"/"
os.makedirs(file_target, exist_ok=True)

url_rss_gorafi = "http://www.legorafi.fr/feed/"

# On récupère les flux URL pour chaque nouvel article
# Chaque article codé en HTML est analysé avec beautiful soup.
req = requests.get(url_rss_gorafi)
data = req.text
soup = BeautifulSoup(data, "lxml")
items = soup.find_all("item")
article_gorafi = []

# On récupère tous les nouveaux articles dans une liste
for item in items:
    article_gorafi.append(re.search(r"<link/>(.*)", str(item))[1])
file_json = []

for article in article_gorafi:
    req = requests.get(article)
    data = req.text

    soup = BeautifulSoup(data, "lxml")

    balise_title = soup.title.string
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

sources = "legorafi"
cur_date = date.datetime.now().date()

if not os.path.exists(file_target+sources):
    os.makedirs(file_target+sources)

i = 1
# Chaque article est exporté en format json et nommé de la forme suivante :
# art_lg_numero_datejour_robot.json
for article in file_json:
    file_art = file_target + sources + "art_lg_" + str(i) + "_" + str(cur_date) + "_robot.json"
    with open(file_art, "w", encoding="UTF-8") as fic:
        json.dump(article, fic, ensure_ascii=False)
    i += 1
