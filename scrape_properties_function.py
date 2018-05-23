# -*- coding: utf-8 -*-
"""
Project for Programming: The next step
Data science project to estimate house prices from a Dutch real estate site

Part 2: function to scrape a list of links to properties of pararius.nl


Author: Sjoerd Evelo
Student ID: 10370862
Universiteit van Amsterdam

function usage: 
function takes the following input:
- name of the textfile with a list of links that is located in the working directory.
- path to Chromedriver 
output is a .csv file

"""
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
                elif item == 'Inhoud (m³)':
                    volume = elements[0][i+1].rstrip(' m³')
                elif item == 'Status':
                    listing_status = elements[0][i+1]
                elif item == 'Aangeboden sinds':
                    date_posted = elements[0][i+1]

        for item in my_browser.find_elements_by_id("listing-buy-map"):
            longitude = item.get_attribute('data-lng')
            latitude = item.get_attribute('data-lat')
            
    #might want to add more stuff
            
        property_data.append({"Price": price,
                              "Zipcode": zipcode,
                              "Surface (m²)": surface,
                              "Number of rooms": n_rooms,
                              "Neighbourhood": neighbourhood,
                              "Year built": year_built,
                              "Total volume": volume,
                              "Listing_status": listing_status,
                              "Available since": date_posted,
                              "Coordinates": (longitude,latitude)
                              })
    
        time.sleep(randint(5, 10))
    
    property_data_frame = pd.DataFrame(property_data)
    
    property_data_frame.to_csv(csv_filename+'.csv', sep = ";")
    
    
    
    
    