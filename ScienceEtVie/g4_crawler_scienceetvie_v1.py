# Group 4 Robot - Lea Besnard, Laetitia Krumeich, Noemie Deloeuvre,
# Céline Mothes

import g4_utils_v40 as utils
import datetime as date


def recovery_information_sv(url_article):
    """
        Arguments:
            - url of one article
        Returns:
            - informations of the article
    """
    soup_article = utils.recovery_flux_url_rss(url_article)

    title = ''
    title = soup_article.find('h1', attrs={'class': 'like-h1'}).get_text()

    # date
    date = soup_article.find("time")["datetime"]

    # author
    author = []
    for span in soup_article.find_all('span', attrs={'class': 'author'}):
        author.append(span.span.get_text())

    # content
    content = ''
    for div in soup_article.find_all('div',
                                     attrs={'class': ['content', 'left']}):
        for p in div.find_all('p'):
            content += p.get_text() + ' '

    # theme
    theme = ''
    tag_meta = soup_article.find('meta', attrs={'property': 'article:tag'})
    theme = tag_meta.get_text('content')

    article = utils.recovery_article(title, 'Scienceetvie',
                                     author, date, content, theme)
    return(article)


def recovery_old_articles_sv(file_target='/var/www/html/projet2018/data/clean/robot/" +
                             str(date.datetime.now().date()) + "/"):
    """
        Returns:
            - creation of a json for each new article
    """
    list_category = [
        'corps-et-sante',
        'nature-et-enviro',
        'ciel-et-espace',
        'technos-et-futur',
        'cerveau-et-intelligence',
        'science-et-culture']

    list_articles = []
    i = 0
    for cat in list_category:
        url_rss_sv = 'https://www.science-et-vie.com/' + cat

        soup_url = utils.recovery_flux_url_rss(url_rss_sv)

        article_sv = []
        # We retrieve all the articles for a given page
        for div in soup_url.find_all('div', attrs={'class': 'title'}):
                for item in div.find_all("a"):
                    links = 'https://www.science-et-vie.com/' + \
                        str(item.get('href'))
                    article_sv.append(links)

        # Each article is analized one by one
        for article in article_sv:
            new_article = recovery_information_sv(article)
            if not utils.is_empty(new_article):
                list_articles.append(recovery_information_sv(article))
            i += 1
            if i == 20:
                utils.create_json(file_target, list_articles, 'ScienceEtVie/',
                                  'sv')
                i = 0
                list_articles = []

    utils.create_json(file_target, list_articles, 'ScienceEtVie/',
                      'sv')


if __name__ == '__main__':
    recovery_old_articles_sv()
    # /var/www/html/projet2018/data/clean/robot/
