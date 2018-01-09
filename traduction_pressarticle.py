import chardet
import json
import os
import datetime as date

path = "pressarticles/"
path_target = "target_press_article/"
newspapers = os.listdir(path)

cur_date = date.datetime.now().date()

os.makedirs(path_target, exist_ok=True)

dict_init = {"futurasciences" : "fusc",
             "lefigaro" : "lfi",
             "lemonde" : "lmde",
             "liberation" : "libe",
             "nouvelobs" : "noob",
             "telerama" : "tera"}
 
for newspaper in newspapers:

    newspaper_path = path + newspaper + "/"
    newspaper_path_target = path_target +  newspaper + "/"
    articles = os.listdir(newspaper_path)

    os.makedirs(newspaper_path_target, exist_ok=True)        

    i = 0
    for article in articles:
        i += 1
        article_path = newspaper_path + article
        article_name = 'art'+ dict_init[newspaper] + str(i) + str(cur_date) + "_robot.json"
        article_path_target = newspaper_path_target + article_name
        with open(article_path, "rb") as f:
            charcode = chardet.detect(f.read())["encoding"]
        with open(article_path, "r", encoding=charcode) as f:
            data = json.load(f)

        data["body"] = data["body"].replace(u'\xa0', u' ')
        
        newformat = {}
        newformat["title"] = data["title"]
        newformat["newspaper"] = data["newspaper"]
        try:
            newformat["author"] = data["author"]
        except:
            newformat["author"] = "La rédaction"
        newformat["date_publi"] = data["date"]
        newformat["content"] = data["body"]
        newformat["theme"] = data["theme"]
        with open(article_path_target, "w", encoding="utf-8") as fw:
            json.dump(newformat, fw, ensure_ascii=False)






