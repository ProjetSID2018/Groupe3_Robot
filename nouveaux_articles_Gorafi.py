import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re

fileTarget = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Projet_inter_promo/"

url_rss_gorafi = "http://www.legorafi.fr/feed/"

req = requests.get(url_rss_gorafi)
data = req.text
soup = BeautifulSoup(data, "lxml")
items = soup.find_all("item")
article_gorafi = []
for item in items:
    article_gorafi.append(re.search(r"<link/>(.*)", str(item))[1])
fichier_json=[]
for article in article_gorafi:
    req = requests.get(article)
    data = req.text

    soup = BeautifulSoup(data, "lxml")

    balise_title = soup.title.string
    sep = balise_title.split("—")
    titre = sep[0]
    journal = sep[1]

    for span in soup.find_all('span'):
        if span.get("class") == ['context']:
            auteur = span.a.string
            for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', str(span)):
                date_p = valeur.group(0)
                           
    for ul in soup.find_all('ul'):
        if ul.get("class") == ['post-categories'] :
            for li in ul.find_all('li'):
                categorie = li.get_text()
   
    contenu = ""            
    for div in soup.find_all('div'):
        if div.get("class") == ['content']:
            for p in div.find_all('p'):
                contenu += p.get_text() + " "

    new_article = {
            "title" : titre,
            "newspaper" : journal,
            "author" : auteur,
            "date_publi" : date_p,
            "theme" : categorie,
            "content" : contenu
    }
    
    fichier_json.append(new_article)
    
print(fichier_json)

sources = "LeGorafi/"
cur_date = date.datetime.now().date()

if not os.path.exists(fileTarget+sources):
    os.makedirs(fileTarget+sources)

i = 1
for article in fichier_json:
    file_art = fileTarget + sources + "artJT"+ str(i) + str(cur_date) + "_robot.json"
    with open(file_art, "w", encoding="UTF-8") as fic:
        json.dump(article, fic, ensure_ascii=False)
    i += 1