from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time




"""
TO DO:
1. Make it headless with Chrome
2. Sort through closerClass and pull out individual variables, may be an issue since some books get doubled up into 1 index
3. Pull from the Alamo II and Barnes and Noble, so we have some textbooks on campus
4. Ensure it works with different books(I used this book because I currently have the book, and I never changed it)

Other Notes:
Setting this up will be a headache, no matter what kind of browser you use
In order for this to work on Firefox, you have to download Selenium(pip install Selenium in cmd), download geckodriver (https://github.com/mozilla/geckodriver/releases)
In order for this to work on Chrome, you have to download Selenium(pip install Selenium in cmd), download ChromeDriver(find out your chromeversion, then just search it up)

After that you have two more options:
Go to advanced system settings in your pc, go to environment variables, into path, and add the path to the driver

OR

type this in cmd: setx PATH "%PATH%;C:\INPUT PATH TO DRIVER HERE"
"""

def main():
    webBrowserChoice = input('Choose a browser:\n1.Firefox\n2.Chrome (Recommended)')
    
    driver = seleniumStartup(webBrowserChoice)
    ISBN = '9781442222502'
    
    #googleScraping(driver,ISBN)
    #alamoScraping(driver,ISBN)
    
    barnesAndNobleResults=[]
    barnesAndNobleResults = barnesAndNobleScraping(driver,ISBN)
    driver.quit()

#Attempts to start a Firefox webdriver using Selenium, I did firefox because I don't want to redownload chrome, even though chrome is probably better for this process

def seleniumStartup(webBrowserChoice):
    
    #Ensures the webdriver will load w/o GUI
    options = Options()
    
    
    for i in range(3):

        #Actually starting the webdriver. Will do 3 attempts then shut down if it fails. If it works, returns the driver
        try:
            #Start a firefox webdriver
            if int(webBrowserChoice) == 1:
                #options.headless = True
                driver= webdriver.Firefox(options=options)
                print("Driver loaded.")
                return driver
            #Start a chrome webdriver
            else:
                #some command goes here to make it headless
                driver = webdriver.Chrome()
                print("Driver loaded.")
                return driver

        except exceptions.WebDriverException as err:
            print("Driver Failed. Attempt #"+str(i+1)+"/3")
    if i == 2:
        print("Error: ",err)
        print("Webdriver Load Failed. Shutting Down.")
        exit()
        

#this code is ridiculously scuffed, if we have enough time at the end I'll try to go back and fix it, but idk man I gotta rewrite this entire class    
def googleScraping(driver,ISBN):
    #Grabbing the entire webpage
    #I broke it up because my IDE cant scroll horizontally, and trying to transport imports to a different IDE is irritating :/
    driver.get("https://www.google.com/search?q=Information+Technology+Project+Management:+Providing+Measurable+"+
               "Organizational+Value,+5th+Edition++Jack+T.+Marchewka&source=lmns&tbm=shop&bih=750&biw=1536&client=firefox-b-1-d&hl=en&sa=X&ved="+
               "2ahUKEwjCgqf8gMvzAhUYU80KHQcFCe0Q_AUoAnoECAEQAg")
    
    #Searches the html for elements named GhTN2e

    #Looking closer at the html pulled, it has all 4, but they're grouped in 2. Soooooooo it technically works :)
    closerClass = driver.find_elements_by_xpath("//div[@class='GhTN2e']")

    #Prints out each element in closerClass
    for element in closerClass:
        print(element.get_attribute("innerHTML")+'\n')
        
    #Self explanitory
    

