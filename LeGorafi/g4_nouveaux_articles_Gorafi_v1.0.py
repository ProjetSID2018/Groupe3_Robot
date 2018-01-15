# -*- coding: utf-8 -*-
"""
 Group 4
 Realized by BENJEBRIA Sofian, DELOEUVRE Noémie, MOTHES Céline Mothes,
             SEGUELA Morgan
 V1 : create code
 V1.1 : create function
"""

import re
import g4_utils_v32 as utils

# Path to change : target where we will store the json files
file_target = "/var/www/html/projet2018/data/clean/robot/"
+ str(date.datetime.now().date()) + "/"
os.makedirs(file_target, exist_ok=True)

url_rss_gorafi = "http://www.legorafi.fr/feed/"

# We retrieve the URL feeds for each new article
# Each HTML-coded article is analyzed with beautiful soup
soup = utils.recovery_flux_url_rss(url_rss_gorafi)
items = soup.find_all("item")
article_gorafi = []

# We're picking up every new item in a list
for item in items:
    article_gorafi.append(re.search(r"<link/>(.*)", str(item))[1])
file_json = []

for article in article_gorafi:
    soup = utils.recovery_flux_url_rss(article)

    balise_title = soup.title.string
    sep = balise_title.split("—")
    title = sep[0]
    newspaper = sep[1]

    author = []

    # Recovery of author and publication date
    for span in soup.find_all('span'):
        if span.get("class") == ['context']:
            author.append(span.a.get_text())
            for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',
                                      str(span)):
                date_p = valeur.group(0)

    # Retrieving the theme
    for ul in soup.find_all('ul'):
        if ul.get("class") == ['post-categories']:
            for li in ul.find_all('li'):
                theme = li.get_text()
    contents = ""

    # Récupération du contenu de l'article
    for div in soup.find_all('div'):
        if div.get("class") == ['content']:
            for p in div.find_all('p'):
                contents += p.get_text() + " "
    new_article = recovery_article(title, "Le Gorafi", author, date_p,
                                   contents, theme)

    if theme != "Magazine":
        file_json.append(new_article)

sources = "legorafi/"

# Call the create_json function
g4_utils_v2.create_json(file_target, file_json, sources, "lg")
