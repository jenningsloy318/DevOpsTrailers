import os
import requests
from bs4 import BeautifulSoup,Tag
from selenium import webdriver

# URL of the archive page
for pageNum in range(0, 10):
    url = 'https://hbr.org/2018/01/podcast-ideacast?page='+str(pageNum)
    print(f"Processing page: {url}")
    # Create a folder to save the audio and transcript files
    os.makedirs('ideacast', exist_ok=True)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'html.parser')

    episode_container = soup.find('body').find('div', attrs={'id':'main','class':'container'}).find('div', attrs={'class':'component','data-order':'4'}).find('article-content', attrs={'class':'article-content'}).find('div', attrs={'js-target':'article-content'}).find('div', attrs={'class':'row'}).find('div',attrs={'class':'content-area--full column'}).find('div',attrs={'class':'article article-first-row'}).find('section',attrs={'class':'series-page'}).find('div',attrs={'class':'row'}).find('div',attrs={'class':'series-page__container'}).find('main',attrs={'class':'series-page__main'}).find('div',role="list")
    #.find('div',attrs={'role':'list','class':'series-page__podcast-list','aria-label':'Podcasts'})

    #/body/div[1]/div[4]/article-content/div/div/div/div/section/div/div[2]/main/div[2]
    # Find all the episode articles in the container
    episode_articles = episode_container.find_all('div',attrs={'role':'listitem','class':'series-page__podcast-list-item'})

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
        audio_link = episode_soup.find('body',attrs={'class':'podcast-episode'}).find('div', attrs={'id':'main','class':'container'}).find('div', attrs={'class':'component','data-order':'4'}).find('article-content', attrs={'class':'article-content'}).find('div', attrs={'js-target':'article-content'}).find('section',attrs={'class':'podcast-post'}).find('div', attrs={'class':'row'}).find('div',attrs={'class':'podcast-post__banner-wrapper'}).find('div',attrs={'class':'podcast-post__banner podcast-post__banner--ideacast'}).find('div',attrs={'class':'podcast-post__banner-container'}).find('div',attrs={'class':'podcast-post__banner-info'}).find('div',attrs={'class':'podcast-post__banner-player'}).find('audio',attrs={'id':'js-player','class':'podcast-post__audio-file'})['src']

        # Download the audio file
        audio_response = requests.get(audio_link)
        audio_filename = os.path.basename(episode_name+'.mp3')
        audio_filepath = os.path.join('ideacast', audio_filename)
        with open(audio_filepath, 'wb') as audio_file:
            audio_file.write(audio_response.content)


        # Download the transcript file
        transcript_link = episode_soup.find('body',attrs={'class':'podcast-episode'}).find('div', attrs={'id':'main','class':'container'}).find('div', attrs={'class':'component','data-order':'4'}).find('article-content', attrs={'class':'article-content'}).find('div', attrs={'js-target':'article-content'}).find('section',attrs={'class':'podcast-post'}).find('div', attrs={'class':'row'}).find('div',attrs={'class':'podcast-post__container'}).find('div',attrs={'class':'podcast-post__main'}).find('div',attrs={'class':'podcast-tabs__content'}).find('section',attrs={'id':'transcript-section','class':'podcast-tabs__section','role':'tabpanel'})

        transcript_content=[]

        for item in transcript_link.find_all('p'):
            transcript_content.append(item.encode())


        #print(transcript_content)
        transcript_filename = os.path.basename(episode_name+'.html')
        transcript_filepath = os.path.join('ideacast', transcript_filename)

        with open(transcript_filepath, 'wb') as transcript_file:
            transcript_file.writelines("\n".join(transcript_content))


        print(f"Downloaded: {audio_filename} and {transcript_filename}")
        exit(1)
print("Scraping completed.")
