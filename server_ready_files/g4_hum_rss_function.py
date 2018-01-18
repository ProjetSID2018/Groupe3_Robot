#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Group 4
# Realized by DELOEUVRE Noémie

import g4_utils_v40 as utils
import re
from datetime import datetime
import datetime as date


def recovery_information_hum(url_article):
    """
        Arguments:
            - url of one article
        Returns:
            - informations of the article
    """
    soup_article = utils.recovery_flux_url_rss(url_article)

    for meta in soup_article.find_all('meta'):
        if meta.get("property") == 'og:title':
            title = meta.get("content")

    for meta in soup_article.find_all('meta'):
        if meta.get("property") == 'article:section':
            theme = meta.get("content")

    author = []
    for h2 in soup_article.find_all('h2'):
        for a in h2.find_all('a'):
            if re.search('auteur', str(a.get("href"))):
                author.append(a.get_text())

    for meta in soup_article.find_all('meta'):
        if meta.get("property") == 'article:published_time':
            raw_date = meta.get("content")
            date_p = raw_date[0:10]
            date_p = datetime.strptime(date_p, "%Y-%m-%d")

    contents = ""
    for div in soup_article.find_all('div'):
        if div.get("class") == ['field', 'field-name-field-news-chapo', 'field-type-text-long', 'field-label-hidden']:
            for p in div.find_all('p'):
                contents += p.get_text()
        if div.get("class") == ['field', 'field-name-field-news-text', 'field-type-text-long', 'field-label-hidden']:
            for p in div.find_all('p'):
                contents += p.get_text()

    article = utils.recovery_article(title, 'Humanite',
                                     author, date_p, contents, theme)
    return(article)


def recovery_link_new_articles_hum_rss(url_rss):
    """
        Arguments:
            - url of the page containing feed links for
            the different categories
        Returns :
            - list of urls of the different categories

    """
    soup = utils.recovery_flux_url_rss(url_rss)

    items = soup.find_all("item")
    article_humanite = []
    # Retrieving all urls of new RSS feeds of different categories
    for item in items:
        article_humanite.append(re.search(r"<link/>(.*)", str(item))[1])

    return(article_humanite)


def recovery_new_articles_hum_rss(file_target="data/clean/robot/" +
                                  str(date.datetime.now().date()) + "/"):
    """
        Returns:
            - creation of a json for each new article
    """
    file_json = []
    i = 0
    # Each url is analized one by one
    article_humanite = recovery_link_new_articles_hum_rss("https://www." +
                                                          "humanite.fr/rss/" +
                                                          "actu.rss")
    for article in article_humanite:
        new_article = recovery_information_hum(article)
        if utils.is_empty(new_article) is False:
            file_json.append(new_article)
            i += 1
        if i == 20:
            utils.create_json(file_target, file_json, "Humanite_rss/",
                              "hum")
            i = 0
            file_json = []

    utils.create_json(file_target, file_json, "Humanite_rss/",
                      "hum")


if __name__ == '__main__':
    recovery_new_articles_hum_rss()
