# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class pedailyCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "pedaily"
    DESCRIPTION = "爬取投资界网"
    EXAMPLE_URL = "https://m.pedaily.cn/news/444086"
    EXTRACT_LATEST_RE = re.compile("<a target=\"_self\" href=\"https://m\.pedaily\.cn/news/(.+?)\">")
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'time', 'title', 'summary', 'article', 'tag'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def getLastestPostID():
        html = crawlUtils.crawlWorker("https://m.pedaily.cn/", "Anon", 0)['raw']
        return int(pedailyCrawlMethod.EXTRACT_LATEST_RE.findall(html)[1])

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "https://m.pedaily.cn/news/%s"
        latestID = pedailyCrawlMethod.getLastestPostID()
        if userParamObj["crawlBy"] == "ORDER":
            result = [
                urlTemplate % i
                for i in range(latestID - int(userParamObj["info"]["amount"]), latestID)
            ]
            return result
        if userParamObj["crawlBy"] == "ID":
            result = [urlTemplate % i for i in range(
                latestID - int(userParamObj["info"]["idRangeEnd"]),
                latestID - int(userParamObj["info"]["idRangeStart"]))
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
            rulesObj.append({'name': 'author', 'rule': ['span', {'class': 'author'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'time', 'rule': ['span', {'class': 'date'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'subject'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'news-content'}, 0]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['div', {'class': 'tag'}, 0]})

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
