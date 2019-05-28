from crawlMethods import baseCrawlMethod


class ethercapCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "Ethercap"
    DESCRIPTION = "Crawl Pages of Ethercap"
    EXAMPLE_URL = "https://www.ethercap.com/cases/view?id=302"
    IS_VIP_REQUIRED = False
    MAXIMUM = 200
    USING_SOUP = False
    REQUIREMENT = {
        "info": {
            "labels": ["title", "author", "content"],
            "isCrawlByIDAvailable": True,
            "isCrawlByTimeAvailable": False,
            "isCrawlByOrderAvailable": True,
        }
    }

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "https://www.ethercap.com/cases/view?id=%s"
        if userParamObj["crawlBy"] == "ORDER":
            result = [
                urlTemplate % i
                for i in range(321 - int(userParamObj["info"]["amount"]), 321)
            ]
            return result
        if userParamObj["crawlBy"] == "ID":
            result = [urlTemplate % i for i in range(
                    int(userParamObj["info"]["idRangeStart"]),
                    int(userParamObj["info"]["idRangeEnd"]))
            ]
            return result

    @staticmethod
    def generateSoupRules(userParamObj):
        rulesObj = []
        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})
        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['p', {'class': ['auth-info']}, 0]})
        if 'content' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'content', 'rule': ['div', {'class': ['article-content']}, 0]})
        return rulesObj

    @staticmethod
    def generateRegexRules(userParamObj):
        rulesObj = []
        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': "<h1>(.+?)</h1>"})
        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': "<p class=\"auth-info\">(.+?)</p>"})
        if 'content' in userParamObj["info"]["requiredContent"]:
            rulesObj.append("")
        return rulesObj