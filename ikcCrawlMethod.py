# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import json


class ikcCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "ikc"
    DESCRIPTION = "爬取爱砍柴网"
    EXAMPLE_URL = "http://tech.ikanchai.com/article/20190618/293675.shtml"
    USING_SOUP = int("1")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'tag', 'title', 'summary',
                       'article'],  # Implement here!
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
        APIURL = "http://app.ikanchai.com/roll.php?do=more&status=1&sort=0&pagesize=%s&page=0" % amount
        html = crawlUtils.crawlWorker(APIURL, "Anon", 0)['raw'] \
            .replace("<html><body><p>", "") \
            .replace("</p></body></html>", "")
        jsonData = json.loads(html)
        result = [x["url"] for x in jsonData["data"]]
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return ikcCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
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

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['span', {'class': 'u'}, 0]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['div', {'class': 'space_k_s'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {'class': 'space_show_title'}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'space_show_desc'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'space_show_content'}, 0]})

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
