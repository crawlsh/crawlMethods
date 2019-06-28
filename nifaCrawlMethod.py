# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class nifaCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "nifa"
    DESCRIPTION = "爬取互联网金融协会"
    EXAMPLE_URL = "http://www.nifa.org.cn/nifa/2955675/2955761/2982417/index.html"
    GET_LINK_REGEX = re.compile("<a href=\"/nifa/(.+?)/(.+?)/(.+?)index.html\"")
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['title', 'time', 'article'],  # Implement here!
            "isCrawlByIDAvailable": False,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
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
        i = amount / 10
        j = amount // 10
        needPages = int(i) if i == j else int(i) + 1
        result = []
        for i in range(1, 1 + needPages):
            APIURL = "http://www.nifa.org.cn/nifa/2955675/2955761/a704445f/index%s.html" % i
            html = crawlUtils.crawlWorker(APIURL, "Anon", 0)['raw']
            links = nifaCrawlMethod.GET_LINK_REGEX.findall(html)
            for j in links:
                result.append("http://www.nifa.org.cn/nifa/%s/%s/%s/index.html" % (j[0], j[1], j[2]))
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return nifaCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        return

    """
    This function should generate rules

    For example, if user want to crawl title of the articles, 
    this function should generate regex/soup rules of title

    return in an array please 😊
    """

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['td', {'class': 'dabiaoti'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'time', 'rule': ['td', {'class': 'zi8'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['table', {'width': '720'}, 0]})

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
