# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class geekparkCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "geekpark"
    DESCRIPTION = "爬取极客公园"
    EXAMPLE_URL = "http://www.geekpark.net/news/243272"
    USING = "Soup"
    EXTRACT_LATEST_RE = re.compile("\"id\":(.+?),")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'tag', 'title',
                       'article', 'time', 'thumb_count'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def getLastestPostID():
        html = crawlUtils.crawlWorker("http://www.geekpark.net/", "Anon", 0)['raw']
        return int(geekparkCrawlMethod.EXTRACT_LATEST_RE.findall(html)[1])

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "http://www.geekpark.net/news/%s"
        latestID = geekparkCrawlMethod.getLastestPostID()
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
            rulesObj.append({'name': 'author', 'rule': ['a', {'class': 'author'}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'topic-cover'}, 0]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['section', {'class': 'tags'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {'class': 'topic-title'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'article-content'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'time', 'rule': ['span', {'class': 'release-date'}, 0]})

        if 'thumb_count' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'thumb_count', 'rule': ['div', {'class': 'like-wrap'}, 0]})
        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
