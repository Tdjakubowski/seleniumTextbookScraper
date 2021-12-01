from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options as ff_options
from selenium.webdriver.chrome.options import Options as cr_options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import re




"""
Setting this up will be a headache, no matter what kind of browser you use
In order for this to work on Firefox, you have to download Selenium(pip install Selenium in cmd), download geckodriver (https://github.com/mozilla/geckodriver/releases)
In order for this to work on Chrome, you have to download Selenium(pip install Selenium in cmd), download ChromeDriver(find out your chromeversion, then just search it up)

After that you have two more options:
Go to advanced system settings in your pc, go to environment variables, into path, and add the path to the driver

OR

type this in cmd: setx PATH "%PATH%;C:\INPUT PATH TO WEBDRIVER HERE"
"""

def main():
    webBrowserChoice = input('Choose a browser:\n1.Firefox\n2.Chrome (Recommended)')
    
    driver = seleniumStartup(webBrowserChoice)
    ISBN = '9781442222502' 
    
    #barnesAndNobleResults = [] #[buyNew,buyUsed,rentNew,rentUsed,rentReturn] If one of the items is unavailable, it will return None
    #barnesAndNobleResults= barnesAndNobleScraping(driver,ISBN)

    #[Cost of book, Website it came from, If it's used, URL to Website]
    googleResults = googleScraping(driver,ISBN)

    amazonResults = amazonScraping(driver,ISBN)
    driver.quit()

#Attempts to start a Firefox webdriver using Selenium, I did firefox because I don't want to redownload chrome, even though chrome is probably better for this process

def seleniumStartup(webBrowserChoice):
    
    for i in range(3):

        #Actually starting the webdriver. Will do 3 attempts then shut down if it fails. If it works, returns the driver
        try:
            #Start a firefox webdriver
            if int(webBrowserChoice) == 2:
                options = ff_options()
                options.headless = True
                driver = webdriver.Firefox(options=options)
                print("Driver loaded.")
                return driver
            #Start a chrome webdriver
            else:
                options = cr_options()
                options.headless = False
                driver = webdriver.Chrome(options=options)
                print("Driver loaded.")
                return driver

        except exceptions.WebDriverException as err:
            print("Driver Failed. Attempt #"+str(i+1)+"/3")
    if i == 2:
        print("Webdriver Load Failed. Shutting Down.")
        exit()
        

