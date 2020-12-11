{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 64,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: selenium in c:\\users\\mbannon\\anaconda3\\lib\\site-packages (3.141.0)\n",
      "Requirement already satisfied: urllib3 in c:\\users\\mbannon\\anaconda3\\lib\\site-packages (from selenium) (1.25.9)\n",
      "Requirement already satisfied: splinter in c:\\users\\mbannon\\anaconda3\\lib\\site-packages (0.14.0)\n",
      "Requirement already satisfied: six in c:\\users\\mbannon\\anaconda3\\lib\\site-packages (from splinter) (1.15.0)\n",
      "Requirement already satisfied: selenium>=3.141.0 in c:\\users\\mbannon\\anaconda3\\lib\\site-packages (from splinter) (3.141.0)\n",
      "Requirement already satisfied: urllib3 in c:\\users\\mbannon\\anaconda3\\lib\\site-packages (from selenium>=3.141.0->splinter) (1.25.9)\n"
     ]
    }
   ],
   "source": [
    "# Imports\n",
    "import pymongo\n",
    "import pandas as pd\n",
    "from bs4 import BeautifulSoup\n",
    "import urllib.request\n",
    "from IPython.display import HTML\n",
    "import re\n",
    "import requests\n",
    "import json\n",
    "!pip install selenium\n",
    "!pip install splinter\n",
    "from splinter import Browser"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Step 1 - Scraping"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 65,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Choose the executable path to the chrome driver \n",
    "executable_path = {\"executable_path\": \"/Users/mbannon/Downloads/chromedriver.exe\"}\n",
    "browser = Browser(\"chrome\", **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "NASA Mars News\n",
    "Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 68,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Go to NASA news url\n",
    "nasa_url = 'https://mars.nasa.gov/news/'\n",
    "browser.visit(nasa_url)\n",
    "\n",
    "#create html object\n",
    "html = browser.html\n",
    "\n",
    "#parse HTML w/ BeautifulSoup\n",
    "soup = BeautifulSoup(html, \"html.parser\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 69,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "5 Hidden Gems Are Riding Aboard NASA's Perseverance Rover\n",
      "The symbols, mottos, and small objects added to the agency's newest Mars rover serve a variety of purposes, from functional to decorative.\n"
     ]
    }
   ],
   "source": [
    "# Get the latest element that contains news title and news_paragraph\n",
    "article = soup.find(\"div\", class_='list_text')\n",
    "news_title = article.find(\"div\", class_ =\"content_title\").text\n",
    "news_p = article.find(\"div\", class_ =\"article_teaser_body\").text\n",
    "\n",
    "#display scraped data\n",
    "print(news_title)\n",
    "print(news_p)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "JPL Mars Space Images - Featured Image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 70,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA19334-1920x1200.jpg'"
      ]
     },
     "execution_count": 70,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# visit the url for JPL Featured space image\n",
    "image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "browser.visit(image_url_featured)\n",
    "\n",
    "#create html object\n",
    "html_image = browser.html\n",
    "\n",
    "#parse HTML w/ BeautifulSoup\n",
    "soup = BeautifulSoup(html_image, 'html.parser')\n",
    "\n",
    "# Retrieve background-image url from style tag \n",
    "featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]\n",
    "\n",
    "# Website Url \n",
    "main_url = 'https://www.jpl.nasa.gov'\n",
    "\n",
    "# Concatenate website url with scrapped route\n",
    "featured_image_url = main_url + featured_image_url\n",
    "\n",
    "# Display full link to featured image\n",
    "featured_image_url"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Mars Facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 71,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<table border=\"1\" class=\"dataframe\">\n",
      "  <tbody>\n",
      "    <tr>\n",
      "      <td>Equatorial Diameter:</td>\n",
      "      <td>6,792 km</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <td>Polar Diameter:</td>\n",
      "      <td>6,752 km</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <td>Mass:</td>\n",
      "      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <td>Moons:</td>\n",
      "      <td>2 (Phobos &amp; Deimos)</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <td>Orbit Distance:</td>\n",
      "      <td>227,943,824 km (1.38 AU)</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <td>Orbit Period:</td>\n",
      "      <td>687 days (1.9 years)</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <td>Surface Temperature:</td>\n",
      "      <td>-87 to -5 °C</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <td>First Record:</td>\n",
      "      <td>2nd millennium BC</td>\n",
      "    </tr>\n",
      "    <tr>\n",
      "      <td>Recorded By:</td>\n",
      "      <td>Egyptian astronomers</td>\n",
      "    </tr>\n",
      "  </tbody>\n",
      "</table>\n"
     ]
    }
   ],
   "source": [
    "#visit url for the Mars Facts webpage\n",
    "facts_pg = \"https://space-facts.com/mars/\"\n",
    "browser.visit(facts_pg)\n",
    "\n",
    "mars_data = pd.read_html(facts_pg)\n",
    "mars_data = pd.DataFrame(mars_data[0])\n",
    "mars_facts = mars_data.to_html(header = False, index = False)\n",
    "print(mars_facts)"
   ]
  },
  {
   "attachments": {},
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Mars Hemispheres!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 72,
   "metadata": {},
   "outputs": [],
   "source": [
    "import time \n",
    "hemispheres_url = \"https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars\"\n",
    "browser.visit(hemispheres_url)\n",
    "html = browser.html\n",
    "soup = BeautifulSoup(html, \"html.parser\")\n",
    "mars_hemisphere = []\n",
    "\n",
    "products = soup.find(\"div\", class_ = \"result-list\" )\n",
    "hemispheres = products.find_all(\"div\", class_=\"item\")\n",
    "\n",
    "for hemisphere in hemispheres:\n",
    "    title = hemisphere.find(\"h3\").text\n",
    "    title = title.replace(\"Enhanced\", \"\")\n",
    "    end_link = hemisphere.find(\"a\")[\"href\"]\n",
    "    image_link = \"https://astrogeology.usgs.gov/\" + end_link    \n",
    "    browser.visit(image_link)\n",
    "    html = browser.html\n",
    "    soup=BeautifulSoup(html, \"html.parser\")\n",
    "    downloads = soup.find(\"div\", class_=\"downloads\")\n",
    "    image_url = downloads.find(\"a\")[\"href\"]\n",
    "    mars_hemisphere.append({\"title\": title, \"img_url\": image_url})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 73,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[{'title': 'Cerberus Hemisphere ',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},\n",
       " {'title': 'Schiaparelli Hemisphere ',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},\n",
       " {'title': 'Syrtis Major Hemisphere ',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},\n",
       " {'title': 'Valles Marineris Hemisphere ',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]"
      ]
     },
     "execution_count": 73,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "mars_hemisphere"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%pwd"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
