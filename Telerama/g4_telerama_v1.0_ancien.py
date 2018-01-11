#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import datetime as date
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
    articles=soup.find_all("div",class_="item--body")
    for article in articles:
        url_article=article.find("a").get("href")
        if is_article(url_article):
            # Insérer le nouveau article dans un le tableau
            result.append(get_article(url_article))
    return result

# Prend en argument une adresse url (url) et retourne une aticle 
def get_article(url):
    from unidecode import unidecode
    soup=utils.recovery_flux_urss(url)
    article=soup.find("article")
    meta=soup.find("meta",property="og:title").get("content")
    tab=meta.split("-")
    n=len(tab)
    newspaper=tab[n-1] 
    # Theme de l'article
    theme=tab[n-2]
    # Titre de l'article
    title="-".join(tab[:n-2])
    # tableau vide quand il y'a pas d'autheur sinon tableau de(s) auteur(s)
    authors=[]
    regex = re.compile(r'[\n\r\t]')
    for span in article.find_all("span",class_="author--name"):
        # Enlever les \n \r \t du contenu
        author = regex.sub("", unidecode(span.get_text()))
        authors.append(author)
    # Date de publication de l'article
    date_pub=article.find("span",itemprop="datePublished").get("datetime")
    # Theme de l'article
    # Contenu de l'article
    content=""
    for div in article.find_all("div",class_=["article--intro","article--wysiwyg","article--footnotes"]) :
        for p in div.find_all("p"):
            content=content+p.get_text()
    # Enlever les \n \r \t du contenu
    content = regex.sub("", content)
    return utils.recovery_article(unidecode(title),unidecode(newspaper),authors,date_pub,unidecode(content),unidecode(theme))

def is_article(url):
    soup=utils.recovery_flux_urss(url)
    return soup.find("div",class_="article--text")!=None

# Chemin repertoire des articles
file_target="/home/etudiant/Documents/ProjetSID/Groupe4_Robot/Telerama/Art/"


articles=[]

source="Telerama/"

categories={
    "cinema" : 20,
    "scenes" : 15,
    "enfants" : 3,
    "idees" : 10,
}

for category,nbre in categories.items() :
    for i in range(0,nbre) :
        url="http://www.telerama.fr/"+category+"/articles?page="+str(i)
        articles.extend(get_article_of_category(url))

utils.create_index()
utils.create_json(file_target,articles,source,"tera")