def googleScraping(driver,ISBN):
    results = []
    driver.get('https://www.google.com/')

    searchBar = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    searchBar.click()
    searchBar.send_keys(ISBN)
    searchBar.submit()
    
    #Getting to the shopping page
    try:
        shoppingButton = WebDriverWait(driver, 2).until(expected_conditions.visibility_of_element_located((By.XPATH,'/html/body/div[7]/div/div[3]/div/div[1]/div/div[1]/div/div[5]/a')))
        shoppingButton.click()
    except exceptions.TimeoutException:
        shoppingButton = driver.find_element_by_xpath('/html/body/div[7]/div/div[4]/div/div[1]/div/div[1]/div/div[5]/a')
        shoppingButton.click()
    
    try:
        #If it finds this, then its on the wrong page and redirects
        shoppingCheck = WebDriverWait(driver, 2).until(expected_conditions.visibility_of_element_located((By.XPATH,'/html/body/div[7]/div/div[10]/div[1]/div/div[2]/div[1]/div/div/p[1]')))
        shoppingButton = driver.find_element_by_xpath('/html/body/div[7]/div/div[4]/div/div[1]/div/div[1]/div/div[4]/a')
        shoppingButton.click()
    except exceptions.TimeoutException:
        vibeCheck = 'passed'
    
    #Trying to find a button that'll take us to the page with all of the prices. If all fails, sends ProcessLookupError which is caught in bringItAllTogether
    try:
        comparePricesButton = WebDriverWait(driver, 2).until(expected_conditions.visibility_of_element_located((By.XPATH,'/html/body/div[6]/div/div[3]/div[4]/div/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[3]/div/a')))
    except exceptions.TimeoutException:
        try:
            comparePricesButton=driver.find_element_by_xpath('/html/body/div[7]/div/div[9]/div[4]/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[3]/div/a')
        except exceptions.NoSuchElementException:
            try:
                comparePricesButton = driver.find_element_by_xpath('/html/body/div[7]/div/div[9]/div[4]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[3]/div/a')
            except exceptions.NoSuchElementException:               
                try:
                    comparePricesButton = driver.find_element_by_xpath('/html/body/div[6]/div/div[3]/div[4]/div/div[3]/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[3]/div/a')
                except exceptions.NoSuchElementException:
                    try:
                        comparePricesButton = driver.find_element_by_xpath('/html/body/c-wiz[2]/div/div/div[1]/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div[1]/div/div/div/div/article/div/div[2]/div[2]/a')                  
                    except exceptions.NoSuchElementException:
                        try:
                            comparePricesButton = driver.find_element_by_xpath('/html/body/div[7]/div/div[10]/div[4]/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[3]/div/a')
                        except exceptions.NoSuchElementException:
                            try:
                                comparePricesButton = driver.find_element_by_xpath('/html/body/div[7]/div/div[10]/div[4]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[3]/div/a')
                            except exceptions.NoSuchElementException:
                                raise ProcessLookupError("Couldn't access next page.")
    comparePricesButton.click()  
    
    #Scraping the cost, where to buy it,  and the URL for a specific seller. If an scraping is thrown, it skips the line and moves to the next one. Also, regex is used to search through scraped data to grab specifics                
    #If an AttributeError is raised, it'll read the innerHTML without calling group()
    for i in range(len(WebDriverWait(driver,2).until(expected_conditions.presence_of_all_elements_located((By.XPATH,'/html/body/div[4]/div[2]/div/div[3]/div/table/tbody/tr'))))):
        try:
            try:
                cost = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div/table/tbody/tr['+str(i+1)+']/td[3]').get_attribute('innerHTML')
                cost = re.search('\W\d\d\.\d\d',cost).group(0)#Pulls the price w/ the dollar sign
            except AttributeError:
                cost = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div/table/tbody/tr['+str(i+1)+']/td[3]/span').get_attribute('innerHTML')
            
            website = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div/table/tbody/tr['+str(i+1)+']/td[1]/div[1]/a').get_attribute("innerHTML")
            website = re.search('.+?(?=<)',website).group(0)#Pulls everything before the first '<'
            
            URL = (driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div/table/tbody/tr['+str(i+1)+']/td[5]/div/a').get_attribute('href'))
            results.append([cost,website,URL])
        except exceptions.NoSuchElementException:
            i+=1

    return results

def isuBookstoreScraping(driver,ISBN):
    
    driver.get('https://ilstu.bncollege.com/')

    #Input the ISBN into the search
    searchbutton = driver.find_element_by_xpath("/html/body/main/header/div[7]/div/div/section[1]/div/div[2]/button[1]")
    searchBar = driver.find_element_by_xpath("//*[@id='bned_site_search']")
    try:
        searchBar.click()
    except exceptions.ElementNotInteractableException:
        searchbutton.click()
        searchBar.click()
    searchBar.send_keys(ISBN)
    searchBar.submit()
    

    try: #The first try would be the cheapest price, then as it fails to grab one it takes the next cheapest, until you'd be buying a new book
        price = WebDriverWait(driver,2).until(expected_conditions.visibility_of_element_located((By.XPATH,'/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[2]/div/label/span[1]'))).get_attribute("innerHTML")
    except exceptions.TimeoutException:
        try:
            price = driver.find_element_by_xpath('/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div/label/span[1]').get_attribute("innerHTML")
        except exceptions.NoSuchElementException:
            try:
                price = driver.find_element_by_xpath('/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[1]/div[2]/div[2]/div/label/span[1]').get_attribute("innerHTML")
            except exceptions.NoSuchElementException:
                try:
                    price = driver.find_element_by_xpath('/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[1]/div[2]/div[1]/div/label/span[1]').get_attribute("innerHTML")
                except exceptions.NoSuchElementException:
                    return None
        
    URL = driver.current_url
    return [price,"ISU Bookstore",URL]
def amazonScraping(driver,ISBN):
    
    #Pull up search page
    driver.get('https://www.amazon.com/advanced-search/books')

    #Input ISBN
    searchBar = driver.find_element_by_id("field-isbn")
    searchBar.send_keys(ISBN)
    searchBar.send_keys(Keys.ENTER)

    #Waits for first item, then pulls. If fails, tries to press a paperback button to get a different price. If that fails, returns None
    try:
        price = WebDriverWait(driver, 2).until(expected_conditions.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[1]/div/span/div/div/div[2]/div[2]/div/div/div[3]/div[1]/div/div[1]/div[2]/a[1]/span[1]/span[2]/span[2]"))).get_attribute('innerHTML')
        price = '$'+price[:2]+'.'+driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[1]/div/span/div/div/div[2]/div[2]/div/div/div[3]/div[1]/div/div[1]/div[2]/a[1]/span[1]/span[2]/span[3]').get_attribute('innerHTML')
        return [price,'Amazon',driver.current_url]
    
    except exceptions.TimeoutException:
        try:
            paperbackButton = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[1]/div/span/div/div/div[2]/div[2]/div/div/div[3]/div[1]/div/div[1]/div/a')
            paperbackButton.click()
            price = WebDriverWait(driver, 2).until(expected_conditions.visibility_of_element_located((By.XPATH,'//*[@id="usedPrice"]'))).get_attribute('innerHTML')
            return [price,'Amazon',driver.current_url]
        except exceptions.NoSuchElementException:
            return None

#if __name__ == '__main__':
#    main()
