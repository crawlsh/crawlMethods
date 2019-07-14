# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import json


class inewsweekCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "inewsweek"
    DESCRIPTION = "爬取Inewsweek"
    EXAMPLE_URL = "http://www.inewsweek.cn/society/2019-06-25/6151.shtml"
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'title', 'article'],  # Implement here!
            "isCrawlByIDAvailable": False,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def requestAPIForURL(amount):
        amount = float(amount)
        i = amount / 20
        j = amount // 20
        needPages = int(i) if i == j else int(i) + 1
        result = []
        for i in range(1, 1 + needPages):
            try:
                APIURL = "http://channel.inewsweek.chinanews.com/u/zk.shtml?pager=%s" % i
                jsonData = crawlUtils.requestJsonWithProxy(APIURL, needCut=True)
                result += [x["url"] for x in jsonData["docs"]]
            except:
                pass
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return inewsweekCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        return

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['div', {'class': 'editor'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'contenttxt'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
