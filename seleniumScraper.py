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
    
    barnesAndNobleResults = [] #[buyNew,buyUsed,rentNew,rentUsed,rentReturn] If one of the items is unavailable, it will return None
    barnesAndNobleResults= barnesAndNobleScraping(driver,ISBN)

    googleResults = [[],[]]
    googleResults = googleScraping(driver,ISBN)

    
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
                options.headless = True
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
#Not perfect yet, google tends to give one of 3 instances when pulling up the shopping page, so need to add more exception catchers to filter through all possible pages.
def googleScraping(driver,ISBN):
    driver.get('https://www.google.com/')

    searchBar = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    searchBar.click()
    searchBar.send_keys(ISBN)
    searchBar.submit()
    

    shoppingButton = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH,'/html/body/div[7]/div/div[3]/div/div[1]/div/div[1]/div/div[5]/a')))
    shoppingButton.click()
    results = []
    for i in range(3):
        try:
            cost = WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located((By.XPATH,'/html/body/div[7]/div/div[9]/div[4]/div/div[2]/div[2]/div/div/div[1]/g-scrolling-carousel/div[1]/div/div/div['+str(i+1)+']/a/div[3]/div/div[2]/span/b')))
            website = WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located((By.XPATH,'/html/body/div[7]/div/div[9]/div[4]/div/div[2]/div[2]/div/div/div[1]/g-scrolling-carousel/div[1]/div/div/div['+str(i+1)+']/a/div[3]/div/div[3]/span')))
        except exceptions.TimeoutException:
            cost = WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located((By.XPATH,'/html/body/div[7]/div/div[9]/div[4]/div/div[2]/div[2]/div/div/div[1]/g-scrolling-carousel/div[1]/div/div/div['+str(i+1)+']/a/div[2]/div/div[2]/span/b')))
            website = WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located((By.XPATH,'/html/body/div[7]/div/div[9]/div[4]/div/div[2]/div[2]/div/div/div[1]/g-scrolling-carousel/div[1]/div/div/div['+str(i+1)+']/a/div[3]/div/div[3]/span')))

        URL = 'https://www.google.com/' + (WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located((By.XPATH,'/html/body/div[7]/div/div[9]/div[4]/div/div[2]/div[2]/div/div/div[1]/g-scrolling-carousel/div[1]/div/div/div['+str(i+1)+']/a'))).get_attribute('href'))
        print(URL)
        results.append([cost,website,URL])

    print(results)
def barnesAndNobleScraping(driver,ISBN):
    
    driver.get('https://ilstu.bncollege.com/')

    #Input the ISBN into the search
    searchBar = driver.find_element_by_xpath("//*[@id='bned_site_search']")
    searchBar.click()
    searchBar.send_keys(ISBN)

    #Find the search button and click it
    searchButton = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div/form/div/div/div[1]/button[2]')
    searchButton.click()

    #Grabs the price to buy new/used, rent new/used, and return date
    buyNew = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH,"/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[1]/div[2]/div[1]/div/label/span[1]")))
    buyUsed = driver.find_element_by_xpath("/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[1]/div[2]/div[2]/div/label/span[1]")
    rentNew = driver.find_element_by_xpath("/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div/label/span[1]")
    rentUsed = driver.find_element_by_xpath("/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[2]/div/label/span[1]")
    rentReturn = driver.find_element_by_xpath("/html/body/main/div[3]/div[5]/div/div/div/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[2]/div/span")
    return [buyNew.get_attribute("innerHTML"),buyUsed.get_attribute("innerHTML"),rentNew.get_attribute("innerHTML"),rentUsed.get_attribute("innerHTML"),rentReturn.get_attribute("innerHTML")]
    
    
main()
