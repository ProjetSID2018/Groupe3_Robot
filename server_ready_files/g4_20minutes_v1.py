#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" -*- coding: utf-8 -*-
 Groupe 4
 SECK Mamadou
 V0 : create code
 V1.1 : create function
"""
import datetime as date
from unidecode import unidecode
import re
import g4_utils_v40 as utils


# Verifier si le tag contient le texte Copyright
def has_copyright(tag):
    """
        Check if the content of the tag contains the keyword "copyright"
    """
    return "Copyright" in tag.get_text()


def get_article(url):
    """
    Arguments :
        - URL address
    Returns :
        - An article
        {
            "title" : str,
            "newspaper" : str,
            "author" : [str],
            "date_publi" : str,
            "content" : str,
            "theme" : str
            }
    """
    soup = utils.recovery_flux_url_rss(url)
    article = soup.find("article")
    # Titre de l'article
    title = article.find("h1").get_text()

    # tableau vide quand il y'a pas d'autheur sinon tableau de(s) auteur(s)
    authors = [] if article.find("header") .find(
        "p", class_="authorsign-label") is None else unidecode(
        article.find("header") .find(
            "p", class_="authorsign-label").get_text()).split(" et ")

    # Date de publication de l'article
    date_pub = article.find("time").get("datetime")[:10]

    # Theme de l'article
    theme = article.find("ol", class_="breadcrumb-list")\
        .find_all("li")[1].find("span").get_text()

    # Contenu de l'article
    content = ""
    for p in article.find("div", class_="content").find_all("p"):
        content = content + p.get_text() + " "

    # Nom du journal
    newspaper = soup.find("footer").find(has_copyright).find("a").get_text()
    regex = re.compile(r'[\n\r\t]')
    # Elever les \n \r \t du contenu
    content = regex.sub("", content)
    return utils.recovery_article(
        unidecode(title),
        unidecode(newspaper),
        authors,
        str(date_pub),
        unidecode(content),
        unidecode(theme))


def is_article(url):
    """
        Arguments :
            - URL address
        Returns :
            - True if the page contains an article
            - False otherwise
    """
    soup = utils.recovery_flux_url_rss(url)
    article = soup.find("article")
    return article is not None


def add_articles(file_target="data/clean/robot/" +
                 str(date.datetime.now().date()) + "/"):
    """
        it create a json for each new article
    """
    soup = utils.recovery_flux_url_rss(
        "http://www.20minutes.fr/feeds/rss-actu-france.xml")
    items = soup.find_all("item")
    articles = []
    for item in items:
        # Récuperer le lien des articles
        url = re.search(r"<link/>(.*)<pubdate>", str(item)).group(1)
        if is_article(url):
            new_article = get_article(url)
            if utils.is_empty(new_article):
                articles.append(new_article)
    utils.create_json(file_target, articles, "Minutes/", "min")


if __name__ == '__main__':
    add_articles()
