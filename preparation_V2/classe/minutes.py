from journal import Journal
from article import Article
from re import compile,search

class Minutes(Journal):
    
    def __init__(self, name_journal, _abbreviation, _base_url=""):
        Journal.__init__(self, name_journal, _abbreviation, _base_url)

    def find_article(self,url):
        soup=self.recovery_flux_url(url)
        article=soup.find("article")
        title=article.find("h1").get_text()
        authors = [] if article.find("header")\
            .find("p", class_="authorsign-label")\
            == None else article.find("header")\
            .find("p", class_="authorsign-label").get_text().split(" et ")
        date_tab=article.find("time").get("datetime")[:10].split("-")
        date_tab.reverse()
        date_pub="/".join(date_tab)
        theme = article.find("ol", class_="breadcrumb-list")\
            .find_all("li")[1].find("span").get_text()
        content=""
        for p in article.find("div",class_="content").find_all("p"):
            content=content+p.get_text()
        newspaper=soup.find("footer").find(self.has_copyright).find("a").get_text()
        regex = compile(r'[\n\r\t]')
        content = regex.sub("", content)
        return Article(title,newspaper,authors,date_pub,content,theme)
    
    def find_links(self,new):
        urls=[]
        if new :
            soup = self.recovery_flux_url("http://www.20minutes.fr/rss/actu-france.xml")
            items = soup.find_all("item")
            for item in items:
                url=search(r"<link/>(.*)<pubdate>", str(item))[1]
                urls.append(url)
        else:
            categories= {
                "sport" : ["footbal","basketball","mercato","rugby","tennis","cyclisme","vendee_globe"],
                "economie" : ["emploi","immobilier","auto","assurance"],
                "high-tech" : ["apple","apple","facebook","jeux_video"],
                "planete" : ["animaux","environnement","climat","ocean","plantes"],
                "cinema" : "cinema","people" : "people","television" : "television","culture" : "culture",
                "web" : "web","livres" : "livres","mode" : "mode","serie" : "serie","sortir" : "sortir",
                "sciences" : "sciences", "bordeaux" : "bordeaux", "strasbourg" : "strasbourg", "toulouse" : "toulouse",
                "lille" : "lille","lyon" : "lyon","marseille" : "marseille", "montpellier" : "montpellier", "paris" : "paris",
                "nice" : "nice", "nantes" : "nantes", "rennes" : "rennes"
            }
            for k,v in categories.items():
                url=self.base_url+"/"+k+"/"
                if isinstance(v,list):
                    for s_category in v:
                        urls.append(url+s_category)
                else:
                    urls.append(url)
        return urls

    def find_articles(self,url):
        """
            Prend en parametre une catégorie et retour toutes les articles de cette catégorie
        """
        result=[]
        soup=self.recovery_flux_url(url)
        articles=soup.find_all('article')
        for article in articles:
            url_article=self.base_url+article.find("a").get("href")
            if(self.is_article(url_article)):
                result.append(self.find_article(url_article))
        return result
    
    def is_article(self,url):
        """
            Prend en argument une adresse url et retourne vrai s'il est une article et faux sinon
        """
        soup=self.recovery_flux_url(url)
        article=soup.find("article")
        return article != None

    def has_copyright(self,tag):
        """
            Verifier si le contenu de la balise contient le mot cle "copyright"
        """
        return "Copyright" in tag.get_text()


