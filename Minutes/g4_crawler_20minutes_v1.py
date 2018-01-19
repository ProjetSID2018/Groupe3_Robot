#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unidecode import unidecode
import datetime as date

import g4_utils_v40 as utils


# Verifier si le tag contient le texte Copyright
def has_copyright(tag):
    """
        Verifier si le contenu de la balise contient le mot cle "copyright"
    """
    return "Copyright" in tag.get_text()


# Prend en parametre une catégorie et retour toutes les articles de cette catégorie
def get_article_of_category(url):
    result = []
    soup = utils.recovery_flux_url_rss(url)
    articles = soup.find_all('article')
    for article in articles:
        url_article = "http://www.20minutes.fr"+article.find("a").get("href")
        # Insérer le nouveau article dans un le tableau
        if(is_article(url_article)):
            result.append(get_article(url_article))
    return result


# Prend en argument une adresse url (url) et retourne un
# article en format dictionnaire
def get_article(url):
    soup = utils.recovery_flux_url_rss(url)
    article = soup.find("article")
    # Titre de l'article
    title = article.find("h1").get_text()
    # tableau vide quand il y'a pas d'autheur sinon tableau de(s) auteur(s)
    if article.find("header").find("p", class_="authorsign-label") is None:
        authors = []
    else:
        authors = article.find("header").find("p",
                              class_="authorsign-label").get_text().split(" et ")
        
    # Date de publication de l'article
    date_pub = article.find("time").get("datetime")[0:10]

    # Theme de l'article
    theme = article.find("ol", class_="breadcrumb-list").find_all("li")[1]\
        .find("span").get_text()
    # Contenu de l'article
    content = ""
    for p in article.find("div", class_="content").find_all("p"):
        content = content+p.get_text()
    # Nom du journal
    newspaper = soup.find("footer").find(has_copyright).find("a").get_text()

    return utils.recovery_article(title, newspaper, authors, date_pub, content,
                                  theme)


# Prend en argument une adresse url et retourne vrai s'il
# est un article et faux sinon
def is_article(url):
    soup = utils.recovery_flux_url_rss(url)
    article = soup.find("article")
    return article is not None


def recovery_old_article_minutes(
        file_target="/var/www/html/projet2018/data/clean/robot/" +
        str(date.datetime.now().date()) + "/"):
    # Chemin repertoire des articles

    source = "Minutes/"

    soup = utils.recovery_flux_url_rss("http://www.20minutes.fr")

    categories = soup.find("nav", class_="header-nav").find_all("li")
    articles = []

    for category in categories:
        url = category.find("a").get("href")
        theme = unidecode(category['data-theme'])
        if theme in ["default", "entertainment", "sport", "economy",
                     "hightech", "planet"]:
            articles.extend(get_article_of_category(url))

        utils.create_json(file_target, articles, source, "min")


if __name__ == '__main__':
    recovery_old_article_minutes()
