#Groupe 10
#MOTHES Céline
#HERVE Pierrick
#V1

import bs4
import requests
import unidecode
import re

###############Initialisation
fileTarget \
= "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Projet_inter_promo/"
futurascience_url \
= "https://www.futura-sciences.com/sciences/dossiers/mathematiques-elegante- \
efficacite-symetries-1671/"
futurascience_url2 \
= "https://www.futura-sciences.com/sciences/actualites/physique-physique- \
albert-einstein-domine-actualite-2017-69721/"
futurascience_url3 \
= "https://www.futura-sciences.com/sante/dossiers/sommeil-rever-monde- \
fascinant-reves-1281/page/2/"
futurascience_url4 \
= "https://www.futura-sciences.com/tech/videos/bitcoin-ca-marche-4392/"


#la réponse (200_OK si tout va bien)
req = requests.get(futurascience_url4)
#le html de réponse
data = req.text
#objet de type BeautifulSoup
soup = bs4.BeautifulSoup(data, "lxml")
#on indente
prettyHTML = soup.prettify()


#récupération titre
title = soup.title.string
indice = title.find('|')
if indice != -1:
    title = title[:indice-1]
else:
    title = soup.title.string
    
#récupération du journal
newspaper = 'FuturaSciences'

#récupération de l'auteur
author=[]
for h3 in soup.find_all('h3'):
    if h3.get('itemprop') == 'author':
        author.append(h3.get_text())
        
#récupération de la date de publication
publi_date = soup.time.string[11:]

content = ''
for p in soup.find_all('p'):
    for p2 in re.finditer('py0p5', p.get('class')[-1]):
        content += p.get_text()
#traduction en utf-8
content = unidecode.unidecode(content)

#récupération du theme
theme=''
for meta in soup.find_all('meta'):
    if meta.get('property') == 'og:url':
        tmp = meta.get('content')[32:]
        indice = tmp.find('/')
        theme = tmp[:indice]
        
#création du json
data = [{
    "title" : title,
    "newspaper" : newspaper,
    "author" : author,
    "date_publi" : publi_date,
    "content" : content,
    "theme" : theme
}]