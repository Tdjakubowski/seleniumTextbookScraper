import searchList as sL
import seleniumScraper as scraper

def main():
    i=0
    googleList = []
    results = []
    individualResults = []
    className = input('Input Class Name:')
    section = 'Section:'+input('Input 3 Digit Section Number(ex: 001):')
    path = input(r"Input path to TextbookList.txt:")+r'\textbookList.txt'
    textbook = sL.searchTextbookList(className,section,path)

    #If it doesn't return a textbook, adds a space inbetween className
    for i in range(2):
        if textbook == None:
            textbook = sL.searchTextbookList(className[:3]+' '+className[3:],section,path)

    if str(textbook[2]) == 'No Textbook Assigned':
        print('No Textbook Assigned')
        return 'No Textbook Assigned'
    else:
        driver = scraper.seleniumStartup(1)    
    for x in range(2,len(textbook)): #Will run several times if multiple ISBN's
        resultsRetrieved = False
        while not resultsRetrieved and i<5:
            try:
                googleList = scraper.googleScraping(driver,textbook[x])
                resultsRetrieved = True
        
            except ProcessLookupError: #There is a raised exception in googleScraping in seleniumScraper, this catches it and tries again
                resultsRetrieved=False
                i+=1
            
        isuList = scraper.isuBookstoreScraping(driver,textbook[x])
        amazonList = scraper.amazonScraping(driver,textbook[x])
        
        try:
            for book in googleList:
                results.append(book)
        except AttributeError:
            big = 'sad' #Google couldn't get any textbooks
        if isuList != None:
            individualResults.append(isuList)
        if amazonList != None:
            individualResults.append(amazonList)
        results.append(individualResults)
            
    driver.quit()
    print(results)
    return results
        
    

main()
