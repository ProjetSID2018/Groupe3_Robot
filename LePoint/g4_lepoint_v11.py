# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 12:30:00 2018
Group 4
@authors: Noemie DELOEUVRE, Morgan SEGUELA, Aurelien PELAT
V 1.1
"""

import time
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
import g4_utils_v40 as utils


def collect_url_themes(url_rss_lepoint):
    """Create a list containing the URL or the differents themes
    Arguments:
        url_rss_lepoint {string} -- url of the rss
    Returns:
        list_url_themes {list} -- list of URL (string)
    """
    req = requests.get(url_rss_lepoint)
    data = req.text
    soup = BeautifulSoup(data, "lxml")

    list_url_themes = []
    for a in soup.find_all("a"):
        if ("http://www.lepoint.fr/" in a.get("href")[0:22]
                and a.get("href") !=
                "http://www.lepoint.fr/content/system/rss/24H/24H_doc.xml"):
            list_url_themes.append(a.get("href"))

    return list_url_themes


def collect_url_articles(list_url_articles, url_theme):
    """Add the URL of all the articles from the URL of a theme in a list of URL
    Arguments:
        list_url_articles {list} -- list of URL
        url_theme {string} -- URL of a theme
    """
    req = requests.get(url_theme)
    data = req.text
    soup = BeautifulSoup(data, "lxml")

    items = soup.find_all("item")
    for item in items:
        list_url_articles.append(re.search(r"<link/>(.*)", str(item))[1])


def collect_articles(list_dictionaries, list_url_articles, theme):
    """Add the articles (dictionaries) from a list of URL in a list of
    dictionaries
    Arguments:
        list_dictionaries {list} -- list of dictionaries
        list_url_articles {list} -- list of URL
        theme {string} -- theme related to the list of dictionaries
    """
    for url_article in list_url_articles:
        try:
            req = requests.get(url_article)
            data = req.text
            soup = BeautifulSoup(data, "lxml")
    
            balise_title = soup.title.string
            sep = balise_title.split(" - Le Point")
            title = sep[0]
    
            list_authors = []
            for div in soup.find_all('div'):
                if div.get('class') == ['mbs']:
                    for span in div.find_all('span'):
                        name = span.get_text()
                        name = re.sub('Par', '', name)
                        name = re.sub("\s\s+", "", name)
            list_authors.append(name)
    
            dates = []
            for balise_time in soup.find_all('time'):
                for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',
                                          str(balise_time)):
                    dates.append(date.datetime.strptime(valeur.group(0),
                                                        '%d/%m/%Y'))
            date_publication = date.datetime.strftime(min(dates), '%d/%m/%Y')
            date_publication = str(date.datetime.strptime(date_publication,
                                                          "%d/%m/%Y").date())
    
            content = ''
            for h2 in soup.find_all('h2'):
                if h2.get('class') == ['art-chapeau']:
                    content += h2.get_text()+" "
            for div in soup.find_all('div'):
                if div.get('class') == ['art-text']:
                    for p in div.find_all('p'):
                        content += p.get_text()+" "
    
            new_article = utils.recovery_article(title, 'LePoint',
                                                 list_authors,
                                                 date_publication, content,
                                                 theme)
            if not utils.is_empty(new_article):
                list_dictionaries.append(new_article)

        except:
            print("Erreur lors de l'enregistrement de l'article")


def recovery_new_articles_lpt(file_target="data/clean/robot/" +
                              str(date.datetime.now().date()) + "/"):
    """Procedure that calls all the others functions and procedures in order to
    collect articles from a newspaper in a file
    Arguments:
        file_target {string} -- path where the articles will be recorded
    """
    list_url_themes = collect_url_themes('http://www.lepoint.fr/rss/')

    for url_theme in list_url_themes:

        list_url_articles = []

        list_dictionaries = []

        theme = re.search("http://www.lepoint.fr/(.*)/rss.xml", url_theme)[1]
        print("---------------------------"+theme+"------------------------")

        collect_url_articles(list_url_articles, url_theme)
        for index_page in range(2, 10):
            collect_url_articles(list_url_articles,
                                 url_theme+"index_"+str(index_page)+".php")

        collect_articles(list_dictionaries, list_url_articles, theme)
        time.sleep(3)

        utils.create_json(file_target, list_dictionaries, "LePoint/",
                          "lpt")


if __name__ == '__main__':
    recovery_new_articles_lpt()
