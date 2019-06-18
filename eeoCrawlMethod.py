# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import json


class eeoCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "eeo"
    DESCRIPTION = "爬取经济观察网"
    EXAMPLE_URL = "http://www.eeo.com.cn/2019/0617/358786.shtml"
    USING_SOUP = int("1")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'title', 'article'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": True,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    """
    This function should generate all links user want to crawl
    
    For example, if user want to crawl 20 articles randomly, 
    this function should generate links of these articles
    
    If you need to crawl any page, use utils.crawlUtils.crawlWorker(url), 
    for more info, see https://docs.crawl.sh/
    
    return in an array please 😊
    """

    @staticmethod
    def requestAPIForURL(amount):
        amount = float(amount)
        i = amount / 10
        j = amount // 10
        needPages = int(i) if i == j else int(i) + 1
        result = []
        for i in range(1, 1 + needPages):
            try:
                APIURL = "http://app.eeo.com.cn/?app=wxmember&controller=index&action=getMoreArticle&catid=3572" \
                         "&allcid=358818,358815,358809,358808,358799,358795,358777,358775,358767,358763,358761,358740," \
                         "358732,358730,358718,358712&page=%s" % i
                html = crawlUtils.crawlWorker(APIURL, "Anon", 0)['raw'] \
                    .replace("<html><body><p>", "") \
                    .replace("</p></body></html>", "")\
                    .replace("(", "")\
                    .replace(");", "")
                jsonData = json.loads(html)
                links = [x["url"] for x in jsonData["article"]]
                result += links
            except:
                pass
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return eeoCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        return

    """
    This function should generate rules

    For example, if user want to crawl title of the articles, 
    this function should generate regex/soup rules of title

    return in an array please 😊
    """

    @staticmethod
    def generateSoupRules(userParamObj):
        rulesObj = []

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['div', {'class': 'xd_zuozheinfo'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'xd-nr'}, 0]})

        return rulesObj

    """
    [Optional]
    You can ignore this if everything works fine with foregoing functions
    
    This function can modify the html before it is analyzed by rules.
    
    For example, if you want to match the title of article but you replaced the title with empty string,
    the result would also be empty.
    """

    @staticmethod
    def replaceSoup(soup):
        return soup
