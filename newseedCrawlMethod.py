# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod


class newseedCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "newseed"
    DESCRIPTION = "Crawl Content of NewSeed"
    EXAMPLE_URL = "https://news.newseed.cn/p/1354890"
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'title', 'summary',
                       'article', 'time'],  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
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
        urlTemplate = "https://news.newseed.cn/p/%s"
        if userParamObj["crawlBy"] == "ORDER":
            result = [
                urlTemplate % i
                for i in range(1354890 - int(userParamObj["info"]["amount"]), 1354890)
            ]
            return result
        if userParamObj["crawlBy"] == "ID":
            result = [urlTemplate % i for i in range(
                    1354890 - int(userParamObj["info"]["idRangeEnd"]),
                    1354890 - int(userParamObj["info"]["idRangeStart"]))
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

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['span', {'class': 'author'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {'id': 'title'}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'subject'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'news-content'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'time', 'rule': ['span', {'class': 'date'}, 0]})

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
