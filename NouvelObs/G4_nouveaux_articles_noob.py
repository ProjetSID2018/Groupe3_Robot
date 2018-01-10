# Group 4
# Realized by BENJEBRIA Sofian, DELOEUVRE Noémie

import os
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import utils

# Path to modify : target where we will store the json files
fileTarget = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Projet_inter_promo/"

url_rss_noob = "http://www.nouvelobs.com/rss/"

# We retrieve the URL feeds fo each new article
# Each article coded in HTML is analized with beautiful soup.

req = requests.get(url_rss_noob)
data = req.text
soup = BeautifulSoup(data, "lxml")

liste_url = []
# Retrieving all urls of new RSS feeds of different categories
for a in soup.find_all('a'):
    for valeur in re.finditer('sp-rss', str(a.get("class"))):
        for valeur in re.finditer('www', str(a.get("href"))):
            liste_url.append(a.get("href"))

file_json = []
# Each url is analized one by one
for url in liste_url:
    req = requests.get(url)
    data = req.text
    soup_url = BeautifulSoup(data, "lxml")
    items = soup_url.find_all("item")
    article_noob = []

    # We're picking up every new article in a list
    for item in items:
        article_noob.append(re.search(r"<link/>(.*)", str(item))[1])
    # Each article is analized one by one
    for article in article_noob:
        req = requests.get(article)
        data = req.text
        soup_article = BeautifulSoup(data, "lxml")

        sources = "NouvelObs/"
        cur_date = date.datetime.now().date()

        title = soup_article.title.get_text()

        # Retrieval of publication date
        for time in soup_article.find_all('time'):
            if time.get("class") == ['date']:
                for valeur in re.finditer('[0-9]{4}\/[0-9]{2}\/[0-9]{2}', str(time)):
                    date_p = valeur.group(0)
                    date_p = datetime.strptime(date_p, "%Y/%m/%d").strftime("%d/%m/%Y")

        # Retrieval of the author of the article
        for div in soup_article.find_all('div'):
            for valeur in re.finditer('author', str(div.get("class"))):
                author = div.p.span.get_text()

        # Retrieval of the artical theme
        for nav in soup_article.find_all('nav'):
            if nav.get("class") == ['breadcrumb']:
                for ol in nav.find_all('ol'):
                    for a in ol.find_all('a'):
                        theme = a.get_text()

        # Retrieving the content of the article
        contents = ""
        for div in soup_article.find_all('div'):
            for valeur in re.finditer('body', str(div.get("id"))):
                for aside in div.find_all('aside'):
                    for p in aside.find_all('p'):
                        p.string = ""
                for p in div.find_all('p'):
                    for a in p.find_all('a'):
                        if a.get("class") == ['lire']:
                            a.string = ""
                    for img in p.find_all('img'):
                        p.string = ""
                    contents += p.get_text() + " "

        new_article = [{
            "title": title,
            "newspaper": "Le Nouvel Observateur",
            "date_publi": date_p,
            "author": author,
            "theme": theme,
            "content": contents
        }]
        file_json.append(new_article)

sources = "NouvelObs_nouveaux/"
cur_date = date.datetime.now().date()

if not os.path.exists(fileTarget+sources):
    os.makedirs(fileTarget+sources)

# Call the create_json function
utils.create_json(fileTarget, file_json, sources, "noob")
