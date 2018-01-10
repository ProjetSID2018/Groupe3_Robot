# -*- coding: utf-8 -*-
# Group 4 Robot - Lea BESNARD, Laetitia KRUMEICH, Sofian BENJEBRIA,
# Noémie DELOEUVRE , Morgan SEGUELA

from bs4 import BeautifulSoup
import requests
import re
import g4_utils_v2

fileTarget = "C:/Users/lea/Desktop/PROJET/"
rss = requests.get("https://www.ladepeche.fr/services/flux-rss/")
data = rss.text
soup = BeautifulSoup(data)
i = 0

# We retrieve the rss feeds for each article page.
# Each HTML-coded article is scanned with beautiful soup.
for link in soup.find_all("a"):
    if link.get("class") == ["rss"]:
        url_rss_ladepeche = link.get("href")
        url_rss_ladepeche = "https://www.ladepeche.fr/"+url_rss_ladepeche
        req = requests.get(url_rss_ladepeche)
        data = req.text
        soup = BeautifulSoup(data, "lxml")
        article_ladepeche = []
        items = soup.find_all("item")

        # We retrieve all articles
        for item in items:
            article_ladepeche.append(re.search(r"<link/>(.*)", str(item))[1])

        file_json = []
        for article in article_ladepeche:
            req = requests.get(article)
            data = req.text
            soup = BeautifulSoup(data, "lxml")
            sources = "La Depeche"

            # Retrieve the title
            for meta in soup.find_all('meta'):
                if meta.get("property") == 'og:title':
                    title = meta.get("content")

            # Retrieve the publication date
            for time in soup.find_all('time'):
                if time.get("itemprop") == 'datePublished':
                    date = time.get("itemprop")
                    for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',
                                              str(time)):
                        date = valeur.group(0)

            # Retrieve the author
            author = []
            for div in soup.find_all('div'):
                if div.get("class") == ['article_author']:
                    author.append(div.span.get_text())

            # Retrieve the content
            content = ""
            for div in soup.find_all('div'):
                if div.get("itemprop") == 'articleBody':
                    for p in div.find_all('p'):
                        content += p.get_text() + " "

            # Retrieve the theme
            theme = ""
            for h2 in soup.find_all('h2'):
                if h2.get("itemprop") == 'about':
                    theme = h2.get_text()

            # Retrieve all the informations off the article
            new_article = [{
                "title": title,
                "newspaper": "La Depeche",
                "author": author,
                "date_publi": date,
                "content": content,
                "theme": theme
            }]
            # add each new article in the "file_json" table
            file_json.append(new_article)

sources = "Ladepeche_articles_nouveaux/"

g4_utils_v2.create_json("C:/Users/Laetitia/Desktop/Groupe4_Robot", file_json,
                        "Ladepeche_articles_anciens/", "LD")
