import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re

fileTarget = "C:/Users/aurel/Documents/Etudes/ProjetIPJournaux/"

url_rss_figaro_une = "http://www.lefigaro.fr/rss/figaro_actualites.xml";

req = requests.get(url_rss_figaro_une)
data = req.text
soup = BeautifulSoup(data, "lxml")
items = soup.find_all("item")
article_figaro = []
for item in items:
    article_figaro.append(re.search(r"<link/>(.*)", str(item))[1])

fichier_json=[]
for article in article_figaro:
    req = requests.get(article)
    data = req.text

    soup = BeautifulSoup(data, "lxml")

    titre = soup.title.string
   
    auteur = []
    
    for a in soup.find_all('a'):
        if a.get("class") == ['fig-content-metas__author']:
            auteur.append(re.sub("\s\s+", "", a.get_text()))
    
    date_publi = ""
    
    for time in soup.find_all('time'):
        for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', str(time)):
            date_p = valeur.group(0)
    
    contenu = ""

    for p in soup.find_all('p'):
        if p.get("class") == ['fig-content__chapo']:
            contenu = p.get_text() + " "
            
    for div in soup.find_all('div'):
        if div.get("class") == ['fig-content__body']:
            for p in div.find_all('p'):
                contenu += p.get_text() + " "

    new_article = {
            "title" : titre,
            "newspaper" : 'Le Figaro.fr',
            "author" : auteur,
            "date_publi" : date_p,
            "content" : contenu
    }
    
    fichier_json.append(new_article)
    
print(fichier_json)

sources = "LeFigaro/"
cur_date = date.datetime.now().date()

if not os.path.exists(fileTarget+sources):
    os.makedirs(fileTarget+sources)

i = 1
for article in fichier_json:
    file_art = fileTarget + sources + "artJT"+ str(i) + str(cur_date) + "_robot.json"
    with open(file_art, "w", encoding="UTF-8") as fic:
        json.dump(article, fic, ensure_ascii=False)
    i += 1