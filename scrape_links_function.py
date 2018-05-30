#%%
"""
Project for Programming: The next step
Data science project to estimate house prices from a Dutch real estate site

Author: Sjoerd Evelo
ID: 10370862
Universiteit van Amsterdam

This script contains a function that can be ran to loads all the links for the search results on pararius,
and saves them to a file in the current working directory that can be used by the data_scraper_all function.

IMPORTANT: 
the function takes several inputs:
- string: filepath to your webdriver: chromedriver is default
- string: location of the properties (a city, like 'amsterdam') - No capitals!
- tuple: range of the pages you want to scrape: (firstpage,lastpage). Can't start at 0!
- string: name of the textfile where the links are saved: should end with .txt!


An example of the function usage is:
scrape_links('C:\Users\chromedriver','amsterdam',(1,60), 'amsterdam_properties.txt')

MORE IMPORTANT:
- To run this script, you need to have the selenium package installed for python.
- You need chromedriver in a path you can find.

MOST IMPORTANT
- Parasius will probably recognize you try to acces the site with a headless browser and confront you with a Captcha.
You have 2 minutes to solve this captcha, if you take longer te function will time out, but you can start again from a new ' firstpage' 
- Sometimes pararius will completely shut you out. you can try to manually navigate to the next page by copying the link in the headless browser and the function will continue,
or shut down the browser and start again from the next page as the new (firstpage)
- IF you start again, make sure to save the links to another textfile, function overwrites old files!

"""

#%%

#importing needed packages
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
from random import randint

#initialize function
def scrape_links(driver_filepath, location, pagerange, textfile_name):
    
    #create parameters
    list_of_links = []
    firstpage = abs(pagerange[0])
    lastpage = abs(pagerange[1])+1
    #make sure range does not start at 0
    try:
        firstpage != 0
    except:
        print("pagerange can't start at zero!")
    
    #initialize browser
    my_browser = webdriver.Chrome(executable_path= driver_filepath)
    
    #set maximum timeout duration <-- change this if you need longer to solve Capthca's
    wait = WebDriverWait(my_browser, 120)
    
    #open page, wait 2 minutes or until page is loaded, save all links in a list
    print('extracting links...')
    for i in range(firstpage,lastpage):
        if i == 1:
            my_browser.get("https://www.pararius.nl/koopwoningen/"+location)
        else:
            my_browser.get("https://www.pararius.nl/koopwoningen/"+location+"/page-"+str(i))
        
        try: 
            wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="search-page"]/div/div/ul[2]/li[7]')))
            for item in my_browser.find_elements_by_class_name('details'):
                link = item.find_element_by_css_selector('a').get_attribute('href')
                list_of_links.append(link)
            #keep track what page is extracted, wait a little bit until the next page is opened 
            if i == lastpage:
                print('page ' +str(i) + ' extracted, closing browser')
            else:
                print('page '+ str(i) + ' extracted, opening next page')
            time.sleep(randint(10, 15))
        except (TimeoutException, NoSuchElementException) as e:
            print(e)
    
    my_browser.close()
    
    #Delete duplicate links
    list_of_links = list(set(list_of_links))
    print('gathered a total of '+ str(len(list_of_links))+' links to properties')
    
    #save links to file
    print('saving file...')
    
    textfile = open(textfile_name, 'w')
    for item in list_of_links:
        textfile.write("%s\n" % item)
    
    print('file saved to current working directory')
    
    print('done!')
    
#%%
'''Cell that runs the function'''  
scrape_links(r'C:\Users\droes\.spyder-py3\chromedriver', 'amsterdam', (1,1), 'pararius_links_new.txt')

