# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class chinatimesCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "pedata"
    DESCRIPTION = "爬取华夏时报网"
    EXAMPLE_URL = "http://www.chinatimes.net.cn/article/87450.html"
    USING = "Soup"
    EXTRACT_LATEST_RE = re.compile("<a href=\"http://www\.chinatimes\.net\.cn/article/(.+?)\.html\" target=\"_blank\">")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'time', 'title', 'summary', 'article', 'thumb_count'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def getLastestPostID():
        html = crawlUtils.crawlWorker("http://www.chinatimes.net.cn/", "Anon", 0)['raw']
        return int(chinatimesCrawlMethod.EXTRACT_LATEST_RE.findall(html)[0])

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "http://www.chinatimes.net.cn/article/%s.html"
        latestID = chinatimesCrawlMethod.getLastestPostID()
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
            rulesObj.append({'name': 'author', 'rule': ['p', {'id': 'author_baidu'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['p', {'id': 'pubtime_baidu'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'abstract'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'infoMain'}, 0]})

        if 'thumb_count' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'thumb_count', 'rule': ['b', {'id': 'praise_count'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
