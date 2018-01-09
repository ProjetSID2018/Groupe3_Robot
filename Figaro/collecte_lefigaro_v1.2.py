import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re

fileTarget = "C:/Users/aurel/Documents/Etudes/ProjetIPJournaux/"

url_rss_figaro = "http://www.lefigaro.fr/rss/"

req = requests.get(url_rss_figaro)
data = req.text
soup = BeautifulSoup(data, "lxml")

items = soup.find_all("item")
links_themes_figaro = []
for span in soup.find_all("span"):
    if span.get("class") == ['boite2']:
        if ("http://www.lefigaro.fr/rss/figaro_" in span.find('a')['href']
        and "http://www.lefigaro.fr/rss/figaro_videos.xml" != span.find('a')['href']
        and "http://www.lefigaro.fr/rss/figaro_photos.xml" != span.find('a')['href']): 
            links_themes_figaro.append(span.find('a')['href'])

i = 1
for link_theme in links_themes_figaro:
    url_rss_figaro_theme = link_theme;
    
    theme = re.search("http://www.lefigaro.fr/rss/figaro_(.*).xml", link_theme)[1]
    #à supprimer, juste pour voir l'avancement
    print(theme)
    req = requests.get(url_rss_figaro_theme)
    data = req.text
    soup = BeautifulSoup(data, "lxml")
    
    
    
    items = soup.find_all("item")
    article_figaro = []
    for item in items:
        article_figaro.append(re.search(r"<link/>(.*)", str(item))[1])
    
    #Supprimer les lien d'articles vides dû au codage maladroit du site
    articles_figaro = []
    for article in article_figaro:
        if article != '':
            articles_figaro.append(article)
    
    fichier_json=[]
    for article in articles_figaro:
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
                "content" : contenu,
                "theme" : theme
        }
        
        fichier_json.append(new_article)
        
    sources = "LeFigaro/"
    cur_date = date.datetime.now().date()
    
    if not os.path.exists(fileTarget+sources):
        os.makedirs(fileTarget+sources)
    
    for article in fichier_json:
        file_art = fileTarget + sources + "artlfi"+ str(i) + str(cur_date) + "_robot.json"
        with open(file_art, "w", encoding="UTF-8") as fic:
            json.dump(article, fic, ensure_ascii=False)
        i += 1