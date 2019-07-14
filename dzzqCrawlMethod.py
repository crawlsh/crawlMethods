# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class dzzqCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "dzzq"
    DESCRIPTION = "爬取大众证券"
    EXAMPLE_URL = "http://www.dzzq.com.cn/finance/41337611.html"
    GET_LINK_REGEX = re.compile("<a href=\"/finance/(.+?).html\">")
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['title', 'article'],  # Implement here!
            "isCrawlByIDAvailable": False,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def requestAPIForURL(amount):
        amount = float(amount)
        i = amount / 30
        j = amount // 30
        needPages = int(i) if i == j else int(i) + 1
        result = []
        for i in range(1, 1 + needPages):
            APIURL = "http://www.dzzq.com.cn/list_111_%s.html" % i
            html = crawlUtils.crawlWorker(APIURL, "Anon", 0)['raw']
            links = dzzqCrawlMethod.GET_LINK_REGEX.findall(html)
            for j in links:
                if "list" not in j and j[0] != "S":
                    result.append("http://www.dzzq.com.cn/finance/%s.html" % j)
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return dzzqCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        return

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['div', {'class': 'tthd'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'article'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
