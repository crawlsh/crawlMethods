# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class dzzqCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "dzzq"
    DESCRIPTION = "爬取大众证券"
    EXAMPLE_URL = "http://www.dzzq.com.cn/finance/41337611.html"
    GET_LINK_REGEX = re.compile("<a href=\"/finance/(.+?).html\">")
    USING_SOUP = int("1")
    REQUIREMENT = {
        "info": {
            "labels": ['title', 'article'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": True,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }
    """
    This function should generate all links user want to crawl
    
    For example, if user want to crawl 20 articles randomly, 
    this function should generate links of these articles
    
    If you need to crawl any page, use utils.crawlUtils.crawlWorker(url), 
    for more info, see https://docs.crawl.sh/
    
    return in an array please 😊
    """

    @staticmethod
    def requestAPIForURL(amount):
        amount = float(amount)
        i = amount / 30
        j = amount // 30
        needPages = int(i) if i == j else int(i) + 1
        result = []
        for i in range(1, 1 + needPages):
            APIURL = "http://www.dzzq.com.cn/list_111_%s.html" % i
            html = crawlUtils.crawlWorker(APIURL, "Anon", 0)['raw'] \
                .replace("<html><body><p>", "") \
                .replace("</p></body></html>", "")
            links = dzzqCrawlMethod.GET_LINK_REGEX.findall(html)
            for i in links:
                if "list" not in i and i[0] != "S":
                    result.append("http://www.dzzq.com.cn/finance/%s.html" % i)
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return dzzqCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        return

    """
    This function should generate rules

    For example, if user want to crawl title of the articles, 
    this function should generate regex/soup rules of title

    return in an array please 😊
    """

    @staticmethod
    def generateSoupRules(userParamObj):
        rulesObj = []

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['div', {'class': 'tthd'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'article'}, 0]})

        return rulesObj

    """
    [Optional]
    You can ignore this if everything works fine with foregoing functions
    
    This function can modify the html before it is analyzed by rules.
    
    For example, if you want to match the title of article but you replaced the title with empty string,
    the result would also be empty.
    """

    @staticmethod
    def replaceSoup(soup):
        return soup
