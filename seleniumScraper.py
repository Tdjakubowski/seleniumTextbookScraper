from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options 
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
    
    actuallyScraping(driver)




#Attempts to start a Firefox webdriver using Selenium, I did firefox because I don't want to redownload chrome, even though chrome is probably better for this process

def seleniumStartup(webBrowserChoice):
    
    #Allows us to edit the options for the webdriver
    options = Options()
    
    
    for i in range(3):

        #Actually starting the webdriver. Will do 3 attempts then shut down if it fails. If it works, returns the driver
        try:
            #Start a firefox webdriver
            if int(webBrowserChoice) == 1:
                
                #Webdriver will load without GUI
                options.headless = True
                
                driver= webdriver.Firefox(options=options)
                
                print("Driver loaded.")
                return driver
            
            #Start a chrome webdriver
            else:
                #some command goes here to make the webdriver headless on chrome
                
                
                
                driver = webdriver.Chrome(options=options)
                print("Driver loaded.")
                return driver
        #Prevents the program from crashing, and tries again
        except WebDriverException:
            print("Driver Failed. Attempt #"+str(i+1)+"/3")
    #exits program after 3rd failed load        
    if i == 2:
        print("Webdriver Load Failed. Shutting Down.")
        exit()
        
    

def actuallyScraping(driver):
    #Grabbing the entire webpage
    #I broke it up because my IDE cant scroll horizontally, and trying to transport imports to a different IDE is irritating :/
    driver.get("https://www.google.com/search?q=Information+Technology+Project+Management:+Providing+Measurable+"+
               "Organizational+Value,+5th+Edition++Jack+T.+Marchewka&source=lmns&tbm=shop&bih=750&biw=1536&client=firefox-b-1-d&hl=en&sa=X&ved="+
               "2ahUKEwjCgqf8gMvzAhUYU80KHQcFCe0Q_AUoAnoECAEQAg")
    
    #Searching the html for elements named mR2gOd, which contains all of the books in the ad section, but also has a lot of other stuff we dont need
    largerClass = driver.find_elements_by_class_name("mR2gOd")
    
    #Prints out each element in largerClass
    for element in largerClass:
        print(element.get_attribute("innerHTML")+'\n')
        
    #wait 3 seconds, allows everything else to load
    #time.sleep(3)
    
    #Searches the html for elements named GhTN2e, which is more specific, but for some unknown reason only pulls 2 books. Why? IDK

    #Looking closer at the html pulled, it has all 4, but they're grouped in 2. Soooooooo it technically works :)
    closerClass = driver.find_elements_by_xpath("//div[@class='GhTN2e']")
    print(len(closerClass))

    #Prints out each element in closerClass
    for element in closerClass:
        print(element.get_attribute("innerHTML")+'\n')
        
    #Self explanitory
    driver.quit()
main()
