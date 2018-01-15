# Group 4
# Realized by BESNARD Léa

import os
import datetime as datetime
from bs4 import BeautifulSoup
import requests
import re
import unidecode
import g4_utils_v31 as utilsg4



def recuperation_info_lt(file_target = "C:/Users/lea/Desktop/PROJET/" + str(date.datetime.now().date()) +"/"):
    url_rss_latribune = "http://www.latribune.fr/rss/rubriques/actualite.html"
    articles = article_lt(url_rss_latribune)
    file_json = fileJson(articles)
    sources = "Latribune_articles_nouveaux/"
    if not os.path.exists(file_target+sources):
        os.makedirs(file_target+sources)
    # Call the create_json function
    utilsg4.create_json(file_target, file_json, sources, "lt")
        

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
        req = requests.get(article)
        data = req.text
        soup = BeautifulSoup(data, "lxml")
        # Retrieve the title
        title = soup.title.string
        
        # Retrieve the theme
        #theme = ""
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
                for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', str(time)):
                    date = valeur.group(0)
        
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
        file_json.append(new_article)
    return(file_json)
    
if __name__ == '__main__':
    recuperation_info_lt()
