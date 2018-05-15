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
#Save the extracted links to a file
linksfile = open('pararius_links.txt', 'w')
for item in list_of_links:
    print(item)
    linksfile.write("%s\n" % item)