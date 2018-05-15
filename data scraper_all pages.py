# -*- coding: utf-8 -*-
#%%
"""

Project for Programming: The next step
Data science project to estimate house prices from a Dutch real estate site
Part 1: Data scraper: all houses


Author: Sjoerd Evelo
Student ID: 10370862
Universiteit van Amsterdam

"""
#%%
"""Importing functions, make sure you have selenium installed before running this script"""

from selenium import webdriver 
#from selenium.webdriver.common.by import By 
#from selenium.webdriver.support.ui import WebDriverWait 
#from selenium.webdriver.support import expected_conditions as EC 
#from selenium.common.exceptions import TimeoutException

import pandas as pd
import time
from random import randint

#%%
''' This code block will contain the settings for the webbrowser'''

#might want to do it in incognito mode? 
#my_option = webdriver.ChromeOptions()
#my_option.add_argument("- incognito")
#my_browser = webdriver.Chrome(executable_path=r'C:\Users\S.Evelo\.spyder-py3\PNS project\chromedriver', 
#                              chrome_options=my_option)

my_browser = webdriver.Chrome(executable_path=r'C:\Users\S.Evelo\.spyder-py3\PNS project\chromedriver')


#%%
'''Code block containing a list of links of the houses i want to get data for
list of links can be generated by a seperate script'''

list_of_links =  open("pararius_links.txt", "r")
list_of_links = list_of_links.readlines()


#%%
''''Test Cell 2.0'''
'''This is (for now an incomplete) cell that will contain the code to loop over all the links in list_of_links and extract '''
#create variable
data = []

#initialize webdriver
my_browser = webdriver.Chrome(executable_path=r'C:\Users\S.Evelo\.spyder-py3\PNS project\chromedriver') 

#loop over properties
for link in list_of_links:
    #open browser
    my_browser.get(str(link))
    elements = []
    for item in my_browser.find_elements_by_class_name('details-container'):
        elements.append(item.text.split('\n'))
        for i, item in enumerate(elements[0]):
            if item == 'Buurt':
                neighbourhood = elements[0][i+1]
            elif item == 'Postcode':
                zipcode = elements[0][i+1].replace(' ', '')
            elif item == 'Vraagprijs':
                price = elements[0][i+1].lstrip('€ ').rstrip(',-')
            elif item == 'Aantal kamers':
                n_rooms = elements[0][i+1]
            elif item == 'Oppervlakte (m²)':
                surface = elements[0][i+1].rstrip(' m²')
            elif item == 'Bouwjaar':
                year_built = elements[0][i+1]
            #might want to add more stuff
    data.append({"Price": price,
                 "Zipcode": zipcode,
                 "Surface (m²)": surface,
                 "Number of rooms": n_rooms,
                 "Neighbourhood": neighbourhood,
                 "Year built": year_built
                 })
    
    time.sleep(randint(5, 10))
df = pd.DataFrame(data)
print(df)
#%%

for i in range(1,3):
    print(i)