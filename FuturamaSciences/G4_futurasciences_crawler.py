# -*- coding: utf-8 -*-
# Group 4
# MOTHES Céline
# HERVE Pierrick
# V1

import bs4
import requests
import unidecode
import re
import utils

fileTarget = "C:/"

# we get the data from website
url_rss_futurasciences = "https://www.futura-sciences.com"
rss_url = "https://www.futura-sciences.com/flux-rss/"
req = requests.get(rss_url)
data = req.text
soup = bs4.BeautifulSoup(data, "lxml")

# we find new articles
articles = []
for link in soup.find_all("a"):
    if link.get("class") == ["first-capitalize"]:
        articles.append(link.get("href"))

# table of JSON objects
jsons = []

for article in articles:
    # the response (200_OK if everything is ok)
    req = requests.get(url_rss_futurasciences+article)
    # we get the body of the response
    data = req.text
    # a BeautifulSoup object
    soup = bs4.BeautifulSoup(data, "lxml")
    # we indent
    prettyHTML = soup.prettify()

    # we get the title
    title = soup.title.string
    indice = title.find('|')
    if indice != -1:
        title = title[:indice-1]
    else:
        title = soup.title.string

    # we get the newspaper name
    newspaper = 'FuturaSciences'

    # we get the author
    author = []
    for h3 in soup.find_all('h3'):
        if h3.get('itemprop') == 'author':
            author.append(h3.get_text())

    # we get the publication date
    publi_date = soup.time.string[11:]

    content = ''
    for p in soup.find_all('p'):
        for p2 in re.finditer('py0p5', p.get('class')[-1]):
            content += p.get_text()
    # we traduce in utf-8
    content = unidecode.unidecode(content)

    # we get the theme
    theme = ''
    for meta in soup.find_all('meta'):
        if meta.get('property') == 'og:url':
            tmp = meta.get('content')[32:]
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

sources = "FuturaSciences/"

# creation of the file
utils.create_json("C:/", jsons, sources, "fusc")
