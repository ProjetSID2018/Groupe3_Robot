# Group 4
# DELOEUVRE Noémie

import g4_utils_v32 as utils
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
        for valeur in re.finditer('author', str(div.get("class"))):
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
        for valeur in re.finditer('body', str(div.get("id"))):
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

"""
def recovery_link_new_articles_noob(url_rss):
        Arguments:
            - url of the page containing feed links for
            the different categories
        Returns :
            - list of urls of the different categories

    soup = utils.recovery_flux_url_rss(url_rss)
    
    liste_url = []
    # Retrieving all urls of new RSS feeds of different categories                
    for a in soup.find_all('a'):
        if a.get("class") == ['sprite-rss', 'sp-rss']:
            for valeur in re.finditer('www', str(a.get("href"))):
                liste_url.append(a.get("href"))

    return(liste_url)
"""


def recovery_new_articles_noob(file_target="data/clean/robot/" +
                               str(date.datetime.now().date()) + "/"):
    """
        Returns:
            - creation of a json for each new article
    """

    list_category = ["politique", "monde", "economie", "culture",
                     "editos-et-chroniques", "debat"]

    file_json = []
    for cat in list_category:
        # We retrieve the URL feeds for each page of article
        # Each HTML-coded article is analyzed with beautiful soup
        for i in range(2, 8):
            url_rss_noob = "http://www.nouvelobs.com/" + cat +\
                "/page-" + str(i) + ".html"

            soup_url = utils.recovery_flux_url_rss(url_rss_noob)

            article_noob = []
            # We retrieve all the articles for a given page
            for h3 in soup_url.find_all('h3'):
                if h3.get("class") == ['title']:
                    for valeur in re.finditer('^\/', str(h3.a.get("href"))):
                        new_article = "http://www.nouvelobs.com" +\
                            h3.a.get("href")
                        article_noob.append(new_article)

            # Each article is analized one by one
            for article in article_noob:
                file_json.append(recovery_information_noob(article))

    utils.create_json(file_target, file_json, "NouvelObs_crawler/",
                      "noob")


if __name__ == '__main__':
    recovery_new_articles_noob()
