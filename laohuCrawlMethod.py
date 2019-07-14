# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class laohuCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "laohu"
    DESCRIPTION = "爬取老虎财经网"
    EXAMPLE_URL = "http://www.laohucaijing.com/Www_detail/index/133977/"
    USING = "Soup"
    GET_LINK_REGEX = re.compile("href=\"(.+?)\"")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'title', 'article', 'view_count', 'tag'],  # Implement here!
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
            APIURL = "http://www.laohucaijing.com/laohu_index1/ajax_news_list/?page=%s" % i
            html = crawlUtils.requestJsonWithProxy(APIURL)["html"]
            links = laohuCrawlMethod.GET_LINK_REGEX.findall(html.replace("\/", "/"))
            for j in set(links):
                if "author_detail" not in j:
                    result.append("http://www.laohucaijing.com%s" % j)
        return result

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "http://www.laohucaijing.com/Www_detail/index/%s/"
        if userParamObj["crawlBy"] == "ORDER":
            return laohuCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        if userParamObj["crawlBy"] == "ID":
            result = [urlTemplate % i for i in range(
                int(userParamObj["info"]["idRangeStart"]),
                int(userParamObj["info"]["idRangeEnd"]))
                      ]
            return result

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['div', {'class': 'artInfo1'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'text'}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'artDeta'}, 0]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['p', {'class': 'Label'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
