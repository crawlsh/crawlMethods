# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import json


class eeoCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "eeo"
    DESCRIPTION = "爬取经济观察网"
    EXAMPLE_URL = "http://www.eeo.com.cn/2019/0617/358786.shtml"
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
        i = amount / 10
        j = amount // 10
        needPages = int(i) if i == j else int(i) + 1
        result = []
        for i in range(1, 1 + needPages):
            try:
                APIURL = "http://app.eeo.com.cn/?app=wxmember&controller=index&action=getMoreArticle&catid=3572" \
                         "&allcid=358818,358815,358809,358808,358799,358795,358777,358775,358767,358763,358761,358740," \
                         "358732,358730,358718,358712&page=%s" % i
                jsonData = crawlUtils.requestJsonWithProxy(APIURL, needCut=True)
                links = [x["url"] for x in jsonData["article"]]
                result += links
            except:
                pass
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return eeoCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        return

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['div', {'class': 'xd_zuozheinfo'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'xd-nr'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
