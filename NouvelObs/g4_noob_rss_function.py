# Group 4
# DELOEUVRE Noémie

import g4_utils_v40 as utils
import re
from datetime import datetime
import datetime as date


def recovery_information_noob(url_article):
    """
        Arguments:
            - url of one article
        Returns:
            - informations of the article
    """
    soup_article = utils.recovery_flux_url_rss(url_article)

    title = soup_article.title.get_text()

    # Retrieval of publication date
    find_date = soup_article.find('time', attrs={"class": "date"})
    for a in find_date.find_all('a'):
        find_valeur = re.compile('[0-9]{4}\/[0-9]{2}\/[0-9]{2}')
        for valeur in find_valeur.finditer(str(a.get("href"))):
            date_p = valeur.group(0)
            date_p = datetime.strptime(date_p, "%Y/%m/%d")\
                .strftime("%Y-%m-%d")

    # Retrieval of the author of the article
    author = []
    for div in soup_article.find_all('div'):
        if re.search('author', str(div.get("class"))):
            author.append(div.p.span.get_text())

    # Retrieval of the artical theme
    theme = ""
    for nav in soup_article.find_all('nav'):
        if nav.get("class") == ['breadcrumb']:
            for ol in nav.find_all('ol'):
                for a in ol.find_all('a'):
                    theme = a.get_text()

    # Retrieving the content of the article
    contents = ""
    for div in soup_article.find_all('div'):
        if re.search('body', str(div.get("id"))):
            for aside in div.find_all('aside'):
                for p in aside.find_all('p'):
                    p.string = ""
            for p in div.find_all('p'):
                for a in p.find_all('a'):
                    if a.get("class") == ['lire']:
                        a.string = ""
                for img in p.find_all('img'):
                    p.string = ""
                contents += p.get_text() + " "

    article = utils.recovery_article(title, 'NouvelObservateur',
                                     author, date_p, contents, theme)
    return(article)


def recovery_link_new_articles_noob_rss(url_rss):
    """
        Arguments:
            - url of the page containing feed links for
            the different categories
        Returns :
            - list of urls of the different categories

    """
    soup = utils.recovery_flux_url_rss(url_rss)

    liste_url = []
    # Retrieving all urls of new RSS feeds of different categories
    for a in soup.find_all('a'):
        if a.get("class") == ['sprite-rss', 'sp-rss']:
            if re.search('www', str(a.get("href"))):
                liste_url.append(a.get("href"))

    return(liste_url)


def recovery_new_articles_noob_rss(file_target="data/clean/robot/" +
                                   str(date.datetime.now().date()) + "/"):
    """
        Returns:
            - creation of a json for each new article
    """
    file_json = []
    i = 0
    # Each url is analized one by one
    list_url = recovery_link_new_articles_noob_rss("http://www.nouvelobs." +
                                                   "com/rss/")
    for url in list_url:
        soup_url = utils.recovery_flux_url_rss(url)
        items = soup_url.find_all("item")
        article_noob = []

        # We're picking up every new article in a list
        for item in items:
            link_article = re.search(r"<link/>(.*)", str(item))[1]
            link_article = link_article.split("<description>")
            link_article = link_article[0]
            article_noob.append(link_article)
            if re.search("\/galeries\-photos\/", link_article):
                article_noob.remove(link_article)
        # Each article is analized one by one
        for article in article_noob:
            new_article = recovery_information_noob(article)
            if utils.is_empty(new_article) is False:
                file_json.append(new_article)
            i += 1
        if i == 20:
            utils.create_json(file_target, file_json, "NouvelObs_rss/",
                              "noob")
            i = 0
            file_json = []

    utils.create_json(file_target, file_json, "NouvelObs/",
                      "noob")


if __name__ == '__main__':
    recovery_new_articles_noob_rss()
