# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 16:16:07 2018

@author: aurel
"""
import g4_utils_v40 as utils
import datetime as date


def collect_url_articles(url_liberation):
    soup = utils.recovery_flux_url_rss(url_liberation)

    list_url_articles = []
    for a in soup.find_all('a', attrs={'class': 'home-une-link'}):
        if 'http://' in a.get('href'):
            list_url_articles.append(a.get('href'))
        else:
            list_url_articles.append('www.liberation.fr' + a.get('href'))
    for a in soup.find_all('a', attrs={'class': 'live-link'}):
        if 'http://' in a.get('href'):
            list_url_articles.append(a.get('href'))
        else:
            list_url_articles.append('www.liberation.fr' + a.get('href'))

    return list_url_articles


def collect_article(url_article):
    pass


def recovery_new_articles_libe(file_target="data/clean/robot/" +
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
        list_dictionaries.append(collect_article(url_article))
        # Buffer
        number_articles += 1
        if number_articles % 50 == 0:
            utils.create_json(file_target, list_dictionaries, 'Liberation/',
                              'libe')
            list_dictionaries.clear()
    utils.create_json(file_target, list_dictionaries, 'Liberation/', 'libe')


if __name__ == '__main__':
    recovery_new_articles_libe()
