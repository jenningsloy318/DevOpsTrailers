import os
import requests
from bs4 import BeautifulSoup,Tag
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from lxml import etree
import time
# URL of the archive page
for pageNum in range(1, 10):
    url = 'https://hbr.org/2018/01/podcast-ideacast?page='+str(pageNum)
    print(f"Processing page: {url}")
    # Create a folder to save the audio and transcript files
    os.makedirs('ideacast', exist_ok=True)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-data-dir=selenium")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    #WebDriverWait(driver,70).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='load-ten-more' and //div/acontains(., 'Load More')]"))).click()
    #i=1
    #while i<11:
    #     try:
    #        element = WebDriverWait(driver,70).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='load-ten-more' and //a.text()=' Load more items']")))
    #        element.location_once_scrolled_into_view
    #        driver.execute_script("arguments[0].click();", element)
    #        print(i)
    #        i=i+1
    #    except TimeoutException:
    #           print("Time out!")
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'html.parser')

    episode_container = soup.find('body').find('div', attrs={'id':'main','class':'container'}).find('div', attrs={'class':'component','data-order':'4'}).find('article-content', attrs={'class':'article-content'}).find('div', attrs={'js-target':'article-content'}).find('div', attrs={'class':'row'}).find('div',attrs={'class':'content-area--full column'}).find('div',attrs={'class':'article article-first-row'}).find('section',attrs={'class':'series-page'}).find('div',attrs={'class':'row'}).find('div',attrs={'class':'series-page__container'}).find('main',attrs={'class':'series-page__main'}).find('div',role="list")
    #.find('div',attrs={'role':'list','class':'series-page__podcast-list','aria-label':'Podcasts'})

    #/body/div[1]/div[4]/article-content/div/div/div/div/section/div/div[2]/main/div[2]
    # Find all the episode articles in the container
    episode_articles = episode_container.find_all('div',attrs={'role':'listitem','class':'series-page__podcast-list-item'})
    print(episode_articles)
    for article in episode_articles:
        # Find the episode audio link
        #article_links = article.find('div', id='content').find('main', id='main').find('div', class_='region region-content').find('div', id='block-system-main').find('div', class_='content').find('article').find('header',class_='episode-header').find('div',class_='container clearfix').find('ul',class_='actions').find('li')
        episode_href=article.find('div',attrs={'class':'series-page__podcast-info-column'}).find('h3',attrs={'class':'podcast__h3'}).find('a',attrs={'class':'podcast-page__link'})['href']
        episode_link='https://hbr.org'+episode_href
        episode_index=article.find('div',attrs={'class':'series-page__podcast-info-column'}).find('p',attrs={'class':'podcast__p'}).get_text().split()[1]
        episode_title=article.find('div',attrs={'class':'series-page__podcast-info-column'}).find('h3',attrs={'class':'podcast__h3'}).find('a',attrs={'class':'podcast-page__link'}).get_text().replace(' ','-')
        episode_name=episode_index+'-'+episode_title

        print(f"processing epsode: {episode_link}")
        driver.get(episode_link)
        episode_response_html_text = driver.page_source
        episode_soup = BeautifulSoup(episode_response_html_text, 'html.parser')
        #audio_link = episode_soup.find('body').find('div', attrs={'id':'main','class':'container'}).find('div',          attrs={'class':'component','data-order':'4'}).find('article-content', attrs={'class':'article-content'}).find('div', attrs={'js-target':'article-content'}).find('section',attrs={'class':'podcast-post'}).find('div', attrs={'class':'row'}).find('div',attrs={'class':'podcast-post__banner-wrapper'}).find('div',attrs={'class':'podcast-post__banner podcast-post__banner--ideacast'}).find('div',attrs={'class':'podcast-post__banner-container'}).find('div',attrs={'class':'podcast-post__banner-info'}).find('div',attrs={'class':'podcast-post__banner-player'}).find('audio',attrs={'id':'js-player','class':'podcast-post__audio-file'})['src']
        dom = etree.HTML(str(episode_soup))
        audio_link=dom.xpath('/html/body/div[1]/div[4]/article-content/div/section[1]/div/div[2]/div/div/div[2]/div[1]/audio/@src')[0]
        print(f"downloading audo from {audio_link}")
        # Download the audio file
        audio_response = requests.get(audio_link)
        audio_filename = os.path.basename(episode_name+'.mp3')
        audio_filepath = os.path.join('ideacast', audio_filename)
        with open(audio_filepath, 'wb') as audio_file:
            audio_file.write(audio_response.content)

        # Download the transcript file
        print(f"downloading transcript")
        transcript_content = episode_soup.find('body',attrs={'class':'podcast-episode'}).find('div', attrs={'id':'main','class':'container'}).find('div', attrs={'class':'component','data-order':'4'}).find('article-content', attrs={'class':'article-content'}).find('div', attrs={'js-target':'article-content'}).find('section',attrs={'class':'podcast-post'}).find('div', attrs={'class':'row'}).find('div',attrs={'class':'podcast-post__container'}).find('div',attrs={'class':'podcast-post__main'}).find('div',attrs={'class':'podcast-tabs__content'}).find('section',attrs={'id':'transcript-section','class':'podcast-tabs__section','role':'tabpanel'})

        #print(transcript_content)
        transcript_filename = os.path.basename(episode_name+'.html')
        transcript_filepath = os.path.join('ideacast', transcript_filename)

        with open(transcript_filepath, 'w',encoding='utf-8') as transcript_file:
          for item in transcript_content.find_all('p'):
            transcript_file.writelines(str(item)+'\n')


        print(f"Downloaded: {audio_filename} and {transcript_filename}")
        time.sleep(10)

print("Scraping completed.")
