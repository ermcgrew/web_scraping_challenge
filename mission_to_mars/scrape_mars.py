#imports
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

#dictionary for storing info to return from function
mars_data = {}

#defining function
def scrape():
    # Mars News Site
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")  

    #save first article heading and teaser paragraph
    news_title = soup.find('div', class_='content_title').text
    news_para = soup.find('div', class_='article_teaser_body').text

    mars_data['news_title'] = news_title
    mars_data['news_para'] = news_para

    browser.quit()


    # JPL Images
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")  

    image = soup.find('a', class_="showimg fancybox-thumbs")['href']
    feature_img = url + image

    mars_data['feature_img'] = feature_img

    browser.quit()


    # Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(url)

    mars_facts_df = table[1]
    mars_facts_df.rename(columns={0: "Stat", 1: "Data"}, inplace=True)
    mars_facts_df.set_index("Stat", inplace=True)

    html_table = mars_facts_df.to_html()
    html_table_clean = html_table.replace('\n', '')
    html_table_clean = html_table_clean.replace('dataframe', 'table')

    mars_data['facts_table'] = html_table_clean


    # Mars Hemispheres
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemi_list=['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']

    for x in hemi_list:
        browser.links.find_by_partial_text(x).click()
        #create soup object for new page
        html = browser.html
        soup = bs(html, 'html.parser')
        
        #find image link and title    
        title = soup.find('h2', class_='title').text
        partial = soup.find('img', class_='wide-image')['src']
        img_url = url + partial

        #append to dictionary
        mars_data[f'{x}_title'] = title
        mars_data[f'{x}_img_url']= img_url
        
        #return to homepage
        browser.links.find_by_partial_text('Back').click()

    browser.quit()
    
    return mars_data