#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as date
from unidecode import unidecode
import re
import g4_utils_v2


# Verifier si le tag contient le texte Copyright
def has_copyright(tag):
    """
        Verifier si le contenu de la balise contient le mot cle "copyright"
    """
    return "Copyright" in tag.get_text()

# Prend en parametre une adresse url et retour la soup
def get_soup(url):
    import requests
    from bs4 import BeautifulSoup
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup

"""Prend en argument une adresse url (url) et retourne une article au format 
    {
        "title" : str,
        "newspaper" : str,
        "author" : [str],
        "date_publi" : str,
        "content" : str,
        "theme" : str
        }
"""
def get_article(url):
    soup=get_soup(url)
    article=soup.find("article")
    # Titre de l'article
    title=article.find("h1").get_text()
    # tableau vide quand il y'a pas d'autheur sinon tableau de(s) auteur(s)
    authors = [] if article.find("header")\
        .find("p", class_="authorsign-label")\
        == None else unidecode(article.find("header")
        .find("p", class_="authorsign-label").get_text()).split(" et ")
    # Date de publication de l'article
    date_pub=article.find("time").get("datetime")
    # Theme de l'article
    theme = article.find("ol", class_="breadcrumb-list")\
        .find_all("li")[1].find("span").get_text()
    # Contenu de l'article
    content=""
    for p in article.find("div",class_="content").find_all("p"):
        content=content+p.get_text()
    # Nom du journal
    newspaper=soup.find("footer").find(has_copyright).find("a").get_text()
    regex = re.compile(r'[\n\r\t]')
    # Elever les \n \r \t du contenu
    content = regex.sub("", content)
    return {
        "title" : unidecode(title),
        "newspaper" : unidecode(newspaper),
        "author" : authors,
        "date_publi" : date_pub,
        "content" : unidecode(content),
        "theme" : unidecode(theme)
        }

    # Nom du journal
    newspaper = soup.find("footer").find(has_copyright).find("a").get_text()

# Chemin repertoire des articles
fileTarget="/home/etudiant/Documents/ProjetSID/Groupe4_Robot/20Minutes/Art/"

    # Insérer le nouveau article dans un le tableau
    articles.append({
            "title": unidecode(title),
            "newspaper": unidecode(newspaper),
            "author": authors,
            "date_publi": date_pub,
            "content": unidecode(content),
            "theme": unidecode(theme)
    })
url_rss= "http://www.20minutes.fr/feeds/rss-actu-france.xml"

soup = get_soup(url_rss)

items = soup.find_all("item")

# creation of the file
g4_utils_v2.create_json("C:/", articles, sources, "fusc")
