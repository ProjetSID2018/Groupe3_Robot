# -*- coding: utf-8 -*-
"""
 Group 4
 Realized by BENJEBRIA Sofian, DELOEUVRE Noémie, MOTHES Céline Mothes,
             SEGUELA Morgan
 V1 : create code
 V1.1 : create function
 V1.2 : code optimization
"""
import datetime as date
import unidecode
import re
import g4_utils_v40 as utils


def recovery_information_lg(url):
    """
        Arguments:
            url : string
        Return :
            article : dictionary
        It retrieve for each article the title, newspaper, author, date, theme
    """
    soup = utils.recovery_flux_url_rss(url)

    # Retrieving the title
    title = ''
    balise_title = soup.title.string
    sep = balise_title.split('—')
    title = unidecode.unidecode('—'.join(sep[:-1]))

    tag_context = soup.find('span', attrs={'class': 'context'})

    # Retrieving of author
    author = []
    author.append(tag_context.a.get_text())

    # Retrieving of publication date
    date_p = ''
    regex_date = re. search('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',
                            tag_context.get_text())
    date_p = regex_date.group(0)
    date_p = str(date.datetime.strptime(date_p, '%d/%m/%Y').date())

    # Retrieving the theme
    tag_post_cat = soup.find('ul', attrs={'class': 'post-categories'})
    for li in tag_post_cat.find_all('li'):
        theme = li.get_text()

    # Retrieving the content of the article
    contents = ''
    tag_content = soup.find('div', attrs={'class': 'content'})
    if tag_content:
        for p in tag_content.find_all('p'):
            contents += p.get_text() + " "

    new_article = utils.recovery_article(title, 'LeGorafi', author, date_p,
                                         contents, theme)
    return(new_article)


def recovery_link_new_articles_lg(url_rss):
    """
        Argument:
            url_rss : string
        Return:
            link_article = list
        Retrieving links of new articles thanks to the rss feed
    """
    soup = utils.recovery_flux_url_rss(url_rss)
    items = soup.find_all('item')
    links_article_gorafi = []
    for item in items:
        links_article_gorafi.append(re.search(r"<link/>(.*)", str(item))[1])
    return(links_article_gorafi)


def recovery_new_article_lg():
    """
         Retrieving new articles thanks to the rss feed
         and create for each article a json
    """
    file_target = "/var/www/html/projet2018/data/clean/robot/"
    url_rss = "http://www.legorafi.fr/feed/"
    links_article = recovery_link_new_articles_lg(url_rss)
    list_article = []
    for link_article in links_article:
        new_article = recovery_information_lg(link_article)
        if not utils.is_empty(new_article):
            print(new_article)
            list_article.append(new_article)
    utils.create_json(file_target, list_article, 'LeGorafi', 'lg')


if __name__ == '__main__':
    recovery_new_article_lg()
