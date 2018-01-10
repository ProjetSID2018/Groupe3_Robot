# Groupe 4
# Realized by BENJEBRIA Sofian, DELOEUVRE Noémie, SEGUELA Morgan

import os
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
from G4_create_json import create_json

# Path to change : target where we will store the json files
file_target="/Users/Sofian/Documents/Robot/" + str(date.datetime.now().date()) +"/"
#file_target = "/var/www/html/projet2018/data/clean/robot/" + str(date.datetime.now().date()) +"/"
os.makedirs(file_target, exist_ok=True)

url_rss_gorafi = "http://www.legorafi.fr/feed/"

# We retrieve the URL feeds for each new article
# Each HTML-coded article is analyzed with beautiful soup
req = requests.get(url_rss_gorafi)
data = req.text
soup = BeautifulSoup(data, "lxml")
items = soup.find_all("item")
article_gorafi = []

# We're picking up every new item in a list
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

    # Recovery of author and publication date
    for span in soup.find_all('span'):
        if span.get("class") == ['context']:
            author.append(span.a.get_text())
            for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', str(span)):
                date_p = valeur.group(0)

    # Retrieving the theme
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
    if theme != "Magazine":
        file_json.append(new_article)

sources = "legorafi/"
cur_date = date.datetime.now().date()

if not os.path.exists(file_target+sources):
    os.makedirs(file_target+sources)


# Call the create_json function
create_json(file_target, file_json, sources, "lg")

