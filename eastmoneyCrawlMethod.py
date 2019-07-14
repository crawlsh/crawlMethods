# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class eastmoneyCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "eastmoney"
    DESCRIPTION = "爬取东方财务网"
    EXAMPLE_URL = "http://finance.eastmoney.com/a/201906251160280558.html"
    USING = "Soup"
    GET_LINK_REGEX = re.compile("</span> <a target=\"_blank\" href=\"(.+?)\">")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'title', 'time', 'summary', 'article'],  # Implement here!
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
                APIURL = "http://finance.eastmoney.com/a/cywjh_%s.html" % i
                html = crawlUtils.requestWithProxy(APIURL)[0]
                links = eastmoneyCrawlMethod.GET_LINK_REGEX.findall(html)
                result += links
            except:
                pass
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return eastmoneyCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        return

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['div', {'class': 'data-source'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'time', 'rule': ['div', {'class': 'time'}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'b-review'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'id': 'ContentBody'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
