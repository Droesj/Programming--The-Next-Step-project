#%%
"""

Project for Programming: The next step
Data science project to estimate house prices from a Dutch real estate site
Part 1: Data scraper


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
'''For now: lets write the code for a single advert'''

data = []

my_browser = webdriver.Chrome(executable_path=r'C:\Users\S.Evelo\.spyder-py3\PNS project\chromedriver')
my_browser.get("https://www.pararius.nl/appartement-te-koop/amsterdam/PB0002375969/albert-cuypstraat")

for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[1]/dd[4]'):
    price = x.text.lstrip('€ ').rstrip(',-')
for x in my_browser.find_elements_by_xpath('//*//*[@id="details"]/dl[1]/dd[3]'):
    zipcode = x.text.replace(' ', '')
for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[1]/dd[6]'):
    n_rooms = x.text
for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[1]/dd[1]'):
    neighbourhood = x.text
#From here it goes wrong    
for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[2]/dd[8]'):
    surface = x.text.rstrip(' m²')
for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[2]/dd[6]'):
    year_built = x.text

data.append({"Price": price,
             "Zipcode": zipcode,
             "Surface (m²)": surface,
             "Number of rooms": n_rooms,
             "Neighbourhood": neighbourhood,
             "Year built": year_built
             })

df = pd.DataFrame(data)
print(df)

#%%
'''test it against a second house'''

my_browser = webdriver.Chrome(executable_path=r'C:\Users\S.Evelo\.spyder-py3\PNS project\chromedriver')
my_browser.get("https://www.pararius.nl/appartement-te-koop/amsterdam/PB0002376055/willemsparkweg")

for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[1]/dd[4]'):
    price = x.text.lstrip('€ ').rstrip(',-')
for x in my_browser.find_elements_by_xpath('//*//*[@id="details"]/dl[1]/dd[3]'):
    zipcode = x.text 
for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[1]/dd[6]'):
    n_rooms = x.text
for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[1]/dd[1]'):
    neighbourhood = x.text
#From here it goes wrong    
for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[2]/dd[8]'):
    surface = x.text
for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[2]/dd[6]'):
    year_built = x.text
data.append({"price": price,
             "zipcode": zipcode,
             "surface (m²)": surface,
             "Number of rooms": n_rooms,
             "neighbourhood": neighbourhood,
             "year built": year_built
             })
df = pd.DataFrame(data)
print(df)

#%%
'''This is (for now an incomplete) cell that will contain the code to loop over all the links in list_of_links and extract '''

my_browser = webdriver.Chrome(executable_path=r'C:\Users\S.Evelo\.spyder-py3\PNS project\chromedriver') 
data = []
for link in list_of_links:
    my_browser.get(str(link))
    for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[1]/dd[4]'):
        price = x.text.lstrip('€ ').rstrip(',-')
    for x in my_browser.find_elements_by_xpath('//*//*[@id="details"]/dl[1]/dd[3]'):
        zipcode = x.text.replace(' ', '')
    for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[1]/dd[6]'):
        n_rooms = x.text
    for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[1]/dd[1]'):
        neighbourhood = x.text
#From here it goes wrong    
    for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[2]/dd[8]'):
        surface = x.text.rstrip(' m²')
    for x in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[2]/dd[6]'):
        year_built = x.text
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
'''Test cell'''    
my_browser = webdriver.Chrome(executable_path=r'C:\Users\S.Evelo\.spyder-py3\PNS project\chromedriver')
my_browser.get("https://www.pararius.nl/appartement-te-koop/amsterdam/PB0002375969/albert-cuypstraat")
my_list = []
for item in my_browser.find_elements_by_xpath('//*[@id="details"]/dl[1]'):
    my_list.append(item.text)
    
print(my_list)

#%%
'''testcell 2.0'''
my_browser = webdriver.Chrome(executable_path=r'C:\Users\S.Evelo\.spyder-py3\PNS project\chromedriver')
my_browser.get("https://www.pararius.nl/appartement-te-koop/amsterdam/PB0002376055/willemsparkweg")
for i in range(1,3):
    for j in range(1,10):  #(might have to change to how far it runs)
        for x in my_browser.find_element_by_xpath('//*[@id="details"]/dl['+str(i)+']/dt['+str(j)+']'):
            element = x.text
            #Maybe make the next part loop trough a predetermined dictionairy?
            if element == 'Buurt':
                for x in my_browser.find_element_by_xpath('//*[@id="details"]/dl['+str(i)+']/dd['+str(j)+']'):
                    neighbourhood = x.text
            elif element == 'Postcode':
                for x in my_browser.find_element_by_xpath('//*[@id="details"]/dl['+str(i)+']/dd['+str(j)+']'):
                    zipcode = x.text.replace(' ', '')
            elif element == 'Vraagprijs':
                for x in my_browser.find_element_by_xpath('//*[@id="details"]/dl['+str(i)+']/dd['+str(j)+']'):
                    price = x.text.lstrip('€ ').rstrip(',-')
            elif element == 'Aantal kamers':
                for x in my_browser.find_element_by_xpath('//*[@id="details"]/dl['+str(i)+']/dd['+str(j)+']'):
                    n_rooms = x.text
            elif element == 'Oppervlakte (m²)':
                for x in my_browser.find_element_by_xpath('//*[@id="details"]/dl['+str(i)+']/dd['+str(j)+']'):
                    surface = x.text
            elif element == 'Bouwjaar':
                for x in my_browser.find_element_by_xpath('//*[@id="details"]/dl['+str(i)+']/dd['+str(j)+']'):
                    year_built = x.text
data.append({"Price": price,
             "Zipcode": zipcode,
             "Surface (m²)": surface,
             "Number of rooms": n_rooms,
             "Neighbourhood": neighbourhood,
             "Year built": year_built
             })
#time.sleep(randint(5, 10))
df = pd.DataFrame(data)
print(df)

#%%
elements = []
my_browser = webdriver.Chrome(executable_path=r'C:\Users\S.Evelo\.spyder-py3\PNS project\chromedriver')
my_browser.get("https://www.pararius.nl/appartement-te-koop/amsterdam/PB0002376055/willemsparkweg")
#%%
data = []
elements = []
print(elements)
for item in my_browser.find_elements_by_class_name('details-container'):
    elements.append(item.text.split('\n'))
    print(elements)
    for i, item in enumerate(elements[0]):
        if item == 'Buurt':
            neighbourhood = elements[0][i+1]
            print(neighbourhood)
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
data.append({"Price": price,
             "Zipcode": zipcode,
             "Surface (m²)": surface,
             "Number of rooms": n_rooms,
             "Neighbourhood": neighbourhood,
             "Year built": year_built
             })
df = pd.DataFrame(data)
print(df)

#details > dl:nth-child(2)
#try:
#    WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id="content"]/div/section[2]/div[1]/div[1]")))