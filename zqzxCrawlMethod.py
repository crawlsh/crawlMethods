# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class zqzxCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "zqzx"
    DESCRIPTION = "爬取证券之星"
    EXAMPLE_URL = "https://finance.stockstar.com/JC2019061900000004.shtml"
    GET_LINK_REGEX = re.compile("<a href=\"https://finance.stockstar.com/(.+?).shtml\">")
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'time', 'title', 'article'],  # Implement here!
            "isCrawlByIDAvailable": False,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def requestAPIForURL(amount):
        amount = float(amount)
        i = amount / 60
        j = amount // 60
        needPages = int(i) if i == j else int(i) + 1
        result = []
        for i in range(2, 2 + needPages):
            APIURL = "http://www.stockstar.com/roll/finance_%s.shtml" % i
            html = crawlUtils.crawlWorker(APIURL, "Anon", 0)['raw'] \
                .replace("<html><body><p>", "") \
                .replace("</p></body></html>", "")
            links = zqzxCrawlMethod.GET_LINK_REGEX.findall(html)
            for i in links:
                if "list" not in i and i[0] != "S":
                    result.append("https://finance.stockstar.com/%s.shtml" % i)
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return zqzxCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        return

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['span', {'id': 'source_baidu'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['span', {'id': 'pubtime_baidu'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'article'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
