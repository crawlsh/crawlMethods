# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class cyzoneCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "cyzone"
    DESCRIPTION = "爬取创业邦"
    EXAMPLE_URL = "http://www.cyzone.cn/article/532494.html"
    USING = "Soup"
    EXTRACT_LATEST_RE = re.compile("//www\.cyzone\.cn/article/(.+?)\.html\" class=\"item-title\"")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'tag', 'title',
                       'article', 'time', 'thumb_count', 'comments'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def getLastestPostID():
        html = crawlUtils.crawlWorker("http://www.cyzone.cn/content/index/init?tpl=index_page&page=1", "Anon", 0)['raw']
        return int(cyzoneCrawlMethod.EXTRACT_LATEST_RE.findall(html)[0])

    @staticmethod
    def generateLinks(userParamObj):
        latestID = cyzoneCrawlMethod.getLastestPostID()
        urlTemplate = "http://www.cyzone.cn/article/%s.html"
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
            rulesObj.append({'name': 'author', 'rule': ['span', {'class': 'form'}, 0]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['div', {'class': 'article-tags'}, 0]})

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

    @staticmethod
    def replaceSoup(soup):
        return soup
