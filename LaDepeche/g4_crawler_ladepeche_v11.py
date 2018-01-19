# -*- coding: utf-8 -*-
# Group 4 Robot - Lea Besnard, Laetitia Krumeich, Noémie Deloeuvre,
# Sofian Benjebria, Morgan Seguela
""" -*- coding: utf-8 -*-
 Groupe 4
 Lea Besnard, Laetitia Krumeich, Noémie Deloeuvre,Sofian Benjebria,
 Morgan Seguela,MOTHES Céline
 V1 : create code
 V1.1 : create function
"""

import datetime 
import re

import g4_utils_v40 as utils


def recovery_article_ld(url):
    """
        Arguments:
            url : string
        Return :
            article : dictionary
        It retrieve for each article the title, newspaper, author, date, theme
    """
    soup = utils.recovery_flux_url_rss(url)

    # Retrieve the title
    tag_meta = soup.find('meta', attrs={'property': 'og:title'})
    title = tag_meta.get('content')

    # Retrieve the publication date
    publi_date = ''
    tag_publi_date = soup.find('time',
                               attrs={'itemprop': 'datePublished'})
    regex_date = re. search('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',
                            tag_publi_date.string)
    publi_date = regex_date.group(0)

    # Retrieve the author
    author = []
    for div in soup.find_all('div', attrs={'class': 'article_author'}):
        author.append(div.span.get_text())

    # Retrieve the content
    content = ''
    for div in soup.find_all('div', attrs={'itemprop': 'articleBody'}):
            for p in div.find_all('p'):
                content += p.get_text() + ' '
    # Retrieve the theme
    theme = ""
    theme = soup.find('h2', attrs={'itemprop': 'about'}).get_text()

    # Retrieve all the informations off the article
    article = utils.recovery_article(title, 'LaDepeche', author, publi_date,
                                     content, theme)

    return(article)




def recovery_old_articles_LD(file_target = '/var/www/html/projet2018/data/clean/robot/' + str(datetime.datetime.now().date())):
    """
        it create a json for each article
    """
    list_category = ['grand-sud', 'actu', 'faits-divers',
                     'economie', 'sports', 'sante', 'tv-people', 'sorties']
    links_article = []
    list_articles = []
    for cat in list_category:
        for i in range(1, 100):
            try:
                url = 'https://www.ladepeche.fr/recherche/?p=' + str(i)\
                        + '&c=' + cat + '&plus-infos=1'
                soup = utils.recovery_flux_url_rss(url)
            except:
                break

        for h2 in soup.find_all('h2'):
            for item in h2.find_all('a'):
                link = 'https://www.ladepeche.fr' + str(item.get('href'))
                links_article.append(link)

        for link in links_article:
            new_article = recovery_article_ld(link)
            if not utils.is_empty(new_article):
                list_articles.append(new_article)
        utils.create_json(file_target, list_articles, "Ladepeche", "LD")


if __name__ == '__main__':
    recovery_old_articles_LD()
