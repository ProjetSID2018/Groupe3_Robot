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

url_rss_hum = "https://www.humanite.fr/rss/actu.rss"

# We retrieve the URL feeds for each new article
# Each HTML-coded article is analyzed with beautiful soup
req = requests.get(url_rss_hum)
data = req.text
soup = BeautifulSoup(data, "lxml")
items = soup.find_all("item")
article_humanite = []

# We're picking up every new item in a list
for item in items:
    article_humanite.append(re.search(r"<link/>(.*)", str(item))[1])
file_json = []

for article in article_humanite:
    req = requests.get(article)
    data = req.text
    soup = BeautifulSoup(data, "lxml")

    for meta in soup.find_all('meta'):
        if meta.get("property") == 'og:title':
            title = meta.get("content")

    for meta in soup.find_all('meta'):
        if meta.get("property") == 'article:section':
            theme = meta.get("content")

    for h2 in soup.find_all('h2'):
        for a in h2.find_all('a'):
            for valeur in re.finditer('auteur', str(a.get("href"))):
                author = a.get_text()

    for meta in soup.find_all('meta'):
        if meta.get("property") == 'article:published_time':
            raw_date = meta.get("content")
            date_p = raw_date[0:10]
            date_p = datetime.strptime(date_p, "%Y-%m-%d").strftime("%d/%m/%Y")

    contents = ""
    for div in soup.find_all('div'):
        if div.get("class") == ['field', 'field-name-field-news-chapo', 'field-type-text-long', 'field-label-hidden']:
            for p in div.find_all('p'):
                contents += p.get_text()
        if div.get("class") == ['field', 'field-name-field-news-text', 'field-type-text-long', 'field-label-hidden']:
            for p in div.find_all('p'):
                contents += p.get_text()

    new_article = {
        "title": title,
        "newspaper": "Humanite",
        "date_publi": date_p,
        "author": author,
        "theme": theme,
        "content": contents
    }
    file_json.append(new_article)

sources = "Humanite_nouveaux/"
cur_date = date.datetime.now().date()

if not os.path.exists(file_target+sources):
    os.makedirs(file_target+sources)


# Call the create_json function
create_json(file_target, file_json, sources, "hum")
