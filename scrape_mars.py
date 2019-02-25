from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd


def scrape():
    ## MARS NEWS
    ##--------------------------------------------------------------- 
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser.visit(url)
    html = browser.html

    soup = bs(html, 'html.parser')
    results = soup.find_all('div', class_="image_and_description_container")
    ##---------------------------------------------------------------
    news_title = results[0].find('div', class_="content_title").text
    news_p = results[0].find('div', class_="article_teaser_body").text
    ##---------------------------------------------------------------

    ## JPL FEATURED IMAGE
    ##---------------------------------------------------------------
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)
    html = browser.html

    soup = bs(html, 'html.parser')
    results = soup.find_all('li', class_="slide")
    ##---------------------------------------------------------------
    img_url = results[0].find('a')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + img_url
    ##---------------------------------------------------------------

    ## MARS FACTS
    ##---------------------------------------------------------------
    url = 'https://space-facts.com/mars/'
    ##---------------------------------------------------------------
    # tables = pd.read_html(url)
    # tables[0]
    ##---------------------------------------------------------------

    ## MARS WEATHER
    ##---------------------------------------------------------------
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(url)
    html = browser.html

    soup = bs(html, 'html.parser')
    results = soup.find_all('li', class_="js-stream-item")
    ##---------------------------------------------------------------
    mars_weather_unclean = results[0].find('p', class_="TweetTextSize").text.replace('\n',' ')
        #get rid of picture link if there is one
    sep = 'pic.twitter.com'
    mars_weather = mars_weather_unclean.split(sep, 1)[0]
    ##---------------------------------------------------------------
    
    ## MARS HEMISPHERES
    ##---------------------------------------------------------------
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    html = browser.html

    soup = bs(html, 'html.parser')
    results = soup.find_all('div', class_="item")
    ##---------------------------------------------------------------
    hemisphere_image_urls = []

    for result in results:
        # Splinter can capture a page's underlying html and use pass it to BeautifulSoup to allow us to scrape the content
        html = browser.html
        soup = bs(html, 'html.parser')
        # Error handling
        try:
            
            title_unclean = result.find('h3').text
            title = title_unclean.split('Enhanced', 1)[0].strip()
                
            link = 'https://astrogeology.usgs.gov' + result.a['href']

            browser.visit(link)
            
            html = browser.html
            soup = bs(html, 'html.parser')
            
            img_src = 'https://astrogeology.usgs.gov' + soup.find('img', class_="wide-image")['src']
            
            hemisphere_image_urls.append({"title":title, "img_url":img_src})
            
            url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

            browser.visit(url)
                
        except AttributeError as e:
            print(e)
    ##---------------------------------------------------------------

    ## ONE DICTIONARY
    ##---------------------------------------------------------------
    final_dictionary = {
    "news_title":news_title,
    "news_p":news_p,
    "featured_image":featured_image_url,
    "mars_weather":mars_weather,
    # "facts":tables[0],
    "hemisphere_image_urls":hemisphere_image_urls
    }
    ##---------------------------------------------------------------

    return final_dictionary
