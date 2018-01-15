#!/usr/bin/env python
# -*- coding: utf-8 -*-
<<<<<<< HEAD:Minutes/g4_20minutes_v1.0.py

=======
""" -*- coding: utf-8 -*-
 Groupe 4
 SECK Mamadou
"""
>>>>>>> master:Minutes/g4_20minutes_v1.py
import os
import json
import datetime as date
from unidecode import unidecode
import re
import g4_utils_v31 as utils

# Verifier si le tag contient le texte Copyright
def has_copyright(tag):

    
    """
        Verifier si le contenu de la balise contient le mot cle "copyright"
    """
    return "Copyright" in tag.get_text()

def get_article(url):
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
    soup=utils.recovery_flux_urss(url)
    article=soup.find("article")
    # Titre de l'article
    title=article.find("h1").get_text()
    # tableau vide quand il y'a pas d'autheur sinon tableau de(s) auteur(s)
    authors = [] if article.find("header")\
        .find("p", class_="authorsign-label")\
        == None else unidecode(article.find("header")
        .find("p", class_="authorsign-label").get_text()).split(" et ")
    # Date de publication de l'article
<<<<<<< HEAD:Minutes/g4_20minutes_v1.0.py
    date_pub= article.find("time").get("datetime")
    date_pub = date.datetime.strptime(date_pub)
    print(str(date_pub.date()))
=======
<<<<<<< HEAD
    date_pub= article.find("time").get("datetime")
    date_pub = date.datetime.strptime(date_pub)
    print(str(date_pub.date()))
=======
    date_tab=article.find("time").get("datetime")[:10].split("-")
    date_tab.reverse()
    date_pub="/".join(date_tab)
>>>>>>> master
>>>>>>> master:Minutes/g4_20minutes_v1.py
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
    return utils.recovery_article(unidecode(title), unidecode(newspaper),authors,date_pub,unidecode(content),unidecode(theme))

# Prend en argument une adresse url et retourne vrai si la page contient une article et faux sinon
def is_article(url):
    soup=utils.recovery_flux_urss(url)
    article=soup.find("article")
    return article != None

<<<<<<< HEAD
def recovery_new_articles_min(file_target="/home/etudiant/Documents/ProjetSID/Groupe4_Robot/Minutes/Art/"):
        
    source="Minutes/"
    url_rss= "http://www.20minutes.fr/feeds/rss-actu-france.xml"

<<<<<<< HEAD:Minutes/g4_20minutes_v1.0.py
    soup = utils.recovery_flux_urss(url_rss)

=======
<<<<<<< HEAD
    soup = utils.recovery_flux_urss(url_rss)

    items = soup.find_all("item")

    articles=[]
    for item in items:
        #Récuperer le lien des articles
        url=re.search(r"<link/>(.*)<pubdate>", str(item)).group(1)
        if is_article(url):
            articles.append(get_article(url))

    utils.create_index()
    utils.create_json(file_target,articles,source,"min")

if __name__ == '__main__':
    recovery_new_articles_min()
    
=======
=======
>>>>>>> cabfc0f3b5a250cc3b7ce47776515a33ea51d5ea
def add_articles(file_target = "/home/etudiant/Documents/ProjetSID/Groupe4_Robot/Minutes/Art/" + str(date.datetime.now().date()) +"/"):
    """
        it create a json for each new article
    """
    soup = utils.recovery_flux_urss("http://www.20minutes.fr/feeds/rss-actu-france.xml")
>>>>>>> master:Minutes/g4_20minutes_v1.py
    items = soup.find_all("item")
    articles=[]
    for item in items:
        #Récuperer le lien des articles
        url=re.search(r"<link/>(.*)<pubdate>", str(item)).group(1)
        if is_article(url):
            articles.append(get_article(url))
    utils.create_json(file_target, articles, "Minutes/", "min")

if __name__ == '__main__':
<<<<<<< HEAD:Minutes/g4_20minutes_v1.0.py
    recovery_new_articles_min()
    
=======
    add_articles()       

>>>>>>> master
>>>>>>> master:Minutes/g4_20minutes_v1.py
