# -*- coding: utf-8 -*-
#%%
"""
Project for Programming: The next step
Data science project to estimate house prices from a Dutch real estate site

Part 2: function to scrape a list of links to properties of pararius.nl


Author: Sjoerd Evelo
Student ID: 10370862
Universiteit van Amsterdam

Function usage: 
Function takes the following input:
- String: Name of the textfile with a list of links that is located in the working directory, include '.txt'.
- String: Path to Chromedriver, make sure to type r'path' for unicode interpretation
- String: The name for the output file, '.csv' will be added by the function

Output is a .csv file

"""

#%%
#import packages
from selenium import webdriver 

import pandas as pd
import time
from random import randint


def scrape_properties(file, webdriver_path, csv_filename ):
    
    list_of_links = open(file, "r")
    list_of_links = list_of_links.readlines()
    
    #create variable
    property_data = []
    print('opening browser')
    #initialize webdriver
    my_browser = webdriver.Chrome(executable_path= webdriver_path) 

    print('extracting information...')
    #loop over properties
    for link in list_of_links:
    
        my_browser.get(str(link))
        #create/set defeault for some variables
        elements = []
        garden = []
        garden.append('No')
        n_bedrooms = []
        year_built = []
        #loop and store all information in a list
        for item in my_browser.find_elements_by_class_name('details-container'):
            elements.append(item.text.split('\n'))
            #get specific item out of the list, clean some data
            for i, item in enumerate(elements[0]):
                if item == 'Buurt':
                    neighbourhood = elements[0][i+1]
                elif item == 'Type woning':
                    house_type = elements[0][i+1]
                elif item == 'Straat':
                    street = elements[0][i+1]
                elif item == 'Postcode':
                    zipcode = elements[0][i+1].replace(' ', '')
                elif item == 'Vraagprijs':
                    price = int(elements[0][i+1].replace('.','').lstrip('€ ').rstrip(',-'))
                elif item == 'Aantal kamers':
                    n_rooms = int(elements[0][i+1])
                elif item == 'Aantal slaapkamers':
                    n_bedrooms = int(elements[0][i+1])
                elif item == 'Oppervlakte (m²)':
                    surface = int(elements[0][i+1].rstrip(' m²'))
                elif item == 'Bouwjaar':
                    year_built = int(elements[0][i+1])
                elif item == 'Inhoud (m³)':
                    volume = int(elements[0][i+1].replace('.','').rstrip(' m³'))
                elif item == 'Status':
                    listing_status = elements[0][i+1]
                elif item == 'Aangeboden sinds':
                    date_posted = elements[0][i+1]
                elif item == 'Tuin aanwezig':
                    garden = []
                    if elements[0][i+1] == 'Ja':
                        garden.append('Yes')
                elif item == 'Tuininformatie':
                    garden.append(elements[0][i+1])
                        
        #finding coordinates
        for item in my_browser.find_elements_by_id('listing-map'):
                longitude = float(item.get_attribute('data-lng'))
                latitude = float(item.get_attribute('data-lat'))
                    
        #might want to add more stuff
                
        property_data.append({"Link": my_browser.current_url,
                              "Street": street,
                              "Price": price,
                              "Zipcode": zipcode,
                              "Type": house_type,
                              "Surface (m²)": surface,
                              "Number of rooms": n_rooms,
                              "Number of bedrooms": n_bedrooms,
                              "Neighbourhood": neighbourhood,
                              "Year built": year_built,
                              "Total volume (m³)": volume,
                              "Listing_status": listing_status,
                              "Available since": date_posted,
                              "Longitude": longitude,
                              "Latitude": latitude,
                              "Garden": garden
                              })
                    
        time.sleep(randint(5, 10))

    
    my_browser.close()
    
    #create data frame from dictionairy and save file in working directory 
    property_data_frame = pd.DataFrame(property_data)
    #maybe insert a line to delete duplicates here
    property_data_frame.to_csv(csv_filename+'.csv', sep = ";")
    
    print('Done!')
    print('File saved as '+ csv_filename+'.csv with information of ' + str(len(property_data_frame["Link"])) + ' properties')
    
    

#%%    

scrape_properties('pararius_links_new.txt', r'C:\Users\droes\.spyder-py3\chromedriver', 'property_small_database')   
    
#%%
data_frame = pd.read_csv(r'property_small_database.csv', sep = ";")


