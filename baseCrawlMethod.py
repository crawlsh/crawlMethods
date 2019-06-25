import json


class crawlMethod():
    # the name of this crawl method
    NAME = ""

    # the description of this crawl method
    DESCRIPTION = ""

    # example url of the website
    EXAMPLE_URL = ""

    # whether this module is only available for VIP
    IS_VIP_REQUIRED = False

    # maximum pages allowed for crawling
    MAXIMUM = 200

    # whether using soup to generate rules
    USING = "SOUP"

    """
        Example Requirement Param:
        {
            "info": {
                "labels": List | None,
                "isCrawlByIDAvailable": Bool,
                "isCrawlByTimeAvailable": Bool,
                "isCrawlByOrderAvailable": Bool,
            }
        }
    
    """
    REQUIREMENT = {}

    """
            Example User Param:
            {
                "info": {
                    "idRangeStart": Integer | None | ..,
                    "idRangeEnd": Integer | None | ..,
                    "timeRangeEnd": Integer | None | ..,
                    "timeRangeEnd": Integer | None | ..,
                    "requiredContent": String | List, 
                    "amount": Integer, 
                },
                "crawlBy": "ORDER" | "ID" | "TIME",
            }
            idRangeStart : if using CRAWL_BY_ID, showing the start of the id
            idRangeEnd : if using CRAWL_BY_ID, showing the end of the id
            timeRangeStart : if using CRAWL_BY_TIME, showing the start of the time
            timeRangeStart : if using CRAWL_BY_TIME, showing the start of the time
            requiredContent : what user needed
            amount : if using CRAWL_BY_ORDER, showing the amount
            crawlBy: either by random order or id
    """

    @staticmethod
    def paramParser(string):
        return json.loads(string)

    @staticmethod
    def generateLinks(params):
        return

    @staticmethod
    def generateRules(userParamObj):
        return userParamObj["info"]["requiredContent"]

    @staticmethod
    def replaceHTML(html):
        return html

    @staticmethod
    def replaceSoup(soup):
        return soup

