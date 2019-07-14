# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class ctsbwCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "ctsbw"
    DESCRIPTION = "爬取创投时报网"
    EXAMPLE_URL = "http://www.ctsbw.com/article/14415.html"
    USING = "Soup"
    EXTRACT_LATEST_RE = re.compile("<a target=\"_blank\"  href=\"http://www\.ctsbw\.com/article/(.+?).html")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'title', 'summary', 'article', 'tag'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def getLastestPostID():
        html = crawlUtils.crawlWorker("http://www.ctsbw.com/article/", "Anon", 0)['raw']
        return int(ctsbwCrawlMethod.EXTRACT_LATEST_RE.findall(html)[5])

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "http://www.ctsbw.com/article/%s.html"
        latestID = ctsbwCrawlMethod.getLastestPostID()
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

    @staticmethod
    def replaceSoup(soup):
        return soup
