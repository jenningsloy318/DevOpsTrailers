import os
import requests
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from lxml import etree
import time
# URL of the archive page
os.makedirs('ideacast', exist_ok=True)
url = 'https://hbr.org/2018/01/podcast-ideacast'
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument('--always-authorize-plugins=true')
# Create a folder to save the audio and transcript files
bypass_paywalls_ext_path = "/Users/I336589/development/osc-projects/bypass-paywalls-chrome"
# https://github.com/iamadamdev/bypass-paywalls-chrome
chrome_options.add_argument(f"--load-extension={bypass_paywalls_ext_path}")
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)


year_element=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//a[@class='slick-track' and text()=' Load more items']")))


load_more_element = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//a[@href='#' and text()=' Load more items']")))
while load_more_element:
  try:
      load_more_element = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//a[@href='#' and text()=' Load more items']")))
      load_more_element.location_once_scrolled_into_view
      driver.execute_script("arguments[0].click();", load_more_element)
  except TimeoutException:
      print("Time out!")
      load_more_element=''

root_html_text = driver.page_source
root_soup = BeautifulSoup(root_html_text, 'html.parser')
episode_container = root_soup.find('body').find('div', attrs={'id': 'main', 'class': 'container'}).find('div', attrs={'class': 'component', 'data-order': '4'}).find('article-content', attrs={'class': 'article-content'}).find('div', attrs={'js-target': 'article-content'}).find('div', attrs={'class': 'row'}).find(
    'div', attrs={'class': 'content-area--full column'}).find('div', attrs={'class': 'article article-first-row'}).find('section', attrs={'class': 'series-page'}).find('div', attrs={'class': 'row'}).find('div', attrs={'class': 'series-page__container'}).find('main', attrs={'class': 'series-page__main'}).find('div', role="list")

# Find all the episode articles in the container
episode_articles = episode_container.find_all(
    'div', attrs={'role': 'listitem', 'class': 'series-page__podcast-list-item'})
for article in episode_articles:
    # Find the episode audio link
    episode_href = article.find('div', attrs={'class': 'series-page__podcast-info-column'}).find(
        'h3', attrs={'class': 'podcast__h3'}).find('a', attrs={'class': 'podcast-page__link'})['href']
    episode_link = 'https://hbr.org'+episode_href
    episode_index = article.find('div', attrs={'class': 'series-page__podcast-info-column'}).find(
        'p', attrs={'class': 'podcast__p'}).get_text().split()[1]
    #episode_title = article.find('div', attrs={'class': 'series-page__podcast-info-column'}).find('h3', attrs={
        'class': 'podcast__h3'}).find('a', attrs={'class': 'podcast-page__link'}).get_text().replace(' ', '-')
    episode_title=episode_href.split('/')[-1]
    episode_name = episode_index+'-'+episode_title

    print(f"processing epsode: {episode_link}")
    driver.get(episode_link)
    episode_response_html_text = driver.page_source
    episode_soup = BeautifulSoup(episode_response_html_text, 'html.parser')
    #audio_link = episode_soup.find('body').find('div', attrs={'id':'main','class':'container'}).find('div',          attrs={'class':'component','data-order':'4'}).find('article-content', attrs={'class':'article-content'}).find('div', attrs={'js-target':'article-content'}).find('section',attrs={'class':'podcast-post'}).find('div', attrs={'class':'row'}).find('div',attrs={'class':'podcast-post__banner-wrapper'}).find('div',attrs={'class':'podcast-post__banner podcast-post__banner--ideacast'}).find('div',attrs={'class':'podcast-post__banner-container'}).find('div',attrs={'class':'podcast-post__banner-info'}).find('div',attrs={'class':'podcast-post__banner-player'}).find('audio',attrs={'id':'js-player','class':'podcast-post__audio-file'})['src']
    dom = etree.HTML(str(episode_soup))
    audio_link = dom.xpath(
        '/html/body/div[1]/div[4]/article-content/div/section[1]/div/div[2]/div/div/div[2]/div[1]/audio/@src')[0]
    print(f"downloading audio from {audio_link}")
    # Download the audio file
    audio_response = requests.get(audio_link)
    audio_filename = os.path.basename(episode_name+'.mp3')
    audio_filepath = os.path.join('ideacast', audio_filename)
    with open(audio_filepath, 'wb') as audio_file:
        audio_file.write(audio_response.content)

    # Download the transcript file
    print(f"downloading transcript")
    transcript_content = episode_soup.find('body', attrs={'class': 'podcast-episode'}).find('div', attrs={'id': 'main', 'class': 'container'}).find('div', attrs={'class': 'component', 'data-order': '4'}).find('article-content', attrs={'class': 'article-content'}).find('div', attrs={'js-target': 'article-content'}).find('section', attrs={
        'class': 'podcast-post'}).find('div', attrs={'class': 'row'}).find('div', attrs={'class': 'podcast-post__container'}).find('div', attrs={'class': 'podcast-post__main'}).find('div', attrs={'class': 'podcast-tabs__content'}).find('section', attrs={'id': 'transcript-section', 'class': 'podcast-tabs__section', 'role': 'tabpanel'})

    # print(transcript_content)
    transcript_filename = os.path.basename(episode_name+'.html')
    transcript_filepath = os.path.join('ideacast', transcript_filename)

    with open(transcript_filepath, 'w', encoding='utf-8') as transcript_file:
        for item in transcript_content.find_all('p'):
            transcript_file.writelines(str(item)+'\n')

    print(f"Downloaded: {audio_filename} and {transcript_filename}")
    time.sleep(10)

print("Scraping completed.")
