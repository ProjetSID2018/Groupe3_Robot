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

list_category = ["politique", "société", "social-eco", "culture", "sports",
                 "monde", "environnement", "rubriques/en-debat"]

file_json = []
for cat in list_category:
    # We retrieve the URL feeds for each page of article
    # Each HTML-coded article is analyzed with beautiful soup
    for i in range(2, 10):
        url_rss_humanite = "https://humanite.fr/" + cat + "?page=" + str(i) + "/feed/"
        req = requests.get(url_rss_humanite)
        data = req.text
        soup_url = BeautifulSoup(data, "lxml")
        article_humanite = []
        # We retrieve all the articles for a given page
        for div in soup_url.find_all('div'):
            for valeur in re.finditer('field-name-field-news-chapo', str(div.get("class"))):
                for a in div.find_all('a'):
                    article_humanite.append(a.get("href"))

        # Each article is analized one by one
        for article in article_humanite:
            req = requests.get(article)
            data = req.text
            soup = BeautifulSoup(data, "lxml")

            # Retrieving of title
            for meta in soup.find_all('meta'):
                if meta.get("property") == 'og:title':
                    title = meta.get("content")

            # Retrieving of the newspaper name
            for meta in soup.find_all('meta'):
                if meta.get("property") == 'og:site_name':
                    newspaper = meta.get("content")

            # Retrieving of the theme
            for meta in soup.find_all('meta'):
                if meta.get("property") == 'article:section':
                    theme = meta.get("content")

            # Retrieving of the author
            for h2 in soup.find_all('h2'):
                for a in h2.find_all('a'):
                    for valeur in re.finditer('auteur', str(a.get("href"))):
                        author = a.get_text()

            # Retrieving of the date of publication
            for meta in soup.find_all('meta'):
                if meta.get("property") == 'article:published_time':
                    raw_date = meta.get("content")
                    date_p = raw_date[0:10]
                    date_p = datetime.strptime(date_p, "%Y-%m-%d").strftime("%d/%m/%Y")

            # Retrieving the content of the article
            contents = ""
            for p in soup.find_all('p'):
                for a in p.find_all('a'):
                    if a.get_text() == "Lire la suite":
                        a.string = ""
                if p.get("class") == ['TX']:
                    contents += p.get_text()

            new_article = [{
                "title": title,
                "newspaper": newspaper,
                "date_publi": date_p,
                "author": author,
                "theme": theme,
                "content": contents
            }]
            file_json.append(new_article)

sources = "Humanite_anciens/"
cur_date = date.datetime.now().date()

if not os.path.exists(file_target+sources):
    os.makedirs(file_target+sources)


# Call the create_json function
create_json(file_target, file_json, sources, "hum")
