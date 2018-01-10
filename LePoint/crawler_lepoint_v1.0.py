# -*- coding: utf-8 -*-
#Authors : Noemie DELOEUVRE, Morgan SEGUELA, Celine Mothes, Aurelien PELAT
#Version : 1.0

import os
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
import http.client
from urllib.parse import urlparse

"""
Fonction ajoutant des articles dans une liste @fichier_json donnee
d une adresse url @url_lepoint_theme donnee
"""
def collect_articles(fichier_json, url_lepoint_theme):
    #Parsing de la page du theme avec Beautiful Soup
    req = requests.get(url_lepoint_theme)
    data = req.text
    soup = BeautifulSoup(data, "lxml")
    
    #Creation de la liste d articles du theme
    url_articles = []
    for div in soup.find_all('div'):
        if div.get('class') == ['list-view']:
            for a in div.find_all('a'):
                if 'http' in a.get('href'):
                    url_articles.append(a.get('href'))
                else:
                    url_articles.append('http://www.lepoint.fr'+a.get('href'))

    #Parcours des articles du theme
    for url_article in url_articles:
        
        #Parsing de l article avec Beautiful Soup
        req = requests.get(url_article)
        data = req.text
        soup = BeautifulSoup(data, "lxml")
        
        #Recuperation du titre
        balise_title = soup.title.string
        sep = balise_title.split("-")
        titre = sep[0]
        
        #Recuperation de la liste des auteurs de l article
        auteur = []
        for a in soup.find_all('a'):
            if a.get('class') == ['show-author']:
                auteur.append(a.get_text())
        #"\s\s+", "", 
        
        #Recuperation dela date de publication et eventuellement d une date de modification
        dates = []
        for time in soup.find_all('time'):
            for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', str(time)):
                dates.append(date.datetime.strptime(valeur.group(0), '%d/%m/%Y'))

        #Recuperation de la date de publication de l article
        date_p = date.datetime.strftime(min(dates), '%d/%m/%Y')
        
        #Recuperation du contenu de l article
        contenu = ""
        for h2 in soup.find_all('h2'):
            if h2.get('class') == ['art-chapeau']:
                contenu += h2.get_text()+" "

        for div in soup.find_all('div'):
            if div.get('class') == ['art-text']:
                for p in div.find_all('p'):
                    contenu += p.get_text()+" "
        
        
        new_article = {
                "title" : titre,
                "newspaper" : 'Le Point.fr',
                "author" : auteur,
                "date_publi" : date_p,
                "content" : contenu,
                "theme" : theme
        }
        
        #Ajout de l article a la liste d articles
        fichier_json.append(new_article)

"""
Fonction prenant une url en entree
et retournant True si celle-ci est valide ou False sinon.
"""
def checkUrl(url):
    p = urlparse(url)
    conn = http.client.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400

fileTarget = '/var/www/html/projet2018'

#Adresse url Le Point
url_lepoint = 'http://www.lepoint.fr/'

#Parsing de la page d accueil avec Beautiful Soup
req = requests.get(url_lepoint)
data = req.text
soup = BeautifulSoup(data, "lxml")

#Creation de la liste des themes disponibles
links_themes_lepoint = []
for li in soup.find_all('li'):
    if li.get("class") == ['header-red-li']:
        for a in li.find_all('a'):
            if (a.get("href") != '/video/'
            and a.get("href") != 'http://afrique.lepoint.fr'
            and a.get("href") != '/edition-abonnes/'):
                links_themes_lepoint.append('http://www.lepoint.fr'+a.get("href"))


numero_article = 1
#Parcours des themes
for link_theme in links_themes_lepoint:
    url_lepoint_theme = link_theme;
    
    #Recuperation du theme
    theme = re.search("http://www.lepoint.fr/(.*)/", link_theme)[1]
     
    #Creation de la liste des articles du theme
    fichier_json=[]
    
    #Collecte des articles
    collect_articles(fichier_json, url_lepoint_theme)
    for index in range(2, 10):
        if checkUrl(url_lepoint_theme+"/index_"+str(index)):
            collect_articles(fichier_json, url_lepoint_theme+"/index_"+index)
        else:
            break
    
    #Creation du dossier contenant les articles
    sources = "LePointExistant/"
    cur_date = date.datetime.now().date()
    
    if not os.path.exists(fileTarget+sources):
        os.makedirs(fileTarget+sources)
    
    #Creation du fichier article et ajout dans le dossier
    for article in fichier_json:
        file_art = fileTarget + sources + "artlpt"+ str(numero_article) + str(cur_date) + "_robot.json"
        with open(file_art, "w", encoding="UTF-8") as fic:
            json.dump(article, fic, ensure_ascii=False)
        numero_article += 1