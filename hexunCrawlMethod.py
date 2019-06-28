# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class hexunCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "hexun"
    DESCRIPTION = "爬取合讯创投网"
    EXAMPLE_URL = "http://pe.hexun.com/2019-06-24/197618574.html"
    USING = "Soup"
    REGEX_FINDING_LINKS = re.compile("class=\"newtit\" id=\"h(.+?)\" href=\"" +
                                     "http://pe\.hexun\.com/(.+?)/([0-9].+?)\.html\" target=\"_blank\">")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'time', 'title', 'article'],  # Implement here!
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
        homePage = crawlUtils.requestWithProxy("http://pe.hexun.com")[0]
        links = hexunCrawlMethod.REGEX_FINDING_LINKS.findall(homePage)[0]
        return ["http://pe.hexun.com/%s/%s.html" % (x[1], x[2]) for x in links[:amount]]

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return hexunCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
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

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['a', {'rel': 'nofollow'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'time', 'rule': ['span', {'class': 'pr20'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {"class": "art_contextBox"}, 0]})

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
