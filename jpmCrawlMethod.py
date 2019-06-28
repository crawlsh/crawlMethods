# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod


class jpmCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "jpm"
    DESCRIPTION = "爬取金评媒"
    EXAMPLE_URL = "http://www.jpm.cn/article-76489-1.html"
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['title', 'summary',
                       'article', 'comments'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
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
    def generateLinks(userParamObj):
        urlTemplate = "http://www.jpm.cn/article-%s-1.html"
        if userParamObj["crawlBy"] == "ORDER":
            result = [
                urlTemplate % i
                for i in range(76489 - int(userParamObj["info"]["amount"]), 76489)
            ]
            return result
        if userParamObj["crawlBy"] == "ID":
            result = [urlTemplate % i for i in range(
                76489 - int(userParamObj["info"]["idRangeEnd"]),
                76489 - int(userParamObj["info"]["idRangeStart"]))
                      ]
            return result
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
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'writer'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'story_box'}, 0]})

        if 'comments' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'comments', 'rule': ['div', {'class': 'review_read_box'}, 0]})
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
