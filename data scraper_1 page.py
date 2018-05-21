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

for item in my_browser.find_elements_by_class_name('details-container'):
    elements.append(item.text.split('\n'))
    #print(elements)
    for i, item in enumerate(elements[0]):
        if item == 'Buurt':
            neighbourhood = elements[0][i+1]
            #print(neighbourhood)
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

mapstuff = []
x = my_browser.find_element_by_class_name("mapboxgl-map")
mapstuff.append(x.text)
print(mapstuff)
    
data.append({"Price": price,
             "Zipcode": zipcode,
             "Surface (m²)": surface,
             "Number of rooms": n_rooms,
             "Neighbourhood": neighbourhood,
             "Year built": year_built
             })
df = pd.DataFrame(data)
#print(df)

#%%
#//*[@id="listing-buy-map"]
#listing-buy-map
#<div id="listing-buy-map" class="buy-map buy-map--listing mapboxgl-map" data-lng="5.0111489800" data-lat="52.3476560500" data-listing="{&quot;type&quot;:&quot;FeatureCollection&quot;,&quot;features&quot;:[{&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[5.01114898,52.34765605]}}]}" data-education="{&quot;type&quot;:&quot;FeatureCollection&quot;,&quot;features&quot;:[{&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[5.00795851558318,52.3500882131917]},&quot;properties&quot;:{&quot;id&quot;:&quot;eb3f103e-3fb4-54e6-8fc4-4826a4154f2f&quot;,&quot;name&quot;:&quot;Laterna Magica&quot;,&quot;type&quot;:&quot;elementary&quot;,&quot;distance&quot;:347.15076389}},{&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[5.00433549296976,52.3512956677976]},&quot;properties&quot;:{&quot;id&quot;:&quot;f7214e22-6817-5512-96d2-433c7d6319ce&quot;,&quot;name&quot;:&quot;IJburg College voor Vwo Havo Mavo en Vbo&quot;,&quot;type&quot;:&quot;secondary&quot;,&quot;distance&quot;:616.10574127}}]}" data-supermarkets="{&quot;type&quot;:&quot;FeatureCollection&quot;,&quot;features&quot;:[{&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[5.0076370001308,52.351704000366]},&quot;properties&quot;:{&quot;id&quot;:&quot;0484f3cd-aa5f-5975-ba18-eee50784b6cc&quot;,&quot;name&quot;:&quot;Buurtsuper&quot;,&quot;distance&quot;:510.06322013}},{&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[5.0070089996926,52.352149999758]},&quot;properties&quot;:{&quot;id&quot;:&quot;7d89f937-8620-525e-91e7-4324c0a94e45&quot;,&quot;name&quot;:&quot;Buurtsuper&quot;,&quot;distance&quot;:574.15020205}},{&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[5.0210100943998,52.334844360372]},&quot;properties&quot;:{&quot;id&quot;:&quot;64d0d37b-36fe-5305-855a-c531decd3282&quot;,&quot;name&quot;:&quot;Lidl&quot;,&quot;distance&quot;:1576.07918909}},{&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[5.0222113693677,52.334989410337]},&quot;properties&quot;:{&quot;id&quot;:&quot;2b5ea742-96e5-54ba-96df-173a153737ee&quot;,&quot;name&quot;:&quot;AH XL&quot;,&quot;distance&quot;:1598.44225031}}]}" data-tram="{&quot;type&quot;:&quot;FeatureCollection&quot;,&quot;features&quot;:[{&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[5.004324,52.350954]},&quot;properties&quot;:{&quot;id&quot;:&quot;b43aa9d6-ce51-594c-b4eb-135b653aecce&quot;,&quot;name&quot;:&quot;Amsterdam, IJburg&quot;,&quot;types&quot;:[&quot;tram&quot;],&quot;lines&quot;:&quot;26&quot;,&quot;agencies&quot;:&quot;GVB&quot;,&quot;distance&quot;:592.42382873}}]}" data-bus="{&quot;type&quot;:&quot;FeatureCollection&quot;,&quot;features&quot;:[{&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[5.014059,52.3486845]},&quot;properties&quot;:{&quot;id&quot;:&quot;d84ab07f-8181-5e2f-b6c7-d7b5fbde204f&quot;,&quot;name&quot;:&quot;Amsterdam, Peter Martensstraat&quot;,&quot;types&quot;:[&quot;bus&quot;],&quot;lines&quot;:&quot;66&quot;,&quot;agencies&quot;:&quot;GVB&quot;,&quot;distance&quot;:228.95447338}}]}" data-subway="{&quot;type&quot;:&quot;FeatureCollection&quot;,&quot;features&quot;:[{&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[4.9667415,52.328627]},&quot;properties&quot;:{&quot;id&quot;:&quot;6307e16c-8741-55c7-af15-d0e329278cb2&quot;,&quot;name&quot;:&quot;Amsterdam, Verrijn Stuartweg&quot;,&quot;types&quot;:[&quot;subway&quot;],&quot;lines&quot;:&quot;53&quot;,&quot;agencies&quot;:&quot;GVB&quot;,&quot;distance&quot;:3693.90565789}}]}" data-train="{&quot;type&quot;:&quot;FeatureCollection&quot;,&quot;features&quot;:[{&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[4.96679663658,52.3454763561]},&quot;properties&quot;:{&quot;id&quot;:&quot;1b3fc00c-5d26-564e-9132-d86ab2e7fe8e&quot;,&quot;name&quot;:&quot;Diemen&quot;,&quot;types&quot;:[&quot;train&quot;],&quot;lines&quot;:&quot;Sprinter&quot;,&quot;agencies&quot;:&quot;NS&quot;,&quot;distance&quot;:3032.16944835}}]}" data-daycares="{&quot;type&quot;:&quot;FeatureCollection&quot;,&quot;features&quot;:[{&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[5.01017293133368,52.346595866207]},&quot;properties&quot;:{&quot;id&quot;:&quot;35f7d8d5-67f5-5231-a592-5fa359369869&quot;,&quot;name&quot;:&quot;KinderVilla IJburg Haveneiland B.V.&quot;,&quot;type&quot;:&quot;kdv&quot;,&quot;distance&quot;:135.42530016}}]}">
 #   <script src="https://api.tiles.mapbox.com/mapbox-gl-js/v0.44.1/mapbox-gl.js"></script>
 #   <link href="https://api.tiles.mapbox.com/mapbox-gl-js/v0.44.1/mapbox-gl.css" rel="stylesheet">
