#!/usr/bin/env python
# coding: utf-8

# In[64]:


# Imports
import pymongo
import pandas as pd
from bs4 import BeautifulSoup
import re
import json
from splinter import Browser

#Choose the executable path to the chrome driver 
executable_path = {"executable_path": "/Users/mbannon/Downloads/chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

# main function
def scrape_all(browser):
    mars_title, mars_paragraph = mars_news()

    mars_data = {
        title: mars_title,
        paragraph: mars_paragraph,
        image: featured_img
    }


    return mars_data

# NASA Mars News
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later

#Go to NASA news url
def mars_news(browser):
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    #create html object
    html = browser.html

    #parse HTML w/ BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Get the latest element that contains news title and news_paragraph
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_ ="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text

    return news_title, news_p

# JPL Mars Space Images - Featured Image
# visit the url for JPL Featured space image
def featured_img(browser):
    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)

    #create html object
    html_image = browser.html

    #parse HTML w/ BeautifulSoup
    soup = BeautifulSoup(html_image, 'html.parser')

    # Retrieve background-image url from style tag 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    featured_image_url = main_url + featured_image_url

    # Display full link to featured image
    return featured_image_url


#visit url for the Mars Facts webpage
def mars_facts():
    facts_pg = "https://space-facts.com/mars/"
    browser.visit(facts_pg)

    mars_data = pd.read_html(facts_pg)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)
    return mars_facts

def hemi(browser):
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})

    return mars_hemisphere
