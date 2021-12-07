#converted using nbconvert--not that great, still had to remove the In/out boxes

#imports
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

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
    news_title = soup.find('div', class_='content_title')
    news_para = soup.find('div', class_='article_teaser_body')

    browser.quit()



    # JPL Images
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")  

    image = soup.find('a', class_="showimg fancybox-thumbs")['href']
    img_url = url + image

    browser.quit()



    # Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(url)

    mars_facts_df = table[1]
    mars_facts_df.rename(columns={"0": "fact_title", "1": "data"}, inplace=True)
    html_table = mars_facts_df.to_html()
    html_table.replace('\n', '')



    # Mars Hemispheres
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    #blank list for dictionaries
    hemisphere_image_urls = []
    hemi_list=['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']

    for x in hemi_list:
        browser.links.find_by_partial_text(x + ' Hemisphere Enhanced').click()
        #create soup object for new page
        html = browser.html
        soup = bs(html, 'html.parser')
        
        #find image link and title    
        title = soup.find('h2', class_='title').text
        partial = soup.find('img', class_='wide-image')['src']
        img_url = url + partial

        #append to dictionary
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        
        #return to homepage
        browser.links.find_by_partial_text('Back').click()

    browser.quit()
####################################
    return 