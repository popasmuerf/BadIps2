#Preprocessing
url_template = 'https://www.gov.uk/government/collections/weekly-national-flu-reports'

this_year = Date.now.year
last_year = this_year - 1


url = geturl(last_year, this_year)


ifexecFlag = context.hasRun()



#Processing

parse(self,body):
    links = []
    ifexecFlag:
        links = getLinks()
        parse(links)
    else:
        links = getLinks()
        parse(links[0])