# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class jpmCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "jpm"
    DESCRIPTION = "爬取金评媒"
    EXAMPLE_URL = "http://www.jpm.cn/article-76489-1.html"
    EXTRACT_LATEST_RE = re.compile("<a href=\"/article-(.+?)-1\.html\" target=\"_blank\">")
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['title', 'summary',
                       'article', 'comments'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def getLastestPostID():
        html = crawlUtils.crawlWorker("http://www.jpm.cn/", "Anon", 0)['raw']
        return int(jpmCrawlMethod.EXTRACT_LATEST_RE.findall(html)[7])

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "http://www.jpm.cn/article-%s-1.html"
        latestID = jpmCrawlMethod.getLastestPostID()
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

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'writer'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'story_box'}, 0]})

        if 'comments' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'comments', 'rule': ['div', {'class': 'review_read_box'}, 0]})
        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
