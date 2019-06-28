# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class ctsbwCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "ctsbw"
    DESCRIPTION = "爬取创投时报网"
    EXAMPLE_URL = "http://www.ctsbw.com/article/14415.html"
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'title', 'summary', 'article', 'tag'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
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
    def generateLinks(userParamObj):
        urlTemplate = "http://www.ctsbw.com/article/%s.html"
        if userParamObj["crawlBy"] == "ORDER":
            result = [
                urlTemplate % i
                for i in range(14476 - int(userParamObj["info"]["amount"]), 14476)
            ]
            return result
        if userParamObj["crawlBy"] == "ID":
            result = [urlTemplate % i for i in range(
                14476 - int(userParamObj["info"]["idRangeEnd"]),
                14476 - int(userParamObj["info"]["idRangeStart"]))
                      ]
            return result
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
            rulesObj.append({'name': 'author', 'rule': ['p', {'class': 's14'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h2', {'class': 's28'}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'cj_laiyuan'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'col-xs-12'}, 1]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['b', {'class': 'col-xs-5'}, 0]})

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
