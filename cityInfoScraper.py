import pyodbc 
import re 
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#connect to database. get list of cities with state
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-I4MHHC3\SQLEXPRESS;'
                      'Database=firstDatabase;'
                      'Trusted_Connection=yes;')

dbCities = conn.cursor()
dbCities.execute('SELECT [City],[State] FROM [firstDatabase].[dbo].[Cities]')

#Getting Chrome webdrivers and website
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(executable_path="C:\webdrivers\chromedriver.exe", options=options)
driver.get("https://www.city-data.com/")

#Getting 'Counties.txt' file and making it writable
countiesTxt = open("txtFiles/Counties.txt", "w")

for row in dbCities:
    time.sleep(3)
    stateName = row[0] + ", " + row[1]
    #search for city, state
    try:
        driver.find_element_by_id('intelligent_search').send_keys(stateName + "\n")
    except:
        driver.find_element_by_id('menu_search').send_keys(stateName + "\n")
    #if not immediately on page, choose first result
    try:
        driver.find_element_by_xpath("//*[@id='___gcse_0']/div/div/div/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/div/a").send_keys("\n")
    except:
        pass
    
    #On City page
    #Get Population (commented out because I already have the info)
    '''
    cityPop = driver.find_element_by_id("city-population").text 
    cityPop = cityPop.replace("\n", " ").replace(",", "") 
    cityPop = cityPop.replace("Population in 2019: ", ",").replace(" (100% urban 0% rural). Population change since 2000: ", ", ")
    print(cityPop)
    '''

    #Median and per capita income, median come value
    multInfo = driver.find_element_by_id("median-income").text 
    multInfo = multInfo.replace(",", "") 
    medIncSplitter = multInfo.split("\n")
    del medIncSplitter[1:6]
    del medIncSplitter[2:5]
    del medIncSplitter[3:]

    #Median Household Income
    medInc = medIncSplitter[0]
    medInc = medInc.replace("Estimated median household income in 2019: ", ",").replace(" (it was ", ",").replace(" in 2000)","")
    
    #Per Capita Income
    pcapInc = medIncSplitter[1]
    pcapInc = pcapInc.replace("Estimated per capita income in 2019: ", ",").replace(" (it was ", ",").replace(" in 2000)","")
    
    #Median House Value
    medHValue = medIncSplitter[2]
    medHValue = medHValue.replace("Estimated median house or condo value in 2019: ", ",").replace(" (it was ", ",").replace(" in 2000)","")
    
    #Poverty Levels
    poverty = driver.find_element_by_id("poverty-level").text 
    poverty = poverty.replace(",", "") 
    povertySplitter = poverty.split("\n") 
    del povertySplitter[1:]
    poverty = povertySplitter[0]
    poverty = poverty.replace("Percentage of residents living in poverty in 2019: ", ",")

    #Crime Rates
    crime = driver.find_element_by_id("crime").text
    






    

    


