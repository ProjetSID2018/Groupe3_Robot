from telerama import Telerama as Tera
from minutes import Minutes as Minu
from journal_exception import JournalException
from journal_manager import JournalManager as JM
import datetime as date
from article import Article

try:
    #minu=Minu("20 minutes","minu","http://www.20minutes.fr")
    tera=Tera("Telerama","tera","http://www.telerama.fr")
    #tera.add_article("se")
    # ok print(len(tera.get_list_article()))
    jm=JM(tera,"/home/etudiant/Documents/ProjetSID/objet/Art/" + str(date.datetime.now().date()) +"/","telerama")
    #jm=JM(minu,"/home/etudiant/Documents/ProjetSID/objet/Art/" + str(date.datetime.now().date()) +"/","minutes")
    # okart=Article("title","test",["Mr"],"12-1-2017","irem","cin")
    # ok print(art.id_art)
    # ok print(jm.already_exists(art))
    jm.create_json(new=False)

except JournalException as je:
    print(je)