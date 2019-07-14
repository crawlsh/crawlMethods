# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class pedataCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "pedata"
    DESCRIPTION = "爬取清科研究中心"
    EXAMPLE_URL = "https://news.pedata.cn/531113.html"
    EXTRACT_LATEST_RE = re.compile("<a href=\"https://news\.pedata\.cn/(.+?)\.html\" target=\"_blank\">")
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'time', 'title', 'summary', 'article'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def getLastestPostID():
        html = crawlUtils.crawlWorker("https://news.pedata.cn/", "Anon", 0)['raw']
        return int(pedataCrawlMethod.EXTRACT_LATEST_RE.findall(html)[0])

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "https://news.pedata.cn/%s.html"
        latestID = pedataCrawlMethod.getLastestPostID()
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
            rulesObj.append({'name': 'author', 'rule': ['div', {'class': 'article_from'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['div', {'class': 'article_tl'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['div', {'class': 'article_title'}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'article_zy'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'article_main'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
