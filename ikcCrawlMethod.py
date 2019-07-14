# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import json


class ikcCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "ikc"
    DESCRIPTION = "爬取爱砍柴网"
    EXAMPLE_URL = "http://tech.ikanchai.com/article/20190618/293675.shtml"
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['tag', 'title', 'author',
                       'article'],  # Implement here!
            "isCrawlByIDAvailable": False,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def requestAPIForURL(amount):
        APIURL = "http://app.ikanchai.com/roll.php?do=more&status=1&sort=0&pagesize=%s&page=0" % amount
        jsonData = crawlUtils.requestJsonWithProxy(APIURL, needCut=True)
        result = [x["url"] for x in jsonData["data"]]
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return ikcCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        return

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['div', {'class': 'key_ad'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {'class': 'show_title'}, 0]})

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['div', {'class': 'show_topview'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'show_content'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
