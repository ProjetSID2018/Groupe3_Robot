# -*- coding: utf-8 -*-
"""
 Group 4
 Realized by BENJEBRIA Sofian, DELOEUVRE Noémie, Céline Mothes
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
    for ul in soup.find_all('ul', attrs={'class': 'post-categories'}):
        for li in ul.find_all('li'):
                theme = li.get_text()

    # Retrieving the content of the article
    contents = ''
    for div in soup.find_all('div', attrs={'class': 'content'}):
        for p in div.find_all('p'):
            contents += p.get_text() + ' '

    new_article = utils.recovery_article(title, 'LeGorafi', author,
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
    list_category = ['france/politique', 'france/societe', 'monde-libre',
                     'france/economie', 'culture', 'people', 'sports',
                     'hi-tech', 'sciences', 'ledito']
    # We retrieve the URL feeds for each page of category
    link_article = []
    for cat in list_category:
        for i in range(2, 8):
            url_rss = url_rss + cat + '/page/' + str(i) + '/feed/'
            soup = utils.recovery_flux_url_rss(url_rss)
            items = soup.find_all('item')
            # We retrieve all the link of articles for a given page
            for item in items:
                link_article.append(re.search(r"<link/>(.*)", str(item))[1])
    return(link_article)


def recovery_old_article_lg(file_target="/var/www/html/projet2018/data/clean/robot/" +
                            str(date.datetime.now().date()) + "/"):
    """
        it create a json for each new article
    """
    list_article = []
    ii = 0
    url_rss = 'http://www.legorafi.fr/category/'
    links_article = recovery_link_old_articles_lg(url_rss)
    for link in links_article:
        new_article = recovery_information_lg(link)
        if not utils.is_empty(new_article):
            list_article.append(new_article)
            ii += 1
        if ii == 20:
            utils.create_json(file_target, list_article, 'LeGorafi', 'lg')
            ii = 0
            list_article = []
    utils.create_json(file_target, list_article, 'LeGorafi', 'lg')


if __name__ == '__main__':
    recovery_old_article_lg()
    # /var/www/html/projet2018/data/clean/robot/
