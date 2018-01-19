from journal import Journal
from article import Article
from re import compile

class Telerama(Journal):
    
    def __init__(self, name_journal, _abbreviation, _base_url=""):
        Journal.__init__(self, name_journal, _abbreviation, _base_url)

    def find_article(self,url):
        soup=self.recovery_flux_url(url)
        article_soup=soup.find("article")
        meta=soup.find("meta",property="og:title").get("content")
        tab=meta.split("-")
        n=len(tab)
        newspaper=tab[n-1] 
        theme=tab[n-2]
        title="-".join(tab[:n-2])
        authors=[]
        regex = compile(r'[\n\r\t]')
        for span in article_soup.find_all("span",class_="author--name"):
            author = regex.sub("", span.get_text())
            authors.append(author.strip())
        date_pub=article_soup.find("span",itemprop="datePublished").get("datetime")[:10].replace("-","/")
        content=""
        for div in article_soup.find_all("div",class_=["article--intro","article--wysiwyg","article--footnotes"]) :
            for p in div.find_all("p"):
                content=content+p.get_text()
        content = regex.sub("", content)
        return Article(title,newspaper,authors,date_pub,content,theme)
    
    def find_links(self,new):
        """
            it create a json for each new article
        """
        urls=[]
        categories={
            "cinema" : 20,
            "scenes" : 20,
            "enfants" : 3,
            "idees" : 20,
        }
        for category,nbre in categories.items() :
            for i in range(0,nbre) :
                url=self.base_url+"/"+category+"/articles?page="+str(i)
                urls.append(url)
        return urls

    def find_articles(self,url):
        """
            Prend en parametre une catégorie et retour toutes les articles de cette catégorie
        """
        result=[]
        soup=self.recovery_flux_url(url)
        articles=soup.find_all("div",class_="item--body")
        for article in articles:
            url_article=article.find("a").get("href")
            if self.is_article(url_article):
                result.append(self.find_article(url_article))
        return result
    
    def is_article(self,url):
        """
            Prend en argument une adresse url et retourne vrai s'il est une article et faux sinon
        """
        soup=self.recovery_flux_url(url)
        return soup.find("div",class_="article--text")!=None
