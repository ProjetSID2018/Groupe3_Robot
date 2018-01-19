# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 16:16:07 2018

@author: aurel
"""
import time
import g4_utils_v40 as utils
import datetime as date
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import unidecode
import requests


def collect_url_articles(url_liberation):

    driver = webdriver.PhantomJS(executable_path="/var/www/html/projet2018/code/robot/phantom.js")
    time.sleep(2)

    for scroll in range(1000):
        driver.execute_script("window.scrollTo(0, 100000)")

    html_loaded = driver.page_source

    soup = BeautifulSoup(html_loaded, "lxml")

    list_url_articles = []
    for a in soup.find_all('a', attrs={'class': 'home-une-link'}):
        if 'http://' in a.get('href'):
            list_url_articles.append(a.get('href'))
        else:
            list_url_articles.append('http://www.liberation.fr' + a.get('href'))
    for a in soup.find_all('a', attrs={'class': 'live-link'}):
        if 'http://' in a.get('href'):
            list_url_articles.append(a.get('href'))
        else:
            list_url_articles.append('http://www.liberation.fr' + a.get('href'))

    return list_url_articles


def collect_article(article_link):
    """Extact informations from all these articles

    Arguments:
        article_link {string} -- url of an article

    Returns:
        dict -- dict of all informations
    """

    if "video" in article_link or "/apps/" in article_link or "checknews" in article_link or not re.search(r"\d\d\d\d/\d\d/\d\d", article_link):
        return None

    else:
        req = requests.get(article_link)
        data = req.text
        soup = BeautifulSoup(data, "lxml")
        try:
            theme = re.search("http://www.liberation.fr/(.*)", article_link)[1]
            theme = theme.split('/')[0]
        except:
            theme = ''

        if soup.find("div", class_ = "direct-headband") or article_link != req.url:
            return None
        else:               
            balise_title = soup.find("h1")
            balise_title = balise_title.get_text()
            balise_title = re.sub(r"\s\s+", "", balise_title)

            newspaper = "Liberation"
            title = unidecode.unidecode(balise_title)

            date_p = ""
            authors = []
            for span in soup.find_all('span'):
                if span.get("class") == ['author']:
                    if(span.a):
                        author = span.a.string
                        if author:
                            authors.append(author) 
                if span.get("class") == ['date']:
                    if(span.time):
                        date_p = date.datetime.strptime(span.time.get("datetime"),"%Y-%m-%dT%H:%M:%S").date()
                        date_p = date_p.strftime("%d/%m/%Y")
            date_p = str(date.datetime.strptime(date_p,
                                                "%d/%m/%Y").date())
            if not authors:
                authors = ["liberation"]

            content = ""        
            for div in soup.find_all('div'):
                for p in div.find_all('p'):
                    content += p.get_text() + " "
            content = re.sub("<>", "", content)
            content = unidecode.unidecode(content)
            
            new_article = utils.recovery_article(title, newspaper, authors, date_p, content, theme)
            
            return new_article

def recovery_new_articles_libe(file_target="/var/www/html/projet2018/data/clean/robot/" +
                               str(date.datetime.now().date()) + "/"):
    """Procedure that calls all the others functions and procedures in order to
    collect articles from a newspaper in a file
    Arguments:
        file_target {string} -- path where the articles will be recorded
    """
    list_dictionaries = []

    list_url_articles = collect_url_articles('http://www.liberation.fr/')

    number_articles = 0
    for url_article in list_url_articles:
        article = collect_article(url_article)
        if article != None:
            list_dictionaries.append(article)
            # Buffer
            number_articles += 1
            if number_articles % 50 == 0:
                utils.create_json(file_target, list_dictionaries, 'Liberation/',
                                  'libe')
                list_dictionaries.clear()
    utils.create_json(file_target, list_dictionaries, 'Liberation/', 'libe')


if __name__ == '__main__':
    recovery_new_articles_libe()
