availableModules = ["ethercap", "kr"]
crawlMethodsInfo = {}
crawlMethodsInfoHTML = ""

for module in availableModules:
    try:
        exec ("from crawlMethods.%sCrawlMethod import %sCrawlMethod" % (module, module))
        exec ("name = %sCrawlMethod.NAME" % module)
        exec ("description = %sCrawlMethod.DESCRIPTION" % module)
        exec ("exampleLink = %sCrawlMethod.EXAMPLE_URL" % module)
        exec ("requirement = %sCrawlMethod.REQUIREMENT" % module)

        crawlMethodsInfo[module] = {
            "name": name,
            "description": description,
            "requirement": requirement,
            "exampleLink": exampleLink,
        }
        crawlMethodsInfoHTML += '<option data-tokens="" data-subtext="%s" value="%s" id="mode1">%s</option>' \
            % (description, module, name)

    except Exception as e:
        print(e)

