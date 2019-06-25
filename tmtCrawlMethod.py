# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import json


class tmtCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "tmt"
    DESCRIPTION = "爬取钛媒体"
    EXAMPLE_URL = "https://www.tmtpost.com/4011711.html"
    USING = "Soup"
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'tag', 'time', 'title', 'summary',
                       'article', 'thumb_count', 'comments'],  # Implement here!
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
        i = amount / 10
        j = amount // 10
        needPages = int(i) if i == j else int(i) + 1
        result = []
        for i in range(1, 1 + needPages):
            APIURL = "https://www.tmtpost.com/httpsserver/common/get?url=/v1/lists/home&data=offset=%s" % (i*10)
            html = crawlUtils.crawlWorker(APIURL, "Anon", 0)['raw']\
                .replace("<html><body><p>", "")\
                .replace("</p></body></html>", "")
            print(html)
            jsonData = json.loads(html)
            for x in jsonData["data"]:
                if x["item_type"] == "post":
                    result.append(x["short_url"])
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return tmtCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
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
            rulesObj.append({'name': 'author', 'rule': ['a', {'class': 'color-orange'}, 0]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['div', {'class': 'post-tags'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'time', 'rule': ['span', {'class': 'time'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'summary' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'summary', 'rule': ['p', {'class': 'post-abstract'}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'inner'}, 0]})

        if 'thumb_count' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'thumb_count', 'rule': ['a', {'class': 'like'}, 0]})

        if 'comments' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'comments', 'rule': ['div', {'class': 'post-comment'}, 0]})

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
