# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import json


class laohuCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "laohu"
    DESCRIPTION = "爬取老虎财经网"
    EXAMPLE_URL = "http://www.laohucaijing.com/Www_detail/index/133977/"
    USING_SOUP = int("1")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'title', 'article', 'view_count', 'tag'],  # Implement here!
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
    def generateLinks(userParamObj):
        urlTemplate = "http://www.laohucaijing.com/Www_detail/index/%s/"
        if userParamObj["crawlBy"] == "ORDER":
            result = [
                urlTemplate % i
                for i in range(133977 - int(userParamObj["info"]["amount"]), 133977)
            ]
            return result
        if userParamObj["crawlBy"] == "ID":
            result = [urlTemplate % i for i in range(
                int(userParamObj["info"]["idRangeStart"]),
                int(userParamObj["info"]["idRangeEnd"]))
                      ]
            return result

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
            rulesObj.append({'name': 'author', 'rule': ['div', {'class': 'artInfo1'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'text'}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'artDeta'}, 0]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['p', {'class': 'Label'}, 0]})

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
