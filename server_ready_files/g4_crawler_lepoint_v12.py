# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 8:30:00 2018
Group 4
@authors: Noemie DELOEUVRE, Morgan SEGUELA, Celine Mothes, Aurelien PELAT
V 1.2
"""

import time
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
import g4_utils_v34 as utils


def collect_url_themes(url_lepoint):
    """Create a list containing the URL or the differents themes
    Arguments:
        url_lepoint {string} -- url of the newspaper Le Point.fr

    Returns:
        list_url_themes {list} -- list of URL (string)
    """
    req = requests.get(url_lepoint)
    data = req.text
    soup = BeautifulSoup(data, "lxml")

    list_url_themes = []
    for li in soup.find_all('li'):
        if li.get("class") == ['header-red-li']:
            for a in li.find_all('a'):
                if (a.get("href") != '/video/'
                        and a.get("href") != 'http://afrique.lepoint.fr'
                        and a.get("href") != '/edition-abonnes/'):
                    list_url_themes.append('http://www.lepoint.fr' +
                                           a.get("href"))
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

    for div in soup.find_all('div'):
        if div.get('class') == ['list-view']:
            for a in div.find_all('a'):
                if ('http' in a.get('href')
                        and a.get('href') not in list_url_articles):
                    list_url_articles.append(a.get('href'))
                elif ('http' not in a.get('href')
                        and 'http://www.lepoint.fr' + a.get('href')
                        not in list_url_articles):
                    list_url_articles.append('http://www.lepoint.fr' +
                                             a.get('href'))


def collect_articles(list_dictionaries, list_url_articles, theme):
    """Add the articles (dictionaries) from a list of URL in a list of
    dictionaries
    Arguments:
        list_dictionaries {list} -- list of dictionaries
        list_url_articles {list} -- list of URL
        theme {string} -- theme related to the list of dictionaries
    """
    for url_article in list_url_articles:
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

        if (title != ''
                and len(list_authors) != 0
                and date_publication != ''
                and content != ''
                and theme != ''):
            print(title)
            new_article = utils.recovery_article(title, 'LePoint',
                                                 list_authors,
                                                 date_publication, content,
                                                 theme)
        list_dictionaries.append(new_article)


def recovery_new_articles_lpt(file_target="data/clean/robot/" +
                              str(date.datetime.now().date()) + "/"):
    """Procedure that calls all the others functions and procedures in order to
    collect articles from a newspaper in a file
    Arguments:
        file_target {string} -- path where the articles will be recorded
    """
    list_url_themes = collect_url_themes('http://www.lepoint.fr/')

    list_url_articles = []

    list_dictionnaires = []

    for url_theme in list_url_themes:

        theme = re.search("http://www.lepoint.fr/(.*)/", url_theme)[1]
        print("---------------------------"+theme+"------------------------")

        collect_url_articles(list_url_articles, url_theme)
        for index_page in range(2, 10):
            collect_url_articles(list_url_articles,
                                 url_theme+"index_"+str(index_page)+".php")

        collect_articles(list_dictionnaires, list_url_articles, theme)
        time.sleep(3)

    utils.create_json(file_target, list_dictionnaires, "LePointExistant/",
                      "lpt")


if __name__ == '__main__':
    recovery_new_articles_lpt()