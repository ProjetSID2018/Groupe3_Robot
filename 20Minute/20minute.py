#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import datetime as date
from bs4 import BeautifulSoup
from unidecode import unidecode
import requests
import re

# Verifier si le tag contient le texte Copyright
def has_copyright(tag):
    """
        Verifier si le contenu de la balise contient le mot cle "copyright"
    """
    return "Copyright" in tag.get_text()

# Chemin repertoire des articles
fileTarget="/home/etudiant/Documents/ProjetSID/Groupe4_Robot/20Minute/Art/"

url_rss= "http://www.20minutes.fr/feeds/rss-actu-france.xml"

req = requests.get(url_rss)

soup = BeautifulSoup(req.text, "html.parser")

items = soup.find_all("item")

articles=[]

for item in items:
    #Récuperer le lien des articles
    url=re.search(r"<link/>(.*)<pubdate>", str(item)).group(1)
    req = requests.get(url)
    data = req.text
    soup=BeautifulSoup(data,"html.parser")
    article=soup.find("article",id="main-content")

    # Titre de l'article
    title=article.find("header").find("h1").get_text()
    # tableau vide quand il y'a pas d'autheur sinon tableau de(s) auteur(s)
    authors= [] if article.find("header").find("p",class_="authorsign-label")==None else unidecode(article.find("header").find("p",class_="authorsign-label").get_text()).split(" et ")
    # Date de publication de l'article
    date_pub=article.find("header").find("time").get("datetime")
    # Theme de l'article
    theme=article.find("ol",class_="breadcrumb-list").find_all("li")[1].find("span").get_text()
    # Contenu de l'article
    content=""
    for p in article.find("div",class_=["lt-endor-body", "content"]).find_all("p"):
        content=content+p.get_text()

    regex = re.compile(r'[\n\r\t]')
    # Elever les \n \r \t du contenu
    content = regex.sub("", content)

    # Nom du journal
    newspaper=soup.find("footer").find(has_copyright).find("a").get_text()

    # Date courrent
    now=str(date.datetime.now().date())

    # Insérer le nouveau article dans un le tableau
    articles.append({
    "title" : unidecode(title),
    "newspaper" : unidecode(newspaper),
    "author" : authors,
    "date_publi" : date_pub,
    "content" : unidecode(content),
    "theme" : unidecode(theme)
    })


sources = "20minutes/"

# Creer le repertoire s'il n'existe pas
if not os.path.exists(fileTarget+sources):
    os.makedirs(fileTarget+sources)

# Enumérer les articles et pour chaque article , copier le contenu dans un fichier de nom art_numAr_date_robot.json
for i,article in enumerate(articles):
    file_art = fileTarget + sources + "art_"+str(i)+"_"+ now + "_robot.json"
    with open(file_art, "w", encoding="UTF-8") as fil:
        json.dump(article, fil,indent=4)
