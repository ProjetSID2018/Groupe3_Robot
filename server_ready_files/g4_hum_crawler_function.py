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


def recovery_link_new_articles_hum_crawler():
    """
        Arguments:
            - url of the page containing feed links for
            the different categories
        Returns :
            - list of urls of the different categories

    """
    list_category = ["politique", "société", "social-eco", "culture", "sports",
                     "monde", "environnement", "rubriques/en-debat"]

    article_humanite = []
    for cat in list_category:
        # We retrieve the URL feeds for each page of article
        # Each HTML-coded article is analyzed with beautiful soup
        for i in range(2, 10):
            url_rss_humanite = "https://humanite.fr/" + cat + "?page=" +\
                str(i) + "/feed/"
            soup_url = utils.recovery_flux_url_rss(url_rss_humanite)
            # We retrieve all the articles for a given page
            for div in soup_url.find_all('div'):
                if re.search('field-name-field-news-chapo',
                             str(div.get("class"))):
                    for a in div.find_all('a'):
                        article_humanite.append(a.get("href"))

    return(article_humanite)


def recovery_new_articles_hum_crawler(file_target="data/clean/robot/" +
                                      str(date.datetime.now().date()) + "/"):
    """
        Returns:
            - creation of a json for each new article
    """
    file_json = []
    article_humanite = recovery_link_new_articles_hum_crawler()
    # Each url is analized one by one
    i = 0
    for article in article_humanite:
        new_article = recovery_information_hum(article)
        if utils.is_empty(new_article) is False:
            file_json.append(new_article)
            i += 1
        if i == 20:
            utils.create_json(file_target, file_json, "Humanite_crawler/",
                              "hum")
            i = 0
            file_json = []

    utils.create_json(file_target, file_json, "Humanite_crawler/",
                      "hum")


if __name__ == '__main__':
    recovery_new_articles_hum_crawler()
