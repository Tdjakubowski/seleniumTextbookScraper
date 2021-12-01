import searchList as sL
import seleniumScraper as scraper

def main():
    i=0
    googleList = []
    results = []
    individualResults = []
    className = input('Input Class Name:').upper()
    section = 'Section:'+input('Input 3 Digit Section Number(ex: 001):')
    browser = input('Input 1 for Chrome(ChromeDriver), or 2 for Firefox(GeckoDriver):')
    textbook = sL.searchTextbookList(className,section,'textbookList.txt')

    #If it doesn't return a textbook, adds a space inbetween className
    for i in range(2):
        if textbook == None:
            textbook = sL.searchTextbookList(className[:3]+' '+className[3:],section,'textbookList.txt')

    if str(textbook[2]) == 'No Textbook Assigned':
        print('No Textbook Assigned')
        return 'No Textbook Assigned'
    else:
        driver = scraper.seleniumStartup(browser)    
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
                individualResults.append(book)
        except AttributeError:
            big = 'sad' #Google couldn't get any textbooks
        if isuList != None:
            individualResults.append(isuList)
        if amazonList != None:
            individualResults.append(amazonList)
        results.append(individualResults)
            
    driver.quit()

    for i in range(len(results)):
        cheapest = 99999.99
        cheapestIndex = 999
        print('\n')
        print(r'////////////////////Book '+str(i+1)+r'\\\\\\\\\\\\\\\\\\\\')
        print('\n')
        for x in range(len(results[i])):
            print('Price: '+str(results[i][x][0])+' Seller: '+str(results[i][x][1])+' URL: '+str(results[i][x][2])+'\n')
            try:
                if cheapest > float(results[i][x][0][1:]):
                    cheapestIndex = x
            except ValueError:
                if cheapest > float(results[i][x][0][2:]):
                    cheapestIndex = x
        print('\n Cheapest Book:\nPrice: '+str(results[i][cheapestIndex][0])+' Seller: '+str(results[i][cheapestIndex][1])+' URL: '+str(results[i][cheapestIndex][2])+'\n')
    

main()
