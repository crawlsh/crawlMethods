# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class cttCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "ctt"
    DESCRIPTION = "爬取创头条"
    EXAMPLE_URL = "http://www.ctoutiao.com/1937934.html"
    USING = "Soup"
    EXTRACT_LATEST_RE = re.compile("target=\"_blank\" href=\"/(.+?)\.html\"")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'tag', 'title', 'summary',
                       'article'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def getLastestPostID():
        html = crawlUtils.crawlWorker("http://www.ctoutiao.com/", "Anon", 0)['raw']
        return int(cttCrawlMethod.EXTRACT_LATEST_RE.findall(html)[0])

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "http://www.ctoutiao.com/%s.html"
        latestID = cttCrawlMethod.getLastestPostID()
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
            rulesObj.append({'name': 'author', 'rule': ['p', {'class': 'A_pon1'}, 0]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['div', {'class': 'A_linebn'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'A_zys'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'A_contxt'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
