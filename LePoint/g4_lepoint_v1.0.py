# Authors : Noemie DELOEUVRE, Morgan SEGUELA, Aurelien PELAT
# Version : 0.1

import os
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
import datetime
import g4_utils_v2

fileTarget = "/var/www/html/projet2018"

# Adresse url du flux RSS du figaro
url_rss_lepoint = "http://www.lepoint.fr/rss/"

# Parsing de la page RSS avec Beautiful Soup
req = requests.get(url_rss_lepoint)
data = req.text
soup = BeautifulSoup(data, "lxml")

# Creation de la liste des themes disponibles
links_themes_lepoint = []
for a in soup.find_all("a"):
    if ("http://www.lepoint.fr/" in a.get("href")[0:22]
    and a.get("href") != "http://www.lepoint.fr/content/system/rss/24H/24H_doc.xml"):
        and a.get("href") not in
            "http://www.lepoint.fr/content/system/rss/24H/24H_doc.xml"):
        links_themes_lepoint.append(a.get("href"))


numero_article = 1
# Parcours des themes
for link_theme in links_themes_lepoint:
    url_rss_lepoint_theme = link_theme

    # Recuperation du theme
    theme = re.search("http://www.lepoint.fr/(.*)/rss.xml", link_theme)[1]

    # Modification des themes dont le nom est different de celui dans l url
    if theme == "chroniqueurs-du-point/jean-guisnel":
        theme = "Defense ouverte"
    if theme == "high-tech-internet/planete-appli":
        theme = "Planete Appli"

    # Parsing de la page du theme avec Beautiful Soup
    req = requests.get(url_rss_lepoint_theme)
    data = req.text
    soup = BeautifulSoup(data, "lxml")

    # Creation de la liste d articles du theme
    items = soup.find_all("item")
    articles = []
    for item in items:
        articles.append(re.search(r"<link/>(.*)", str(item))[1])

    # Creation de la liste des articles du theme
    fichier_json = []
    # Parcours des articles du theme
    for article in articles:

        # Parsing de l article avec Beautiful Soup
        req = requests.get(article)
        data = req.text
        soup = BeautifulSoup(data, "lxml")

        # Recuperation du titre
        balise_title = soup.title.string
        sep = balise_title.split("-")
        titre = sep[0]

        # Recuperation de la liste des auteurs de l article
        auteur = []
        for a in soup.find_all('a'):
            if a.get('class') == ['show-author']:
                auteur.append(a.get_text())
        # "\s\s+", "",

        # Recuperation dela date de publication et eventuellement d une date
        # de modification
        dates = []
        for time in soup.find_all('time'):
            for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', str(time)):
                dates.append(date.datetime.strptime(valeur.group(0), '%d/%m/%Y'))

        #Recuperation de la date de publication de l article
        date_p = date.datetime.strftime(min(dates), '%d/%m/%Y')
        
        #Recuperation du contenu de l article
            for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',
                                      str(time)):
                dates.append(datetime.datetime.strptime(valeur.group(0),
                                                        '%d/%m/%Y'))

        # Recuperation de la date de publication de l article
        date_p = datetime.datetime.strftime(min(dates), '%d/%m/%Y')

        # Recuperation du contenu de l article
        contenu = ""
        for h2 in soup.find_all('h2'):
            if h2.get('class') == ['art-chapeau']:
                contenu += h2.get_text()+" "

        for div in soup.find_all('div'):
            if div.get('class') == ['art-text']:
                for p in div.find_all('p'):
                    contenu += p.get_text() + " "

        new_article = {
                "title": titre,
                "newspaper": 'Le Point.fr',
                "author": auteur,
                "date_publi": date_p,
                "content": contenu,
                "theme": theme
        }

        # Ajout de l article a la liste d articles
        fichier_json.append(new_article)

sources = "LePoint/"
g4_utils_v2.create_json(fileTarget, fichier_json, sources, "lpt")