def alamoScraping(driver,ISBN):
    #Grabs the html, then inputs the ISBN into the search to pull the textbook
    #Notes: This should work, but there's anti-scraping software on the website that prevents progression, so I have to change the app data being sent(hopefully that'll work)
    driver.get("https://www.bkstr.com/illinoisstatestore/home")
    success1=False
    success2=False
    success3=False
    i=0
    while not success3:
        i+=1    
        
        if not success1:
            try:
                searchBar = driver.find_element_by_xpath("//*[@id='searchKeyword']")
                searchBar.click()
                searchBar.send_keys(ISBN)
                success1 = True
                
            except exceptions.ElementClickInterceptedException or exceptions.ElementNotInteractableException:
                
                clickAndHold(driver)
                
        if not success2:
            try: 
                searchButton = driver.find_element_by_xpath('//*[@id="1000180941"]')
                searchButton.click()
                success2 = True
                
            except exceptions.ElementClickInterceptedException or exceptions.ElementNotInteractableException:
                
                clickAndHold(driver)
                
        if not success3:
            try:
                usedRentalPrice = driver.find_element_by_xpath("/html/body/ef-root/ef-store/ef-product-details/ef-adopted-text/main/div/div[3]/ef-course-material-price/div[1]/div/div[1]/div/label/div[3]/span[1]")
                newRentalPrice = driver.find_element_by_xpath("/html/body/ef-root/ef-store/ef-product-details/ef-adopted-text/main/div/div[3]/ef-course-material-price/div[1]/div/div[2]/div/label/div[3]/span[1]")
                rentalReturnDate = driver.find_element_by_xpath("/html/body/ef-root/ef-store/ef-product-details/ef-adopted-text/main/div/div[3]/ef-course-material-price/div[1]/div/div[1]/div/label/div[3]/span[2]")
                buyUsed = driver.find_element_by_xpath("/html/body/ef-root/ef-store/ef-product-details/ef-adopted-text/main/div/div[3]/ef-course-material-price/div[2]/div/div[1]/div/label/div[3]/span")
                buyNew = driver.find_element_by_xpath("/html/body/ef-root/ef-store/ef-product-details/ef-adopted-text/main/div/div[3]/ef-course-material-price/div[2]/div/div[2]/div/label/div[3]/span")
                print(usedRentalPrice,newRentalPrice,rentalReturnDate,buyUsed,buyNew)
                success3=True
            except exceptions.ElementClickInterceptedException or exceptions.ElementNotInteractableException:
                discountCaptcha = driver.find_elements_by_xpath('//*[@id="modalForAPIChallenge"]')
                clickAndHold(driver)
        if i>=7:
            break

def clickAndHold(driver):
    discountCaptcha = driver.find_element_by_xpath('/html/body/ef-root/ef-store/ef-api-challenge/div/div/div/div[2]/div/iframe[7]')
    ActionChains(driver).move_to_element(discountCaptcha).click_and_hold(discountCaptcha).perform()
        
def barnesAndNobleScraping(driver,ISBN):
    
    driver.get('https://ilstu.bncollege.com/')

    #Input the ISBN into the search and press enter
    searchBar = driver.find_element_by_xpath("//*[@id='bned_site_search']")
    searchBar.click()
    searchBar.send_keys(ISBN)
    searchBar.submit()

    #Grabs the price to buy new/used, rent new/used, and return date
    buyNew = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH,"/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[1]/div[2]/div[1]/div/label/span[1]")))
    buyUsed = driver.find_element_by_xpath("/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[1]/div[2]/div[2]/div/label/span[1]")
    rentNew = driver.find_element_by_xpath("/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div/label/span[1]")
    rentUsed = driver.find_element_by_xpath("/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[2]/div/label/span[1]")
    rentReturn = driver.find_element_by_xpath("/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[2]/div/span")
    print(buyNew.get_attribute("innerHTML"))
    print(buyUsed.get_attribute("innerHTML"))
    print(rentNew.get_attribute("innerHTML"))
    print(rentUsed.get_attribute("innerHTML"))
    print(rentReturn.get_attribute("innerHTML"))
    return [buyNew.get_attribute("innerHTML"),buyUsed.get_attribute("innerHTML"),rentNew.get_attribute("innerHTML"),rentUsed.get_attribute("innerHTML"),rentReturn.get_attribute("innerHTML")]
    
main()
