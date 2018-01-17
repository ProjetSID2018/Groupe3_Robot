# Group 4
# DELOEUVRE Noémie

import os
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
import g4_utils_v32 as utils

# Path to modify : target where we will store the json files
fileTarget = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Projet_inter_promo/"

list_category = ["Beaute/Coiffure", "Beaute/Beaute-People", "Beaute/Parfums",
                 "Beaute/Soins-visage-et-corps", "Beaute/Maquillage",
                 "Mode/Tendances", "Mode/Defiles", "Mode/Lingerie",
                 "Mode/Mode-People", "Cuisine/Recettes",
                 "Cuisine/Recettes-de-chefs", "Cuisine/Shopping-et-conseils",
                 "Cuisine/Idees-de-recettes-par-theme", "Psychologie/Psycho",
                 "Psychologie/Societe", "Psychologie/Argent-Droit",
                 "People/Vie-des-people", "Culture/Series", "Culture/Musique",
                 "Culture/Cinema-et-DVD", "Culture/Sorties",
                 "Loisirs/Jardinage", "Loisirs/Voyages",
                 "Loisirs/Tendace-deco", "Sexo/Sexualite", "Sexo/Amour",
                 "Sante-Forme/Bien-etre", "Sante-Forme/Sport",
                 "Sante-Forme/Regimes-Nutrition", "Sante-Forme/Sante",
                 "Famille/Grossesse", "Famille/Bebe", "Famille/Enfant",
                 "Famille/Adolescent"]

file_json = []
for category in list_category:
    for i in range(2, 5):
        url_rss_fem = "http://www.femina.fr/" + category + "/page-" + str(i)
        req = requests.get(url_rss_fem)
        data = req.text
        soup_url = BeautifulSoup(data, "lxml")

        article_fem = []
        for h2 in soup_url.find_all('h2'):
            for a in h2.find_all('a'):
                article_fem.append(a.get("href"))
        for h3 in soup_url.find_all('h3'):
            for a in h3.find_all('a'):
                article_fem.append(a.get("href"))

        for article in article_fem:
            req = requests.get(article)
            data = req.text
            soup_article = BeautifulSoup(data, "lxml")
            title = soup_article.title.get_text()

            for div in soup_article.find_all('div'):
                if div.get("class") == ['infos']:
                    if div.has_attr("datetime"):
                        date_p = div.get("datetime")

            author = []
            for meta in soup_article.find_all('meta'):
                if meta.get("property") == 'article:author':
                    author.append(meta.get("content"))

            for link in soup_article.find_all('link'):
                if link.get("rel") == ['Index']:
                    link_theme = link.get("href")
                    part_link = link_theme.split("/")
                    theme = part_link[3]

            contents = ""
            for div in soup_article.find_all('div'):
                if div.get("class") == ['chapo']:
                    for p in div.find_all('p'):
                        contents += p.get_text() + " "
                if div.get("class") == ['contenu']:
                    for p in div.find_all('p'):
                        contents += p.get_text() + " "
                if div.get("class") == ['diaporama']:
                    for p in div.find_all('p'):
                        contents += p.get_text() + " "
            contents = re.sub(r"\s\s+", " ", contents)

            new_article = {
                "title": title,
                "newspaper": "Femina",
                "date_publi": date_p,
                "author": author,
                "theme": theme,
                "content": contents
            }
            file_json.append(new_article)

sources = "Femina_crawler/"
cur_date = date.datetime.now().date()

if not os.path.exists(fileTarget+sources):
    os.makedirs(fileTarget+sources)

# Call the create_json function
utils.create_json(fileTarget, file_json, sources, "fem")
