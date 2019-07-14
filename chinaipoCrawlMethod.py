# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import json


class chinaipoCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "chinaipo"
    DESCRIPTION = "爬取China IPO"
    EXAMPLE_URL = "http://m.chinaipo.com/vc/83640.html"
    USING = "Json"
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'title', 'article', 'tag', 'time'],  # Implement here!
            "isCrawlByIDAvailable": False,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def requestAPIForURL(amount):
        amount = float(amount)
        i = amount / 10
        j = amount // 10
        needPages = int(i) if i == j else int(i) + 1
        result = []
        for i in range(1, 1 + needPages):
            try:
                APIURL = "http://api.chinaipo.com/zh-hans/api/articles/?page=%s" % i
                jsonData = crawlUtils.requestJsonWithProxy(APIURL)
                for j in jsonData["results"]:
                    originalId = j["originalId"]
                    result.append("http://api.chinaipo.com/zh-hans/api/article/?originalId=%s" % originalId)
            except:
                pass
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return chinaipoCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        return

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ["results", 0, "source"]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ["results", 0, "tags"]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ["results", 0, "title"]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ["results", 0, "content", "content"]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'time', 'rule': ["results", 0, "publishing_date"]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
