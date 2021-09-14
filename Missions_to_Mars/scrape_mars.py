
# import necessary libraries
import os
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser), 
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser), 
        "last_modified": dt.datetime.now()
    }
    #NASA Mars News
    browser.quit()
    return data
def mars_news(browser):

    url = 'https://redplanetscience.com'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find("div", class_= "content_title").get_text()
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return news_title, news_p

def featured_image(browser):

    url ='https://spaceimages-mars.com'
    browser.visit(url)

    # HTML Object
	img_html = browser.html
	img_soup = BeautifulSoup(img_html, "html.parser")

	# Find image url to the full size
	featured_image = img_soup.find("article")["style"].replace('background-image: url(','').replace(');', '')[1:-1]
	
	# Display url
	main_url = "https://www.jpl.nasa.gov"
	
	# Connect website url with scrapped route
	featured_image_url = main_url + featured_image


	#mars_info["featured_image_url"] = featured_image_url
        return featured_image_url
 
 #Mars Facts
 
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace =True)
    return df.to_html(classes="table-table-striped")

def hemispheres(browser):
        url = 'https://marshemispheres.com/'
        browser.visit(url + 'index.html')

        hemisphere_image_urls =[]

        for i in range(4):
            browser.find_by_css("a.product-item img")[i].click()
            hemi_data = scrape_hemispheres(browser.html)
            hemi_data['img_url'] = url + hemi_data['img_url']
            hemisphere_image_urls.append(hemi_data)
            browser.back()
        return hemisphere_image_urls

def scrape_hemisphere(text_html):
    hemisphere_soup = BeautifulSoup(text_html, "html.parser")
    try:
        title_text = hemisphere_soup.find('h2', class_ = 'title').get_text()
        image_ref = hemisphere_soup.find('a', text = 'Sample').get('href')
    except AttributeError:
        title_text = None
        image_ref = None
        
    hemispheres = {"title" : title_text, "image_url" : image_ref}
    return hemispheres 

if __name__ == '__main__' : 
    print(scrape_all())
            



