# -*- coding: utf-8 -*-
# Group 4 Robot - Lea Besnard, Laetitia Krumeich, Noémie Deloeuvre,
# Sofian Benjebria, Morgan Seguela

from bs4 import BeautifulSoup
import requests
import re
import unidecode
import g4_utils_v2

list_category = ["grand-sud", "actu", "faits-divers",
                 "economie", "sports", "sante", "tv-people", "sorties"]

# We retrieve the rss feeds for each article page
# Each HTML-coded article is scanned with beautiful soup

article_ladepeche = []
file_json = []

for cat in list_category:
    for i in range(1, 6):
        url_rss_ladepeche = "https://www.ladepeche.fr/recherche/?p=" + str(i)\
         + "&c=" + cat + "&plus-infos=1"
        req = requests.get(url_rss_ladepeche)
        data = req.text
        soup = BeautifulSoup(data, "lxml")

        # We retrieve all the URL flux of each page
        # Each HTML-coded article is scanned with beautiful soup.
        for h2 in soup.find_all("h2"):
            for item in h2.find_all("a"):
                link = "https://www.ladepeche.fr" + str(item.get("href"))
                article_ladepeche.append(link)

        # Retrieving variables needed to create the json file
        for article in article_ladepeche:
            req = requests.get(article)
            data = req.text
            soup = BeautifulSoup(data, "lxml")

            # Retrieve the title
            for meta in soup.find_all('meta'):
                if meta.get("property") == 'og:title':
                    title = meta.get("content")
            title = unidecode.unidecode(title)

            # Retrieve the publication date
            for time in soup.find_all('time'):
                if time.get("itemprop") == 'datePublished':
                    for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',
                                              str(time)):
                        date = valeur.group(0)

            # Retrieve the author
            author = []
            for div in soup.find_all('div'):
                if div.get("class") == ['article_author']:
                    author.append(unidecode.unidecode(div.span.get_text()))

            # Retrieve the content
            content = ""
            for div in soup.find_all('div'):
                if div.get("itemprop") == 'articleBody':
                    for p in div.find_all('p'):
                        content += p.get_text() + " "
            content = unidecode.unidecode(content)

            # Retrieve the theme
            theme = ""
            for h2 in soup.find_all('h2'):
                if h2.get("itemprop") == 'about':
                    theme = h2.get_text()
            theme = unidecode.unidecode(theme)

            # Retrieve all the informations off the article
            new_article = {
                    "title": title,
                    "newspaper": "La Depeche",
                    "author": author,
                    "date_publi": date,
                    "content": content,
                    "theme": theme
            }
            # add each new article in the "file_json" table
            file_json.append(new_article)

g4_utils_v2.create_json("C:/Users/Laetitia/Desktop/Groupe4_Robot", file_json,
                        "Ladepeche_articles_anciens/", "LD")
