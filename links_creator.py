# -*- coding: utf-8 -*-
"""

Project for Programming: The next step
Data science project to estimate house prices from a Dutch real estate site

Author: Sjoerd Evelo
ID: 10370862
Universiteit van Amsterdam

This script loads all the links for the search results on pararius,
and stores them in a list that can be used by the data scraper.

"""
#%%

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
from random import randint

#%%
# first page 
#from selenium.webdriver.support import expected_conditions as EC
my_browser = webdriver.Chrome(executable_path=r'C:\Users\S.Evelo\.spyder-py3\PNS project\chromedriver')

my_browser.get("https://www.pararius.nl/koopwoningen/amsterdam")
#This will probably prompt a captha, manually solve that first before running the code cell below

#%%
#extract links from the HTML
list_of_links = []
for item in my_browser.find_elements_by_class_name('details'):
    link = item.find_element_by_css_selector('a').get_attribute('href')
    list_of_links.append(link)
print(list_of_links)
#%%


lastpage = 61
page = 2



my_browser = webdriver.Chrome(executable_path=r'C:\Users\S.Evelo\.spyder-py3\PNS project\chromedriver')
link = "https://www.pararius.nl/koopwoningen/amsterdam/page-"+str(page)
wait = WebDriverWait(my_browser, 100)
my_browser.get(link)
while page <= lastpage:
    
        try:
            if page == 2:
                next_page = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="search-page"]/div/div/ul[2]/li[10]')))
            elif page == 3:
                next_page = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="search-page"]/div/div/ul[2]/li[11]')))
            elif page == 4:
                next_page = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="search-page"]/div/div/ul[2]/li[12]')))
            else:
                next_page = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="search-page"]/div/div/ul[2]/li[13]')))
        
            for item in my_browser.find_elements_by_class_name('details'):
                link = item.find_element_by_css_selector('a').get_attribute('href')
                list_of_links.append(link)
            
            time.sleep(randint(10, 15))
            print('links from page '+str(page)+' extracted, clicking next page')
            page += 1
            next_page.click()
        except ValueError:
            pass
        
            

   


#%%
print
print(list_of_links)
#%%
my_browser = webdriver.Chrome(executable_path=r'C:\Users\S.Evelo\.spyder-py3\PNS project\chromedriver')
wait = WebDriverWait(my_browser, 100)

my_browser.get("https://www.pararius.nl/koopwoningen/amsterdam")

try:
    next_page = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="search-page"]/div/div/ul[2]/li[7]')))
    for item in my_browser.find_elements_by_class_name('details'):
        link = item.find_element_by_css_selector('a').get_attribute('href')
        list_of_links.append(link)
    page += 1
except ValueError:
    pass
my_browser.close()

time.sleep(randint(10, 15))
#%%
#Save the extracted links to a file
linksfile = open('pararius_links.txt', 'w')
for item in list_of_links:
    print(item)
    linksfile.write("%s\n" % item)