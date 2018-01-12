#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" -*- coding: utf-8 -*-
 Groupe 4
 SECK Mamadou
 V0 : create code
 V1.1 : create function
"""
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


# Prend en parametre une catégorie et retour toutes les articles de cette catégorie
def get_article_of_category(url):
    result=[]
    soup=utils.recovery_flux_urss(url)
    articles=soup.find_all('article')
    for article in articles:
        url_article="http://www.20minutes.fr"+article.find("a").get("href")
        # Insérer le nouveau article dans un le tableau
        if(is_article(url_article)):
            result.append(get_article(url_article))
    return result

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
    date_tab=article.find("time").get("datetime")[:10].split("-")
    date_tab.reverse()
    date_pub="/".join(date_tab)
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
    return utils.recovery_article(unidecode(title), unidecode(newspaper),authors,str(date_pub),unidecode(content),unidecode(theme))

# Prend en argument une adresse url et retourne vrai s'il est un article et faux sinon
def is_article(url):
    soup=utils.recovery_flux_urss(url)
    article=soup.find("article")
    return article != None

    
def add_articles(file_target = "/home/etudiant/Documents/ProjetSID/Groupe4_Robot/Minutes/Art/" + str(date.datetime.now().date()) +"/"):
    """
        it create a json for each new article
    """
    soup = utils.recovery_flux_urss("http://www.20minutes.fr")

    categories=soup.find("nav",class_="header-nav").find_all("li")
    articles=[]

    for category in categories:
        url=category.find("a").get("href")
        theme=unidecode(category['data-theme'])
        if theme in ["default","entertainment","sport","economy","hightech","planet"]:
            articles.extend(get_article_of_category(url))
    utils.create_json(file_target, articles, "Minutes/", "min")


if __name__ == '__main__':
    add_articles()     