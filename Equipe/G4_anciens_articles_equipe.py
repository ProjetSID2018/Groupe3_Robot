# Group 4
# Realized by DELOEUVRE Noémie

import datetime as date
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
import os
from G4_create_json import create_json

file_target = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Projet_inter_promo/"
os.makedirs(file_target, exist_ok=True)

list_category = ["Athletisme", "Aussi/Aviron", "Auto-moto", "Aussi/Badminton",
                 "Aussi/Baseball", "Basket", "Aussi/Biathlon", "Aussi/Boxe",
                 "Aussi/Canoe-kayak", "Cyclisme", "Aussi/Equitation",
                 "Aussi/Escrime", "Adrenaline/Escalade", "Football",
                 "Aussi/Football-americain", "Formule-1", "Golf",
                 "Aussi/Gymnastique", "Aussi/Halterophilie",
                 "Handball", "Hippisme", "Aussi/Hockey-sur-gazon",
                 "Aussi/Judo", "Natation", "Basket/NBA",
                 "Aussi/Pentathlon-moderne", "Rugby", "Sports-de-combat",
                 "Sports-us", "Aussi/Squash", "Adrenaline/Surf", "Tennis",
                 "Aussi/Tennis-de-table", "Aussi/Tir", "Aussi/Tir-a-l-arc",
                 "Aussi/Triathlon", "Aussi/Mma", "Voile", "Aussi/Volley-ball",
                 "Natation/Water-polo", "Aussi/Jeux-paralympiques"]

file_json = []
for cat in list_category:
    # We retrieve the URL feeds for each page of article
    # Each HTML-coded article is analyzed with beautiful soup
    url_rss_equipe = "https://www.lequipe.fr/" + cat + "/"
    req = requests.get(url_rss_equipe)
    data = req.text
    soup_url = BeautifulSoup(data, "lxml")

    article_equipe = []
    # We retrieve all the articles for a given page
    for div in soup_url.find_all('div'):
        if div.get("class") == ['home__colead__split']:
            new_article = "https://www.lequipe.fr" + div.a.get("href")
            article_equipe.append(new_article)

    for article in article_equipe:
        req = requests.get(article)
        data = req.text
        soup_article = BeautifulSoup(data, "lxml")
        # Retrieving of title
        balise_title = soup_article.title.string
        sep = balise_title.split("—")
        title = sep[0]

        # Retrieving of the author
        for meta in soup_article.find_all('meta'):
            if meta.get("name") == 'Author':
                author = meta.get("content")

        # Retrieving of date of publication
        for div in soup_article.find_all('div'):
            if div.get("class") == ['article__date']:
                for t in soup_article.find_all('time'):
                    if t.get("itemprop") == 'datePublished':
                        raw_date = t.get("datetime")
                        date_p = raw_date[0:10]
                        date_p = datetime.strptime(date_p, "%Y-%m-%d").strftime("%d/%m/%Y")

        # Retrieving of the artical theme
        for div in soup_article.find_all('div'):
            if div.get("class") == ['navigation__sousmenu']:
                theme = div.get("libelle")

        # Retrieving the content of the article
        for div in soup_article.find_all('div'):
            if div.get("itemprop") == 'mainEntityOfPage':
                for a in div.find_all('a'):
                    a.string = ""
                for span in div.find_all('span'):
                    span.string = ""
                contents = div.get_text()
        contents = re.sub(r"\s\s+", " ", contents)

        new_article = {
            "title": title,
            "newspaper": "L'Equipe",
            "author": author,
            "date_publi": date_p,
            "theme": theme,
            "content": contents
        }
        file_json.append(new_article)

sources = "Equipe_anciens/"
cur_date = date.datetime.now().date()

if not os.path.exists(file_target+sources):
    os.makedirs(file_target+sources)

# Call the create_json function
create_json(file_target, file_json, sources, "noob")