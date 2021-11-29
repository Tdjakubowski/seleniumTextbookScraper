import searchList as sL
import seleniumScraper as scraper


def main():
    i=0
    resultsRetrieved = False
    results = []
    className = input('Input Class Name:')
    section = 'Section:'+input('Input 3 Digit Section Number(ex: 001):')

    textbook = sL.searchTextbookList(className,section)
    #Need to adjust to account for several books
    for i in range(2):
        if textbook == None:
            textbook = sL.searchTextbookList(className[:3]+' '+className[3:],section)
        
    if str(textbook[2]) == 'No Textbook Assigned':
        print('No Textbook Assigned')
        return 'No Textbook Assigned'
    else:
        driver = scraper.seleniumStartup(1)
        while not resultsRetrieved and i<5:
            try:
                googleList = scraper.googleScraping(driver,textbook[2])
                resultsRetrieved = True
            
            except ProcessLookupError: #There is a raised exception in googleScraping in seleniumScraper, this catches it and tries again
                resultsRetrieved=False
                i+=1
            
        isuList = scraper.isuBookstoreScraping(driver,textbook[2])
        amazonList = scraper.amazonScraping(driver,textbook[2])
        try:
            for book in googleList:
                results.append(book)
        except AttributeError:
            big = 'sad'
        if isuList != None:
            results.append(isuList)
        if amazonList != None:
            results.append(amazonList)
        print(results)
        driver.quit()
        return results
        
    

main()
