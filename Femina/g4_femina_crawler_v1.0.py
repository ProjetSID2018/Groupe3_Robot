# -*- coding: utf-8 -*-
# Group 4
# HERVE Pierrick
# DELOEUVRE Noémie
# SEGUELA Morgan
# V1

import os
import bs4
import requests
import unidecode
import re
import g4_utils_v2
import datetime as date

# Path to modify : target where we will store the json files
file_target = "C:/"
os.makedirs(file_target, exist_ok=True)

# we get the data from website
url_rss_femina = "http://www.femina.fr"
req = requests.get(url_rss_femina)
data = req.text
soup = bs4.BeautifulSoup(data, "lxml")

# we retrieve the categories
list_category = []
last_cat = ''
for div in soup.find_all('div'):
    if div.get('class') == ['menu_blocTitre']:
        for a in soup.find_all('a'):
            if div.a.get_text() != last_cat:
                list_category.append(div.a.get_text())
                last_cat = div.a.get_text()

# we retrieve the subcategories
list_sub_category = [' Maquillage ',
                      ' Coiffure ',
                      ' Beauté People ',
                      ' Parfums ',
                      ' Soins visage et corps ',
                      ' Tests & quiz Beauté ',
                      ' News ',
                      ' Tendances ',
                      ' Défilés ',
                      ' Lingerie ',
                      ' Mode People ',
                      ' Tests & quiz Mode ',
                      ' News ',
                      ' Recettes ',
                      ' Recettes de chefs ',
                      ' Idées de recettes par thème ',
                      ' Shopping et conseils ',
                      ' Générateur de menu ',
                      ' Nos Coups de Coeur Cuisine ',
                      ' News ',
                      ' Psycho ',
                      ' Société ',
                      ' Argent Droit ',
                      ' Tests & Quiz Psycho ',
                      ' Toute une Histoire ',
                      ' Vie des people ',
                      ' Mode People ',
                      ' Beauté People ',
                      ' Tests & Quiz People ',
                      ' News ',
                      ' Séries ',
                      ' Musique ',
                      ' Cinéma et DVD ',
                      ' Sorties ',
                      ' Coups de coeur des lectrices ',
                      ' Jardinage ',
                      ' Voyages ',
                      ' Tendance déco ',
                      ' News ',
                      ' Sexualité ',
                      ' Amour ',
                      ' Le kamasutra illustré ',
                      ' Questions / réponses sur les relations amoureuses ',
                      ' Tests & Quiz Sexo ',
                      ' News ',
                      ' Bien-être ',
                      ' Sport ',
                      ' Régimes / Nutrition ',
                      ' Santé ',
                      ' Tests & Quiz Forme ',
                      ' News ',
                      ' Grossesse ',
                      ' Bébé ',
                      ' Enfant ',
                      ' Adolescent ',
                      ' News ',
                      ' Les Rencontres Version Femina ']

# TODO: enlever les espaces avant et après pour les souscatégories


# We go through all the themes of the femina website and for each theme
# we get the articles of 6 pages (120 articles per theme)

file_json = []
for cat in list_category:
    # We retrieve the URL feeds for each page of article
    # Each HTML-coded article is analyzed with beautiful soup

# TODO: checkURL (voir lepoint)

# TODO: ne pas tester tous les couples (catégories, sous catégories) mais seulement les sous_cat correspondant à la catégorie en cours
    # we iterate on sub_categories
    for sub_cat in list_sub_category:
        # we iterate on pages (only the 10 first)
        # TODO: utiliser des while plutôt que des for pour traiter tous les
        # articles et ne pas rencontrer le bug "la page x n'existe pas"
        for i in range(10):
            #print(type(i))
            if i == 1:
                url_rss_femina = "http://www.femina.fr/" + cat + "/" + sub_cat
            else:
                #print('cat : ',type(cat))
                #print('sub_cat : ',type(sub_cat),sub_cat)
                #print('i : ',type(str(i)))
                url_rss_femina = "http://www.femina.fr/" + cat + "/" + sub_cat + "/page-"+ str(i+1)
            req = requests.get(url_rss_femina)
            data = req.text
            soup = bs4.BeautifulSoup(data, "lxml")
            items = soup.find_all("item")
            article_femina = []

            # We retrieve all the articles for a given page
            for link in soup.find_all("comments"):
                article_femina.append(link.string[:-10])


# we get the data from website
url_rss_femina = "https://www.femina.com"
rss_url = "http://feeds.feedburner.com/FeminaNews"
req = requests.get(rss_url)
data = req.text
soup = bs4.BeautifulSoup(data, "lxml")

# table of JSON objects
jsons = []

for article in article_femina:
    # the response (200_OK if everything is ok)
    req = requests.get(url_rss_femina+article)
    # we get the body of the response
    data = req.text
    # a BeautifulSoup object
    soup = bs4.BeautifulSoup(data, "lxml")
    # we indent
    pretty_html = soup.prettify()

    # we get the title
    title = soup.title.string

    # we get the newspaper name
    newspaper = 'Femina'

    # we get the author
    author = []
    for meta in soup.find_all('meta'):
        if meta.get('property') == 'article:author':
            author.append(meta.get('content'))

    # we get the publication date
    for div in soup.find_all('div'):
        if div.get("class") == ['infos']:
            for valeur in re.finditer('[0-9]{4}-[0-9]{2}-[0-9]{2}',
                                      str(div.get('datetime'))):
                publi_date = date.datetime.strptime(div.get('datetime'),
                                                    '%d/%m/%Y')

    # récupération du contenu
    content = ''
    for p in soup.find_all('p'):
        content += p.get_text()
    # we traduce in utf-8
    content = unidecode.unidecode(content)

    # récupération du theme
    theme = ''
    for meta in soup.find_all('meta'):
        if meta.get('property') == 'og:url':
            tmp = meta.get('content')[21:]
            indice = tmp.find('/')
            theme = tmp[:indice]

    # creation of the JSON object
    new_article = [{
        "title": title,
        "newspaper": newspaper,
        "author": author,
        "date_publi": publi_date,
        "content": content,
        "theme": theme
    }]
    jsons.append(new_article)
    print(len(jsons))


# creation of the file
g4_utils_v2.create_json("C:/", jsons, "Femina/", "fem")
