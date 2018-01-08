import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re

###############Initialisation
fileTarget = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Projet_inter_promo/"
url_futurascience3 = "https://www.futura-sciences.com/sciences/dossiers/mathematiques-elegante-efficacite-symetries-1671/"
url_futurascience2 = "https://www.futura-sciences.com/sante/actualites/medecine-grippe-votre-annee-naissance-peut-vous-proteger-65227/"
url_futurascience = "https://www.futura-sciences.com/sciences/actualites/physique-physique-albert-einstein-domine-actualite-2017-69721/"
#la réponse (200_OK si tout va bien)
req = requests.get(url_futurascience)
#le html de réponse
data = req.text
#objet de type BeautifulSoup
soup = BeautifulSoup(data, "lxml")
#on indente
prettyHTML = soup.prettify()

###############Extraction
#title
title = soup.title.string
#newspaper
newspaper = 'FuturaSciences'
#for div in soup.find('div'):
    #if div.get("class") == 'OUTBRAIN':
    #newspaper = div.get('data-ob-template')
#author
author=''
for h3 in soup.find_all('h3'):
    if h3.get('itemprop') == 'author':
        author = h3.get_text()
#date_publi
date_publi = soup.time.string[11:]
################################
#TO DO : inclure les sous-titres
################################
#content
content = ''
for p in soup.find_all('p'):
    #print (p.get('class'))
    if p.get('class') not in (['zeta', 'bold', 'clearfix', 'description'],['ad-header'],['t-small'],['mt2', 't-small', 'color-white', 'display-inline-block', 'pt1'],['mt1'],['mt1', 'bold']):
        content += p.get_text()
content = content.replace(u'\xa0', u' ')
content = content.replace(u'\n', u' ')
#theme
theme=''
for h3 in soup.find_all('h3'):
    if h3.get('class') == 'zeta type-indicator text-uppercase mb1p5 color-white text-shadow':
        theme = h3.get_text()





















data = [{
    "title" : title,
    "newspaper" : newspaper,
    "author" : author,
    "date_publi" : date_publi,
    "content" : content,
    "theme" : theme
}]

print(data)