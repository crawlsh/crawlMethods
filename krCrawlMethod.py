# -*- coding:utf-8 -*-
import baseCrawlMethod


class krCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "36Kr"
    DESCRIPTION = "Crawl content of 36kr"
    EXAMPLE_URL = "https://36kr.com/p/5205828"
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'author_description', 'author_article_count', 'summary',
                       'article', 'time', 'thumb_count', 'comments'],
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
    
    An example:
        urlTemplate = "https://36kr.com/p/%s"
        if userParamObj["crawlBy"] == "ORDER":
            result = [
                urlTemplate % i
                for i in range(5205828 - int(userParamObj["info"]["amount"]), 5205828)
            ]
            return result
        if userParamObj["crawlBy"] == "ID":
            result = [urlTemplate % i for i in range(
                    int(userParamObj["info"]["idRangeStart"]),
                    int(userParamObj["info"]["idRangeEnd"]))
            ]
            return result
    """

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "https://36kr.com/p/%s"
        if userParamObj["crawlBy"] == "ORDER":
            result = [
                urlTemplate % i
                for i in range(5205828 - int(userParamObj["info"]["amount"]), 5205828)
            ]
            return result
        if userParamObj["crawlBy"] == "ID":
            result = [urlTemplate % i for i in range(
                    int(userParamObj["info"]["idRangeStart"]),
                    int(userParamObj["info"]["idRangeEnd"]))
            ]
            return result

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
            rulesObj.append({'name': 'author', 'rule': ['div', {'class': 'author-detail-info-header'}, 0]})

        if 'author_description' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author_description', 'rule': ['p', {'class': 'author-description'}, 0]})

        if 'author_article_count' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author_article_count', 'rule': ['div', {'class': 'author-article-count'}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['div', {'class': 'summary'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'articleDetailContent'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'time', 'rule': ['span', {'class': 'item-time'}, 0]})

        if 'thumb_count' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'thumb_count', 'rule': ['div', {'class': 'thumbNum'}, 0]})

        if 'comments' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'comments', 'rule': ['ul', {'class': 'comment-list'}, 0]})

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
