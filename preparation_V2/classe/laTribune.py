from journal import Journal
from article import Article
from re import compile

class LaTribune(Journal):
    
    def __init__(self, name_journal, _abbreviation, _base_url=""):
        Journal.__init__(self, name_journal, _abbreviation, _base_url)

    def find_article(self,url):
        pass
    
    def find_links(self,new):
        pass

    def find_articles(self,url):
        pass
    
