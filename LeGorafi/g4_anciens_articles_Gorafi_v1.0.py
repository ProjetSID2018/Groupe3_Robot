# Group 4
# Realized by BENJEBRIA Sofian, DELOEUVRE Noémie

import os
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
import g4_utils_v2

# Path to modify : target where we will store the json files
file_target = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Projet_inter_promo/"
+ str(date.datetime.now().date()) + "/"
# file_target = "/var/www/html/projet2018/data/clean/robot/"
# + str(date.datetime.now().date()) +"/"
os.makedirs(file_target, exist_ok=True)

list_category = ["france/politique", "france/societe", "monde-libre",
                 "france/economie", "culture", "people", "sports", "hi-tech",
                 "sciences", "ledito"]

# We go through all the themes of the Gorafi website and for each theme
# we get the articles of 6 pages (120 articles per theme)

file_json = []
for cat in list_category:
    # We retrieve the URL feeds for each page of article
    # Each HTML-coded article is analyzed with beautiful soup
    for i in range(2, 8):
        url_rss_gorafi = "http://www.legorafi.fr/category/" + cat + "/page/"
        + str(i) + "/feed/"
        req = requests.get(url_rss_gorafi)
        data = req.text
        soup = BeautifulSoup(data, "lxml")
        items = soup.find_all("item")
        article_gorafi = []

        # We retrieve all the articles for a given page
        for item in items:
            article_gorafi.append(re.search(r"<link/>(.*)", str(item))[1])

        # Retrieving variables needed to create the json file
        for article in article_gorafi:
            req = requests.get(article)
            data = req.text
            soup = BeautifulSoup(data, "lxml")
            balise_title = soup.title.get_text()
            sep = balise_title.split("—")
            title = sep[0]
            newspaper = sep[1]
            author = []

            # Retrieving of author and publication date
            for span in soup.find_all('span'):
                if span.get("class") == ['context']:
                    author.append(span.a.get_text())
                    for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',
                                              str(span)):
                        date_p = valeur.group(0)

            # Retrieving the theme
            for ul in soup.find_all('ul'):
                if ul.get("class") == ['post-categories']:
                    for li in ul.find_all('li'):
                        theme = li.get_text()
            contents = ""

            # Retrieving the content of the article
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

# Call the create_json function
g4_utils_v2.create_json(file_target, file_json, sources, "lg")
