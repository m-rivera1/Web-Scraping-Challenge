
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from selenium import webdriver
import time

def init_browser():
    executable_path = {"executable_path": "C:/Users/mike1/OneDrive/Desktop/WebDriver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
   browser = init_browser()
   
   #NASA Mars News -  Scrape and collect the latest News Title and Paragraph Text
   url = "https://mars.nasa.gov/news/"
    
   # initiate browser visit
   browser.visit(url)

   time.sleep(1)

   # initiate page parser 
   html = browser.html
   soup = bs(html, "html.parser")

   # scrape page for for text and save as variables
   news_title = soup.find('div', class_= 'bottom_gradient').text
   news_p = soup.find('div', class_= 'article_teaser_body').text

   # JPL Mars Space Images - scrape featured Image

   url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

   # initiate browser visit
   browser.visit(url)


   # browser click on the 'full image' button on open page - selenium webdriver needed for this!
   browser.click_link_by_partial_text('FULL IMAGE')

   # browser click on the 'more info' button on open page - selenium webdriver needed for this!
   browser.click_link_by_partial_text('more info')

   # initiate page parser 
   html = browser.html
   soup = bs(html, "html.parser")

   # scrape page for image and save as a variable
   image_url = soup.find('figure', class_='lede').a["href"]
   featured_image_url = f'https://www.jpl.nasa.gov{image_url}'


   # Mars Facts: Use pandas to scrape table from url and convert into HTML table string

   url_2 = 'https://space-facts.com/mars/'

   # pandas scrape of html page assigning data to tables variable
   tables = pd.read_html(url_2)
   tables

   # pull in tables data into a dataframe
   mars_df = tables[0]

   #add column heading to dataframe
   mars_df.columns = ["Description", "Mars"]

   #set the first column as the index
   mars_df.set_index("Description", inplace = True)

   mars_df


   # Mars Hemispheres

   url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

   #establish empty dic for images URLs and titles
   hemisphere_image_urls = []

   # initiate browser visit
   browser.visit(url)

   # initiate page parser 
   html = browser.html
   soup = bs(html, "html.parser")

   # scrape page for the image data
   page_scrape = soup.find('div', class_= "result-list")
   item_search = page_scrape.find_all('div', class_='item')


   for item in item_search:
       title = item.find('h3').text
       item_link = item.find('a')['href']
       hemisphere_link = 'https://astrogeology.usgs.gov/' + item_link
       browser.visit(hemisphere_link)
       html = browser.html
       soup = bs(html, "html.parser")
       download_links = soup.find('div', class_='downloads')
       hemi_image = download_links.find('a')['href']
       hemisphere_image_urls.append({'title': title, 'img_url': hemi_image})


   # Store data in dictionary
   mars_data = {
       "news_title": news_title,
       "news_p": news_p,
       "featured_image_url": featured_image_url,
       "mars_facts": mars_df,
       "hemisphere_image_urls": hemisphere_image_urls}

   #browser close after scraping
   browser.quit()

   # Return results
   return mars_data


    

