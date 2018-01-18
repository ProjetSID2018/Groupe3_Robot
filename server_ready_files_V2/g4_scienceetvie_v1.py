# Group 4 Robot - Lea Besnard, Laetitia Krumeich, Noemie Deloeuvre

import g4_utils_v40 as utils
from datetime import datetime
import datetime as date


def recovery_information_sv(url_article):
    """
        Arguments:
            - url of one article
        Returns:
            - informations of the article
    """
    soup_article = utils.recovery_flux_url_rss(url_article)

    # title
    title = ""
    for h1 in soup_article.find_all("h1"):
        if h1.get("class") == ["like-h1"]:
            title = h1.get_text()

    # date
    t_date = soup_article.find("time")["datetime"]

    # author
    author = []
    for span in soup_article.find_all('span'):
        if span.get("class") == ["author"]:
            author.append(span.span.get_text())

    # content
    content = ""
    for div in soup_article.find_all('div'):
        if div.get("class") == ['content', 'left']:
            for p in div.find_all('p'):
                content += p.get_text() + " "

    # theme
    theme = ""
    for meta in soup_article.find_all('meta'):
        if meta.get("property") == 'article:tag':
            theme = meta.get("content")

    article = utils.recovery_article(title, 'Scienceetvie',
                                     author, date, content, theme)
    return(article)


def recovery_old_articles_sv(
    file_target="C:/Users/Laetitia/Desktop/Groupe4_Robot" + str(
        date.datetime.now().date()) + "/"):
    """
        Returns:
            - creation of a json for each new article
    """

    list_category = [
        "corps-et-sante",
        "nature-et-enviro",
        "ciel-et-espace",
        "technos-et-futur",
        "cerveau-et-intelligence",
        "science-et-culture"]

    file_json = []
    i = 0
    for cat in list_category:
        # We retrieve the URL feeds for each page of article
        # Each HTML-coded article is analyzed with beautiful soup
        url_rss_sv = "https://www.science-et-vie.com/" + cat

        soup_url = utils.recovery_flux_url_rss(url_rss_sv)

        article_sv = []
        # We retrieve all the articles for a given page
        for div in soup_url.find_all("div"):
            if div.get("class") == ["title"]:
                for item in div.find_all("a"):
                    links = "https://www.science-et-vie.com/" + \
                        str(item.get("href"))
                    article_sv.append(links)

        # Each article is analized one by one
        for article in article_sv:
            new_article = recovery_information_sv(article)
            if utils.is_empty(new_article) is False:
                file_json.append(recovery_information_sv(article))
            i += 1
        if i == 20:
            utils.create_json(file_target, file_json, "ScienceEtVie_crawler/",
                              "sv")
            i = 0
            file_json = []

    utils.create_json(file_target, file_json, "ScienceEtVie_crawler/",
                      "sv")


if __name__ == '__main__':
    recovery_old_articles_sv()
