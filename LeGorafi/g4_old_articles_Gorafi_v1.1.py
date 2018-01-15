# -*- coding: utf-8 -*-
"""
 Group 4
 Realized by BENJEBRIA Sofian, DELOEUVRE Noémie, Céline Mothes
 V1 : create code
 V1.1 : create function
"""

import unidecode
import re
import g4_utils_v32 as utils

# Path to modify : target where we will store the json files
file_target = "C:/"


def recovery_information_lg(url):
    """
        Arguments:
            url : string
        Return :
            article : dictionary
        It retrieve for each article the title, newspaper, author, date, theme
    """
    soup = utils.recovery_flux_url_rss(url)
    balise_title = soup.title.get_text()
    sep = balise_title.split("—")
    title = unidecode.unidecode("—".join(sep[:-1]))
    newspaper = unidecode.unidecode("Le Gorafi")
    author = []

    # Retrieving of author and publication date
    for span in soup.find_all('span'):
        if span.get("class") == ['context']:
            author.append(span.a.get_text())
            for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',
                                      str(span)):
                date_p = valeur.group(0)

    # Retrieving the theme
    for ul in soup.find_all('ul'):
        if ul.get("class") == ['post-categories']:
            for li in ul.find_all('li'):
                theme = li.get_text()

    # Retrieving the content of the article
    contents = ""
    for div in soup.find_all('div'):
        if div.get("class") == ['content']:
            for p in div.find_all('p'):
                contents += p.get_text() + " "
            contents = unidecode.unidecode(contents)
            new_article = utils.recovery_article(title, newspaper, author,
                                                 date_p, theme, contents)
    return (new_article)


def recovery_link_old_articles_lg(url_rss):
    """
        Argument:
            url_rss : string
        Return:
            link_article = list
        Retrieving links of new articles thanks to the rss feed
    """
    list_category = ["france/politique", "france/societe", "monde-libre",
                     "france/economie", "culture", "people", "sports",
                     "hi-tech", "sciences", "ledito"]
    # We retrieve the URL feeds for each page of category
    for cat in list_category:
        for i in range(2, 3):
            url_rss = url_rss + cat + "/page/" + str(i) + "/feed/"
            soup = utils.recovery_flux_url_rss(url_rss)
            items = soup.find_all("item")
            link_article = []
            # We retrieve all the link of articles for a given page
            for item in items:
                link_article.append(re.search(r"<link/>(.*)", str(item))[1])
    return(link_article)


def recovery_old_article_lg():
    list_article = []
    url_rss = "http://www.legorafi.fr/category/"
    links_article = recovery_link_old_articles_lg(url_rss)
    for link in links_article:
        new_article = recovery_information_lg(link)
        list_article.append(new_article)
    utils.create_json(file_target, list_article, "LeGorafi_articles/", "lg")


if __name__ == '__main__':
    recovery_old_article_lg()
