#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as date
from unidecode import unidecode
import re
<<<<<<< HEAD
import g4_utils_v2

=======
>>>>>>> eb1ef29e58747b326eee0e1e4f0e5dc2897f026a

# Verifier si le tag contient le texte Copyright
def has_copyright(tag):
    """
        Verifier si le contenu de la balise contient le mot cle "copyright"
    """
    return "Copyright" in tag.get_text()

<<<<<<< HEAD

# Chemin repertoire des articles
fileTarget = "/home/etudiant/Documents/ProjetSID/Groupe4_Robot/20Minute/Art/"

url_rss = "http://www.20minutes.fr/feeds/rss-actu-france.xml"

req = requests.get(url_rss)

soup = BeautifulSoup(req.text, "html.parser")

items = soup.find_all("item")

articles = []

for item in items:
    # Récuperer le lien des articles
    url = re.search(r"<link/>(.*)<pubdate>", str(item)).group(1)
    req = requests.get(url)
    data = req.text
    soup = BeautifulSoup(data, "html.parser")
    article = soup.find("article", id="main-content")

    # Titre de l'article
    title = article.find("header").find("h1").get_text()
=======
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
>>>>>>> eb1ef29e58747b326eee0e1e4f0e5dc2897f026a
    # tableau vide quand il y'a pas d'autheur sinon tableau de(s) auteur(s)
    authors = [] if article.find("header")\
        .find("p", class_="authorsign-label")\
        == None else unidecode(article.find("header")
        .find("p", class_="authorsign-label").get_text()).split(" et ")
    # Date de publication de l'article
<<<<<<< HEAD
    date_pub = article.find("header").find("time").get("datetime")
=======
    date_pub=article.find("time").get("datetime")
>>>>>>> eb1ef29e58747b326eee0e1e4f0e5dc2897f026a
    # Theme de l'article
    theme = article.find("ol", class_="breadcrumb-list")\
        .find_all("li")[1].find("span").get_text()
    # Contenu de l'article
<<<<<<< HEAD
    content = ""
    for p in article.find("div", class_=["lt-endor-body", "content"])\
    .find_all("p"):
        content = content + p.get_text()

=======
    content=""
    for p in article.find("div",class_="content").find_all("p"):
        content=content+p.get_text()
    # Nom du journal
    newspaper=soup.find("footer").find(has_copyright).find("a").get_text()
>>>>>>> eb1ef29e58747b326eee0e1e4f0e5dc2897f026a
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

<<<<<<< HEAD
    # Nom du journal
    newspaper = soup.find("footer").find(has_copyright).find("a").get_text()

    # Date courrent
    now = str(date.datetime.now().date())

    # Insérer le nouveau article dans un le tableau
    articles.append({
            "title": unidecode(title),
            "newspaper": unidecode(newspaper),
            "author": authors,
            "date_publi": date_pub,
            "content": unidecode(content),
            "theme": unidecode(theme)
    })
=======

# Chemin repertoire des articles
fileTarget="/home/etudiant/Documents/ProjetSID/Groupe4_Robot/20Minutes/Art/"

url_rss= "http://www.20minutes.fr/feeds/rss-actu-france.xml"
>>>>>>> eb1ef29e58747b326eee0e1e4f0e5dc2897f026a

soup = get_soup(url_rss)

items = soup.find_all("item")

<<<<<<< HEAD
# creation of the file
g4_utils_v2.create_json("C:/", articles, sources, "fusc")
=======
articles=[]

for item in items:
    #Récuperer le lien des articles
    url=re.search(r"<link/>(.*)<pubdate>", str(item)).group(1)
    articles.append(get_article(url))


# Creer le repertoire s'il n'existe pas
if not os.path.exists(fileTarget):
    os.makedirs(fileTarget)
# Date courrent
now=str(date.datetime.now().date())
# Enumérer les articles et pour chaque article , copier le contenu dans un fichier de nom art_numAr_date_robot.json
for i,article in enumerate(articles):
    file_art = fileTarget  + "art_"+str(i)+"_"+ now + "_robot.json"
    with open(file_art, "w", encoding="UTF-8") as fil:
        json.dump(article, fil,indent=4)
>>>>>>> eb1ef29e58747b326eee0e1e4f0e5dc2897f026a
