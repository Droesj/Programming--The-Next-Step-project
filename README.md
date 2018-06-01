# Programming: The Next Step

## Property data extraction and Analysis

## Author: Sjoerd Evelo
## Student ID: 10370862
---

_**This project is currently under construction**_

---
### Introduction
The goal fo this project was to gather data of a large number of properties listed on the housing site [Pararius.nl](https://www.pararius.nl), store them in a database and use that to visualize the data, and predict housing prices according to certain features. All of this information is displayed in a Dashboard app by [Plotly Dash](https://plot.ly/products/dash/). 

To view the app simply launch app.py and go to the specified webpage

**Important**: To use this application you need to have dash installed in your computer, use the following lines in your .cmd:

    pip install dash==0.21.1  # The core dash backend
    pip install dash-renderer==0.12.1  # The dash front-end
    pip install dash-html-components==0.10.1  # HTML components
    pip install dash-core-components==0.21.0rc1  # Supercharged components 
    pip install plotly --upgrade  # Plotly graphing library used in examples

Note: the dash-core-components is not the latest version because the dcc.Tabs component that i use is still in development and is not integrated yet in the full package see [the github PR](https://github.com/plotly/dash-core-components/pull/74)

Furthermore, to use the scrapers you will need to install selenium webdriver:

    pip install selenium

Also you need to have chromedriver installed: and be able to navigate to it
http://chromedriver.chromium.org/

**Disclaimer**: the predictor and certain data visualization objects do not work correctly yet, work in progress.


---
### .py functions 

#### Scrape_links_function

This function collects all the links to properties from a specified city, suchs a amsterdam. (Note: the dashboard currently only works for the Amsterdam database (property_databas_final.csv)). Therefore it uses a selenium headless browser which opens automatically and reads certain information for the page it opens. Make sure to have the required packages and files installed as described above. The Browser is closed at the end of the function, do **NOT** close this browser while the function runs. Output is a .txt file which will be used by the `scrape_properties_function.py` function


**Design**
Specify parameters --> loop for every page(open webpage --> wait for page to load (2 minutes to solve captcha) --> Find links and HTML --> append to list) --> close browser --> delete duplicates --> save file

**Function Usage:**
To use te function, open it in your python environment (for instance: Spyder) (might add a runfile if i have time)and give the following inputs: 
* string: filepath to Chromedriver (add 'r' for unicode readability before the filepath and include '\Chromedriver')
* string: location of the properties (a city, like 'amsterdam') - No capitals!
* tuple: range of the pages you want to scrape: (firstpage,lastpage). - Can't start at 0!
* string: name of the textfile where the links are saved. - should end with .txt!

**Important:** 
* Because pararius does not like your scraping their site, it will likely prompt you with a captcha for the first page, and might do so later. If so: you'll have 2 minutes to complete the captcha.
* In some rare cases you will be completely denied access to the page, in that case, wait for a few seconds for the next page to load. the function will automatically delete duplicate links (if the page does not load the last page is stored again in the first place)
* function overwrites files, so be sure to specify the filename for each new use of the function.
---
#### Scrape_properties_function

Similar to the `scrape_links_function` this application is used in a python environment and also opens a headless browser to scrape information from pages. Unlike the first function, accessing these pages should not result in a chaptcha or block by pararius.nl, so there are no exceptions and the function will not wait until a catpcha is solved.

The functions gathers the following information from each property:

* Link
* Streetname
* Listing Price
* Zipcode
* Property Type
* Surface in m²
* Total volume in m³
* Number of rooms
* Number of bedrooms
* Garden
* Neighbourhood
* Year built
* Listing_status
* Date posted online
* Coordinates(Longitude,Latitude)
                              
Output is a .csv file which in turn can be used for the dashboard app.

**Design**
open textfile --> specify parameters --> open browser --> loop for each page (
find all the elements --> store in a list --> 
loop over elements(specify the elements i want to extract --> clean a little while we're at it ) 
--> loop over mapobject (find and extract coordinates) --> store elements in dictionairy) --> wait a little bit) --> close browser --> convert dictionairy to dataframe --> save as .csv 
**Function usage:**

The function takes the following inputs:
* String: Name of the textfile with a list of links that is located in the working directory, include '.txt'.
* String: Path to Chromedriver, make sure to type r'path' for unicode interpretation.
* String: The name for the output file, '.csv' will be added by the function.
---
#### app.py
This function contains the dashboard app. To run, simply launch with python. The server should restart, and after a short load you'll be able to access the app by navigating to the specified webadress in your browser.

**Design**
The Dash app uses a relatively easy way to design: first a layout is specified with all the elements, and those elements can be filled in later using callbacks. The interesting thing about these callbacks is that they can update and interact with eachother. 

Because i use tabs that dynamically display the main content (and as mentioned that this feature is not fullt developed yet) The layout of my dashapp is limited. As a result, the first callback that dynamically provides the output for the main content is rather extensive, and most later callbacks link to an element in this big function. 

For a better understanding, take a look at the code! (a flowchart is pretty much impossible)

 
 