#<div class="loading-indicator loading-indicator--hide"><svg class="loading-indicator__container" viewBox="25 25 50 50"><circle class="loading-indicator__path" cx="50" cy="50" r="20" fill="none" stroke-width="3" stroke-miterlimit="10"></circle></svg></div><div class="mapboxgl-missing-css">Missing Mapbox GL JS CSS</div><div class="mapboxgl-canvas-container mapboxgl-interactive mapboxgl-touch-drag-pan mapboxgl-touch-zoom-rotate"><canvas class="mapboxgl-canvas" tabindex="0" aria-label="Map" style="position: absolute; width: 660px; height: 300px;" width="660" height="300"></canvas></div><div class="mapboxgl-control-container"><div class="mapboxgl-ctrl-top-left"></div><div class="mapboxgl-ctrl-top-right"></div><div class="mapboxgl-ctrl-bottom-left"><div class="mapboxgl-ctrl" style="display: block;"><a class="mapboxgl-ctrl-logo" target="_blank" href="https://www.mapbox.com/" aria-label="Mapbox logo"></a></div></div><div class="mapboxgl-ctrl-bottom-right"><div class="mapboxgl-ctrl mapboxgl-ctrl-group"><button class="mapboxgl-ctrl-icon mapboxgl-ctrl-zoom-in" type="button" aria-label="Zoom In"></button><button class="mapboxgl-ctrl-icon mapboxgl-ctrl-zoom-out" type="button" aria-label="Zoom Out"></button><button class="mapboxgl-ctrl-icon mapboxgl-ctrl-compass" type="button" aria-label="Reset North"><span class="mapboxgl-ctrl-compass-arrow" style="transform: rotate(0deg);"></span></button></div><div class="mapboxgl-ctrl mapboxgl-ctrl-attrib"><a href="https://www.mapbox.com/about/maps/" target="_blank">© Mapbox</a> <a href="http://www.openstreetmap.org/about/" target="_blank">© OpenStreetMap</a> <a class="mapbox-improve-map" href="https://www.mapbox.com/feedback/?owner=treehouse&amp;id=cj8k2ud9t4m3x2ro3ok73r47v&amp;access_token=pk.eyJ1IjoidHJlZWhvdXNlIiwiYSI6ImNqOGsxcTEwajA3MDgyd28zOWd5dXJ0YXcifQ.0PYYxJ09bTgq60eTB2Br0Q" target="_blank">Improve this map</a></div></div></div></div>
#details > dl:nth-child(2)
#try:
#    WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id="content"]/div/section[2]/div[1]/div[1]")))