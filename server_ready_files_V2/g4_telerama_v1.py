#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Groupe 4
 SECK Mamadou
 V0 : create code
 V1 : create function
"""
import datetime as date
import re
import g4_utils_v40 as utils

# Verifier si le tag contient le texte Copyright


def has_copyright(tag):
    """
        Check if the content of the tag contains the keyword "copyright"  
    """
    return "Copyright" in tag.get_text()


def get_article_of_category(url):
    """
        Arguments :
            - Category
        Returns :
            - All articles of this category
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
        Arguments :
            - URL address
        Returns :
            - Dictionnary
    """
    from unidecode import unidecode
    soup = utils.recovery_flux_url_rss(url)
    article = soup.find("article")
    meta = soup.find("meta", property="og:title").get("content")
    tab = meta.split("-")
    n = len(tab)

    theme = tab[n - 2]

    title = "-".join(tab[:n - 2])

    authors = []
    regex = re.compile(r'[\n\r\t]')
    for span in article.find_all("span", class_="author--name"):
        author = regex.sub("", unidecode(span.get_text()))
        authors.append(author.strip())

    date_pub = article.find("span", itemprop="datePublished").get(
        "datetime")[:10].split("-")
    date_pub = date_pub[2] + "-" + date_pub[1] + "-" + date_pub[0]

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
    return utils.recovery_article(title, "Telerama", authors, date_pub,
                                  content, theme)


def is_article(url):
    """
        Prend en argument une adresse url et retourne
        vrai s'il est une article et faux sinon
    """
    soup = utils.recovery_flux_url_rss(url)
    return soup.find("div", class_="article--text") is not None


def add_articles(
        file_target="/home/etudiant/Documents/ProjetSID/Groupe4_Robot/" +
                    "Telerama/Art/" + str(date.datetime.now().date()) + "/"):
    """
        it create a json for each new article
    """
    categories = {
        "cinema": 5,
        "scenes": 5,
        "enfants": 5,
        "idees": 5,
    }
    articles = []
    for category, nbre in categories.items():
        for i in range(0, nbre):
            url = "http://www.telerama.fr/" + \
                category + "/articles?page=" + str(i)
            new_article = get_article_of_category(url)
            if utils.is_empty(new_article) is False:
                articles.append(new_article)
    utils.create_json(file_target, articles, "Telerama/", "tera")


if __name__ == '__main__':
    add_articles()
