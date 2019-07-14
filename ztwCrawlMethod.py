# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class ztwCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "ztw"
    DESCRIPTION = "爬取知投网"
    EXAMPLE_URL = "https://www.tmtpost.com/4011711.html"
    USING = "Soup"
    EXTRACT_LATEST_RE = re.compile("<a href=\"http:\/\/www\.zhito"
                                   "uwang\.cn\/news\/detail\/(.+?)\.html\" target=\"_blank\"")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'title', 'article'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def getLastestPostID():
        html = crawlUtils.crawlWorker("http://www.chinatimes.net.cn/", "Anon", 0)['raw']
        return int(ztwCrawlMethod.EXTRACT_LATEST_RE.findall(html)[5])

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "http://www.zhitouwang.cn/news/detail/%s.html"
        latestID = ztwCrawlMethod.getLastestPostID()
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

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['div', {'class': 'author-warp'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h3', {'class': 'detail-title'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'news-detail-text'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
