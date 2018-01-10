# -*- coding: utf-8 -*-
# Group 4
# HERVE Pierrick
# V1

import bs4
import requests
import unidecode
import re
import g4_utils_v2
import datetime as date

fileTarget = "C:/"

# we get the data from website
url_rss_femina = "https://www.femina.com"
rss_url = "http://feeds.feedburner.com/FeminaNews"
req = requests.get(rss_url)
data = req.text
soup = bs4.BeautifulSoup(data, "lxml")

# we find new articles
articles = []
for link in soup.find_all("comments"):
    articles.append(link.string[:-10])

# table of JSON objects
jsons = []

for article in articles:
    # the response (200_OK if everything is ok)
    req = requests.get(url_rss_femina+article)
    # we get the body of the response
    data = req.text
    # a BeautifulSoup object
    soup = bs4.BeautifulSoup(data, "lxml")
    # we indent
    prettyHTML = soup.prettify()

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
