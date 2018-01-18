# Group 4
# Realized by BESNARD Léa

import os
from datetime import datetime
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
import g4_utils_v40 as utils


def recuperation_info_lt(file_target="data/clean/robot/" +
                         str(date.datetime.now().date()) + "/"):
    url_rss_latribune = "http://www.latribune.fr/rss/rubriques/actualite.html"
    articles = article_lt(url_rss_latribune)
    file_json = fileJson(articles)
    sources = "Latribune/"
    if not os.path.exists(file_target + sources):
        os.makedirs(file_target + sources)
    # Call the create_json function
    utils.create_json(file_target, file_json, sources, "lt")


def article_lt(url_rss_lt):
    # We retrieve the URL feeds for each new article
    # Each HTML-coded article is analyzed with beautiful soup
    req = requests.get(url_rss_lt)
    data = req.text
    soup = BeautifulSoup(data, "lxml")
    items = soup.find_all("item")
    article_latribune = []
    # We're picking up every new item in a list
    for item in items:
        article_latribune.append(re.search(r"<link/>(.*)", str(item))[1])
    return article_latribune


def fileJson(article_latribune):
    file_json = []
    for article in article_latribune:
        soup = utils.recovery_flux_url_rss(article)
        # Retrieve the title
        title = soup.title.string

        # Retrieve the theme
        for li in soup.find_all('li'):
            if li.get("itemprop") == 'itemListElement':
                theme = li.a.span.get_text()

        # Retrieve the author
        author = []
        for span in soup.find_all('span'):
            if span.get("class") == ['author-name']:
                author.append(span.a.span.get_text())

        # Retrieve the publication date
        for time in soup.find_all('time'):
            if time.get("itemprop") == 'datePublished':
                date = time.get("itemprop")
                for valeur in re.finditer(
                        '[0-9]{2}\/[0-9]{2}\/[0-9]{4}', str(time)):
                    date = valeur.group(0)
                    date = datetime.strptime(date, "%d/%m/%Y")\
                        .strftime("%Y-%m-%d")
        print(date)

        # Retrieve the content
        content = ""
        for div in soup.find_all('div'):
            if div.get("itemprop") == 'articleBody':
                for p in div.find_all('p'):
                    content += p.get_text() + " "

        new_article = {
            "title": title,
            "newspaper": "La tribune",
            "author": author,
            "date_publi": date,
            "content": content,
            "theme": theme
        }
        # add each new article in the "file_json" table
        if utils.is_empty(new_article) is False:
            file_json.append(new_article)
    return(file_json)


if __name__ == '__main__':
    recuperation_info_lt()
