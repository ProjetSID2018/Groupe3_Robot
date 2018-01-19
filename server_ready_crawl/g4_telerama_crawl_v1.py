#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Groupe 4
 SECK Mamadou
 V0 : create code
 V1 : create function
"""
import os
import json
import datetime as date
import re
import g4_utils_v33 as utils

# Verifier si le tag contient le texte Copyright


def has_copyright(tag):
    """
        Verifier si le contenu de la balise contient le mot cle "copyright"
    """
    return "Copyright" in tag.get_text()


def get_article_of_category(url):
    """
        Prend en parametre une catégorie et retour toutes les articles de cette catégorie
    """
    result = []
    soup = utils.recovery_flux_url_rss(url)
    articles = soup.find_all("div", class_="item--body")
    for article in articles:
        url_article = article.find("a").get("href")
        if is_article(url_article):
            result.append(get_article(url_article))
    return result


def get_article(url):
    """
        Prend en argument une adresse url (url) et retourne un dictionnaire
    """
    from unidecode import unidecode
    soup = utils.recovery_flux_url_rss(url)
    article = soup.find("article")
    meta = soup.find("meta", property="og:title").get("content")
    tab = meta.split("-")
    n = len(tab)
    newspaper = tab[n - 1]
    theme = tab[n - 2]
    title = "-".join(tab[:n - 2])
    authors = []
    regex = re.compile(r'[\n\r\t]')
    for span in article.find_all("span", class_="author--name"):
        author = regex.sub("", unidecode(span.get_text()))
        authors.append(author.strip())
    date_pub = article.find("span", itemprop="datePublished").get(
        "datetime")[:10].replace("-", "/")
    content = ""
    for div in article.find_all(
        "div",
        class_=[
            "article--intro",
            "article--wysiwyg",
            "article--footnotes"]):
        for p in div.find_all("p"):
            content = content + p.get_text()
    content = regex.sub("", content)
    return utils.recovery_article(
        unidecode(title),
        unidecode(newspaper),
        authors,
        date_pub,
        unidecode(content),
        unidecode(theme))


def is_article(url):
    """
        Prend en argument une adresse url et retourne vrai s'il est une 
        article et faux sinon
    """
    soup = utils.recovery_flux_url_rss(url)
    return soup.find("div", class_="article--text") is not None


def add_articles(
        file_target="/home/etudiant/Documents/ProjetSID/Groupe4_Robot/Telerama/Art/" +
        str(
            date.datetime.now().date()) +
        "/"):
    """
        it create a json for each new article
    """
    categories = {
        "cinema": 40,
        "scenes": 30,
        "enfants": 3,
        "idees": 30,
    }
    articles = []
    for category, nbre in categories.items():
        for i in range(0, nbre):
            url = "http://www.telerama.fr/" + \
                category + "/articles?page=" + str(i)
            articles.extend(get_article_of_category(url))
            utils.create_json(file_target, articles, "Telerama/", "tera")


if __name__ == '__main__':
    add_articles()
