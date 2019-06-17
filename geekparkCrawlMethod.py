# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod


class geekparkCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "geekpark"
    DESCRIPTION = "爬取极客公园"
    EXAMPLE_URL = "http://www.geekpark.net/news/243272"
    USING_SOUP = int("1")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'tag', 'title',
                       'article', 'time', 'thumb_count'],  # Implement here!
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
    def generateLinks(userParamObj):
        urlTemplate = "http://www.geekpark.net/news/%s"
        if userParamObj["crawlBy"] == "ORDER":
            result = [
                urlTemplate % i
                for i in range(243272 - int(userParamObj["info"]["amount"]), 243272)
            ]
            return result
        if userParamObj["crawlBy"] == "ID":
            result = [urlTemplate % i for i in range(
                int(userParamObj["info"]["idRangeStart"]),
                int(userParamObj["info"]["idRangeEnd"]))
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
    def generateSoupRules(userParamObj):
        rulesObj = []

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['a', {'class': 'author'}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'topic-cover'}, 0]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['section', {'class': 'tags'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {'class': 'topic-title'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'article-content'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'time', 'rule': ['span', {'class': 'release-date'}, 0]})

        if 'thumb_count' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'thumb_count', 'rule': ['div', {'class': 'like-wrap'}, 0]})
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
