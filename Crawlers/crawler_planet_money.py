import os
import requests
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import  undetected_chromedriver as uc

from lxml import etree
import time
# URL of the archive page
os.makedirs('planet_money', exist_ok=True)
url = 'https://www.npr.org/podcasts/510289/planet-money'
chrome_options = uc.options.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument('--always-authorize-plugins=true')
chrome_options.add_argument('--disable-blink-features=AutomationControlled"')
chrome_options.add_argument('--start-in-incognito')
# Create a folder to save the audio and transcript files
bypass_paywalls_ext_path = "/Users/I336589/development/osc-projects/bypass-paywalls-chrome"
# https://github.com/iamadamdev/bypass-paywalls-chrome
chrome_options.add_argument(f"--load-extension={bypass_paywalls_ext_path}")
driver = uc.Chrome(options=chrome_options)
driver.get(url)


total_episode_articles=[]
#load_more_element = driver.find_elements(By.XPATH,"//button[@class='options__load-more' and text()='Load more episodes']")

for i in range(20):
    try:
          load_more_element = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='options__load-more' and text()='Load more episodes']")))
          load_more_element.location_once_scrolled_into_view
          driver.execute_script("arguments[0].click();", load_more_element)
          time.sleep(5)
    except TimeoutException:
          print(f"Retrieve eposide list finished!")

root_html_text = driver.page_source
root_soup = BeautifulSoup(root_html_text, 'html.parser')
episode_container = root_soup.find('body').find('main', attrs={'aria-label': 'main content'}).find('div', attrs={'id': 'wrapper'}).find('section', attrs={'id': 'main-section'}).find('section', attrs={'class': 'podcast-section episode-list'})

# Find all the episode articles in the container
episode_articles = episode_container.find_all('article', attrs={'class': 'item podcast-episode'})

for article in episode_articles:
    # Find the episode audio link
    episode_link = article.find('div', attrs={'class': 'item-info'}).find('h2', attrs={'class': 'title'}).find('a')['href']
    episode_title = article.find('div', attrs={'class': 'item-info'}).find('h2', attrs={'class': 'title'}).find('a').get_text().replace(' ','-')
    episode_index = article.find('div', attrs={'class': 'item-info'}).find('h3', attrs={'class': 'episode-date'}).find('time')['datetime']
    episode_name = episode_index+'-'+episode_title

    transcript_link = article.find('div', attrs={'class': 'item-info'}).find('article',attrs={'class': 'bucketwrap resaudio','aria-label':'audio-module'}).find('div',attrs={'class': 'audio-module'}).find('div',attrs={'class': 'audio-module-tools'}).find('ul',attrs={'class': 'audio-module-more-tools'}).find('li',attrs={'class': 'audio-tool audio-tool-transcript'}).find('a')['href']

    print(f"episode link {episode_link} and transcript link {transcript_link}")

    print(f"processing epsode: {episode_link}")
    driver.get(episode_link)
    episode_response_html_text = driver.page_source
    episode_soup = BeautifulSoup(episode_response_html_text, 'html.parser')


    dom = etree.HTML(str(episode_soup))


    audio_link = episode_soup.find('body').find('main',attrs={'aria-label': 'main content'}).find('div',attrs={'id': 'wrapper'}).find('section',attrs={'id': 'main-section'}).find('article',attrs={'class': 'story'}).find('div',attrs={'id':'primaryaudio','class':'storylocation linkLocation'}).find('article',attrs={'class':'bucketwrap resaudio primaryaudio','aria-label':'audio-module'}).find('div',attrs={'class': 'audio-module'}).find('div',attrs={'class': 'audio-module-tools'}).find('ul',attrs={'class': 'audio-module-more-tools'}).find('li',attrs={'class': 'audio-tool audio-tool-download'}).find('a')['href']

    # Download the audio file
    print(f"downloading audio from {audio_link}")
    audio_filename = os.path.basename(episode_name+'.mp3')
    audio_filepath = os.path.join('planet_money', audio_filename)
    if not os.path.exists(audio_filepath):
        audio_response = requests.get(audio_link)
        with open(audio_filepath, 'wb') as audio_file:
            audio_file.write(audio_response.content)

    # Download the transcript file
    print(f"downloading transcript")
    transcript_filename = os.path.basename(episode_name+'.html')
    transcript_filepath = os.path.join('planet_money', transcript_filename)
    if not os.path.exists(transcript_filepath):
      transcript_response = requests.get(transcript_link)
      transcript_soup = BeautifulSoup(transcript_response.text, 'html.parser')
      iframe = transcript_soup.find_all('footer')
      for item in iframe:
          item.decompose()
      share = transcript_soup.find_all('div',attrs={'class': 'share-tools share-tools--secondary'})
      for item in share:
          item.decompose()
      head = transcript_soup.find_all('ul',attrs={'class': 'podcast-tools podcast-tools--510289'})
      for item in head:
          item.decompose()
      head2 = transcript_soup.find_all('header',attrs={'class': 'npr-header'})
      for item in head2:
          item.decompose()
      h1 = transcript_soup.find_all('div',attrs={'id': 'story-meta'})
      for item in h1:
          item.decompose()
      h2 = transcript_soup.find_all('div',attrs={'id': 'primaryaudio','class':'storylocation linkLocation'})
      for item in h2:
          item.decompose()
      h3 = transcript_soup.find_all('div',attrs={'id': 'global-stickybar-mount-piano-wrap'})
      for item in h3:
          item.decompose()
      script=transcript_soup.find_all('script')
      for item in script:
          item.decompose()
      player=transcript_soup.find_all('div',attrs={'class': 'player-react-mount'})
      for item in player:
          item.decompose()
      aside=transcript_soup.find_all('aside')
      for item in aside:
          item.decompose()
      asidebar=transcript_soup.find_all('div',attrs={'id':"main-sidebar"})
      for item in asidebar:
          item.decompose()
      p = transcript_soup.find_all('p',attrs={'class': 'disclaimer'})
      for item in p:
          item.decompose()
      p2 = transcript_soup.find_all('p',attrs={'class': 'left'})
      for item in p2:
          item.decompose()
      p3 = transcript_soup.find_all('p',attrs={'class': 'right'})
      for item in p3:
          item.decompose()
      for a in transcript_soup.findAll('a'):
          del a['href']

      with open(transcript_filepath, 'w') as transcript_file:
              transcript_file.write(transcript_soup.prettify())

    print(f"Downloaded: {audio_filename} and {transcript_filename}")
    time.sleep(5)

print("Scraping completed.")
