# Group 4
# Realized by BENJEBRIA Sofian, DELOEUVRE Noémie

import datetime as date
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
import os
from G4_create_json import create_json

file_target = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Projet_inter_promo/"
os.makedirs(file_target, exist_ok=True)

url_rss_equipe = "https://www.lequipe.fr/rss/"

# We retrieve the URL feeds for each new article
# Each HTML-coded article is analyzed with beautiful soup
req = requests.get(url_rss_equipe)
data = req.text
soup = BeautifulSoup(data, "lxml")

liste_url = []
# Retrieving all urls of new RSS feeds of different categories
for div in soup.find_all('div'):
    if div.get("class") == ['glace']:
        for a in div.find_all('a'):
            for valeur in re.finditer('^(http://www.lequipe.fr/rss/actu_rss)', str(a.get("href"))):
                liste_url.append(a.get("href"))

file_json = []
for url in liste_url:
    req = requests.get(url)
    data = req.text
    soup_url = BeautifulSoup(data, "lxml")
    items = soup_url.find_all("item")
    article_equipe = []

    # We're picking up every new article in a list
    for item in items:
        article_equipe.append(re.search(r"<link/>(.*)", str(item))[1])
    # Each article is analized one by one
    for article in article_equipe:
        req = requests.get(article)
        data = req.text
        soup_article = BeautifulSoup(data, "lxml")

        # Retrieving of title
        balise_title = soup_article.title.string
        sep = balise_title.split("—")
        title = sep[0]

        # Retrieving of the author
        for meta in soup.find_all('meta'):
            if meta.get("name") == 'Author':
                author = meta.get("content")

        # Retrieving of date of publication
        for div in soup.find_all('div'):
            if div.get("class") == ['article__date']:
                for t in soup.find_all('time'):
                    if t.get("itemprop") == 'datePublished':
                        raw_date = t.get("datetime")
                        date_p = raw_date[0:10]
                        date_p = datetime.strptime(date_p, "%Y-%m-%d").strftime("%d/%m/%Y")

        # Retrieving of the artical theme
        for div in soup.find_all('div'):
            if div.get("class") == ['navigation__sousmenu']:
                theme = div.get("libelle")

        # Retrieving the content of the article
        for div in soup.find_all('div'):
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

sources = "Equipe_nouveaux/"
cur_date = date.datetime.now().date()

if not os.path.exists(file_target+sources):
    os.makedirs(file_target+sources)

# Call the create_json function
create_json(file_target, file_json, sources, "equi")
