# Groupe 10
# MOTHES Céline
# HERVE Pierrick
# V1

import bs4
import requests
import unidecode
import re
# TODO: appeler la fonction create_json après Merge dans la branche Master
import G4_create_json


fileTarget = "C:/"

url_rss_gorafi = "https://www.futura-sciences.com"
rss_url = "https://www.futura-sciences.com/flux-rss/"
req = requests.get(rss_url)
data = req.text
soup = bs4.BeautifulSoup(data, "lxml")

articles = []
for link in soup.find_all("a"):
    if link.get("class") == ["first-capitalize"]:
        articles.append(link.get("href"))

jsons = []

for article in articles:
    # la réponse (200_OK si tout va bien)
    req = requests.get(url_rss_gorafi+article)
    # le html de réponse
    data = req.text
    # objet de type BeautifulSoup
    soup = bs4.BeautifulSoup(data, "lxml")
    # on indente
    prettyHTML = soup.prettify()


    # récupération titre
    title = soup.title.string
    indice = title.find('|')
    if indice != -1:
        title = title[:indice-1]
    else:
        title = soup.title.string

    # récupération du journal
    newspaper = 'FuturaSciences'
    
    # récupération de l'auteur
    author = []
    for h3 in soup.find_all('h3'):
        if h3.get('itemprop') == 'author':
            author.append(h3.get_text())

    # récupération de la date de publication
    publi_date = soup.time.string[11:]
    
    content = ''
    for p in soup.find_all('p'):
        for p2 in re.finditer('py0p5', p.get('class')[-1]):
            content += p.get_text()
    # traduction en utf-8
    content = unidecode.unidecode(content)
    
    # récupération du theme
    theme = ''
    for meta in soup.find_all('meta'):
        if meta.get('property') == 'og:url':
            tmp = meta.get('content')[32:]
            indice = tmp.find('/')
            theme = tmp[:indice]
        
    # création du json
    new_article = [{
        "title": title,
        "newspaper": newspaper,
        "author": author,
        "date_publi": publi_date,
        "content": content,
        "theme": theme
    }]
    jsons.append(new_article)


G4_create_json.create_json("C:/", jsons, "FuturaSciences/", "fusc")
