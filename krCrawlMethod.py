# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class krCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "36Kr"
    DESCRIPTION = "Crawl content of 36kr"
    EXAMPLE_URL = "https://36kr.com/p/5205828"
    EXTRACT_LATEST_RE = re.compile("url\":\"https://36kr\.com/p/(.+?)\"")
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'author_description', 'author_article_count', 'summary',
                       'article', 'time', 'thumb_count', 'comments'],
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def getLastestPostID():
        html = crawlUtils.crawlWorker("https://36kr.com/", "Anon", 0)['raw']
        return int(krCrawlMethod.EXTRACT_LATEST_RE.findall(html)[0])

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "https://36kr.com/p/%s"
        latestID = krCrawlMethod.getLastestPostID()
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
            rulesObj.append({'name': 'author', 'rule': ['div', {'class': 'author-detail-info-header'}, 0]})

        if 'author_description' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author_description', 'rule': ['p', {'class': 'author-description'}, 0]})

        if 'author_article_count' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author_article_count', 'rule': ['div', {'class': 'author-article-count'}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'summary'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'articleDetailContent'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'time', 'rule': ['span', {'class': 'item-time'}, 0]})

        if 'thumb_count' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'thumb_count', 'rule': ['div', {'class': 'thumbNum'}, 0]})

        if 'comments' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'comments', 'rule': ['ul', {'class': 'comment-list'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
