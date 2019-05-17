# -*- coding:utf-8 -*-
import argparse
import copy

tmpl = """# -*- coding:utf-8 -*-
import baseCrawlMethod


class CSH@$NAME$@CrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "CSH@$NAME$@"
    DESCRIPTION = "CSH@$DESC$@"
    EXAMPLE_URL = "CSH@$EXAMPLE$@"
    USING_SOUP = int("CSH@$SOUPUSAGE$@")
    REQUIREMENT = {
        "info": {
            "labels": [],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": True,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }
    \"""
    This function should generate all links user want to crawl
    
    For example, if user want to crawl 20 articles randomly, 
    this function should generate links of these articles
    
    If you need to crawl any page, use utils.crawlUtils.crawlWorker(url), 
    for more info, see https://docs.crawl.sh/
    
    return in an array please 😊
    \"""

    @staticmethod
    def generateLinks(params):
        \"""
        Implement here!
        \"""
        return

    \"""
    This function should generate rules
    
    For example, if user want to crawl title of the articles, 
    this function should generate regex/soup rules of title
    
    return in an array please 😊
    \"""

    @staticmethod
    def generateCSH@$USING_SOUP_STRING$@Rules(userParamObj):
        \"""
        Implement here!
        \"""
        return

    \"""
    [Optional]
    You can ignore this if everything works fine with foregoing functions
    
    This function can modify the html before it is analyzed by rules.
    
    For example, if you want to match the title of article but you replaced the title with empty string,
    the result would also be empty.
    \"""

    @staticmethod
    def replaceSoup(soup):
        return soup
"""


def generateModule(args):
    content = copy.deepcopy(tmpl)
    NAME = args.name.lower()
    content = content.replace("CSH@$NAME$@", NAME)
    DESCRIPTION = args.desc
    content = content.replace("CSH@$DESC$@", DESCRIPTION)
    EXAMPLE_URL = args.example
    content = content.replace("CSH@$EXAMPLE$@", EXAMPLE_URL)
    USING_SOUP = int(args.rule == "s")
    USING_SOUP_STRING = "Soup" if USING_SOUP else "Regex"
    content = content.replace("CSH@$SOUPUSAGE$@", str(USING_SOUP))
    content = content.replace("def generateCSH@$USING_SOUP_STRING$@Rules",
                              "def generate%sRules" % USING_SOUP_STRING)
    fileName = '%sCrawlMethod.py' % NAME
    newFile = open(fileName, 'w')
    newFile.write(content)
    newFile.close()
    print("Done! File is at %s" % fileName)


parser = argparse.ArgumentParser(
    description="This is a tool about crawl modules of Crawl.sh")
subparsers = parser.add_subparsers(help='commands')

generateModuleParser = subparsers.add_parser('new', help='Add a new module')
generateModuleParser.add_argument('name', action='store', help='name of the module, e.g. baidu')
generateModuleParser.add_argument('desc', action='store', help='description of the module')
generateModuleParser.add_argument('example', action='store',
                                  help='an exmaple link of the content you are going to crawl')
generateModuleParser.add_argument('rule', action='store',
                                  help='either generate rules by regex or by soup, use r/s to represent each')
generateModuleParser.set_defaults(func=generateModule)

args = parser.parse_args()
args.func(args)
