# Group 4
# Realized by BENJEBRIA Sofian, DELOEUVRE Noémie

from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
import g4_utils_v2
import date

# Path to modify : target where we will store the json files
fileTarget = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Projet_inter_promo/"

# We go through all the themes of the Nouvel Obs website and for each theme
# we get the articles of 8 pages

list_category = ["politique", "monde", "economie", "culture",
                 "editos-et-chroniques", "debat"]

file_json = []
for cat in list_category:
    # We retrieve the URL feeds for each page of article
    # Each HTML-coded article is analyzed with beautiful soup
    for i in range(2, 10):
        url_rss_noob = "http://www.nouvelobs.com/" + cat + "/page-" + str(i)
        + ".html"

        req = requests.get(url_rss_noob)
        data = req.text
        soup_url = BeautifulSoup(data, "lxml")

        article_noob = []
        # We retrieve all the articles for a given page
        for h3 in soup_url.find_all('h3'):
            if h3.get("class") == ['title']:
                for valeur in re.finditer('^\/', str(h3.a.get("href"))):
                    new_article = "http://www.nouvelobs.com" + h3.a.get("href")
                    article_noob.append(new_article)

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
                    for valeur in re.finditer('[0-9]{4}\/[0-9]{2}\/[0-9]{2}',
                                              str(time)):
                        date_p = valeur.group(0)
                        date_p = datetime\
                            .strptime(date_p, "%Y/%m/%d").strftime("%d/%m/%Y")

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

print(file_json)

sources = "NouvelObs_anciens/"
# Call the create_json function
g4_utils_v2.create_json(fileTarget, file_json, sources, "noob")
