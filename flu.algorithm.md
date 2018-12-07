    date = get date
    year = date.year
    
    def parse(self,reponse):
        llst = getLintlist(links)
        if(firstRun()):
            for lnl in llst:
                yield req(url=lnk, callback= downloadPDF())
         else:
            for lnk in llst:
                if lnk.contains(year):
                    req(url=lnk, callback= downloadPDF())
            