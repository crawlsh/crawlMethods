# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import json


class chinaipoCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "chinaipo"
    DESCRIPTION = "爬取China IPO"
    EXAMPLE_URL = "http://m.chinaipo.com/vc/83640.html"
    USING = "Soup"
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
                APIURL = "http://api.chinaipo.com/zh-hans/api/articles/?page=%s" % i
                jsonData = crawlUtils.requestJsonWithProxy(APIURL)
                for j in jsonData["results"]:
                    originalId = j["originalId"]
                    result.append("http://api.chinaipo.com/zh-hans/api/article/?originalId=%s" % originalId)
            except:
                pass
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return chinaipoCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        return

    """
    This function should generate rules

    For example, if user want to crawl title of the articles, 
    this function should generate regex/soup rules of title

    return in an array please 😊
    """

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': "source"})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': "tags"})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {'class': 'article-tit'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'article-content'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'time', 'rule': ['span', {'class': 'date-time'}, 1]})

        if 'thumb_count' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'thumb_count', 'rule': ['div', {'class': 'article-end-collect'}, 0]})

        if 'comment_count' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'comment_count', 'rule': ['div', {'class': 'comment'}, 0]})

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
