#Authors : Noemie DELOEUVRE, Morgan SEGUELA, Aurelien PELAT
#Version : 1.4

import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
import utils

file_target = "A ADAPTER AU SERVEUR"

#Adresse url du flux RSS du figaro
url_rss_figaro = "http://www.lefigaro.fr/rss/"

#Parsing de la page RSS avec Beautiful Soup
req = requests.get(url_rss_figaro)
data = req.text
soup = BeautifulSoup(data, "lxml")

#Creation de la liste des themes disponibles (excepte videos et photographies)
items = soup.find_all("item")
links_themes_figaro = []
for span in soup.find_all("span"):
    if span.get("class") == ['boite2']:
        if ("http://www.lefigaro.fr/rss/figaro_" in span.find('a')['href']
        and "http://www.lefigaro.fr/rss/figaro_videos.xml" != span.find('a')['href']
        and "http://www.lefigaro.fr/rss/figaro_photos.xml" != span.find('a')['href']): 
            links_themes_figaro.append(span.find('a')['href'])


numero_article = 1
#Parcours des themes
for link_theme in links_themes_figaro:
    url_rss_figaro_theme = link_theme;
    
    #Recuperation du theme
    theme = re.search("http://www.lefigaro.fr/rss/figaro_(.*).xml", link_theme)[1]
    
    #Parsing de la page du theme avec Beautiful Soup
    req = requests.get(url_rss_figaro_theme)
    data = req.text
    soup = BeautifulSoup(data, "lxml")
    
    
    #Creation de la liste d articles du theme
    items = soup.find_all("item")
    articles_temp = []
    for item in items:
        articles_temp.append(re.search(r"<link/>(.*)", str(item))[1])
    
    #Supprimer les lien d'articles du theme vides (codage maladroit du site)
    articles_figaro = []
    for article in articles_temp:
        if article != '':
            articles_figaro.append(article)
    
    #Creation de la liste des articles du theme
    fichier_json=[]
    #Parcours des articles du theme
    for article in articles_figaro:
        
        #Parsing de l article avec Beautiful Soup
        req = requests.get(article)
        data = req.text
        soup = BeautifulSoup(data, "lxml")
        
        #Recuperation du titre
        titre = soup.title.string
        
        #Recuperation de la liste des auteurs de l article
        auteur = []
        for a in soup.find_all('a'):
            if a.get("class") == ['fig-content-metas__author']:
                auteur.append(re.sub("\s\s+", "", a.get_text()))
        
        #Recuperation de la date de publication de l article
        date_p = ""
        for time in soup.find_all('time'):
            for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', str(time)):
                date_p = valeur.group(0)
        
        #Recuperation du contenu de l article
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
                "content" : contenu,
                "theme" : theme
        }
        
        #Ajout de l article a la liste d articles
        fichier_json.append(new_article)
    
sources = "leFigaro/"

# Call the create_json function
utils.create_json(file_target, fichier_json, sources, "lg")