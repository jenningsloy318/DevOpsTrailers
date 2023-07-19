import os
import requests
from bs4 import BeautifulSoup

# URL of the archive page
for pageNum in range(0, 10):
    url = 'https://www.thisamericanlife.org/archive?page='+str(pageNum)
    print(f"Processing page: {url}")
    # Create a folder to save the audio and transcript files
    os.makedirs('this_american_life', exist_ok=True)

    # Send a GET request to the archive page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the episode container
    episode_container = soup.find('body').find('div', attrs={'id':'content'}).find('main', attrs={'id':'main'}).find('div', attrs={'class':'region region-content'}).find('div', attrs={'id':'block-system-main'}).find('div', attrs={'class':'content'})

    # Find all the episode articles in the container
    episode_articles = episode_container.find_all('article')

    for article in episode_articles:
        # Find the episode audio link
        #article_links = article.find('div', id='content').find('main', id='main').find('div', class_='region region-content').find('div', id='block-system-main').find('div', class_='content').find('article').find('header',class_='episode-header').find('div',class_='container clearfix').find('ul',class_='actions').find('li')
        episode_href=article.find('header',class_='clearfix').find('a')['href']
        episode_link='https://www.thisamericanlife.org'+episode_href
        episode_name=episode_href[1:].replace('/','-')
        print(f"processing epsode: {episode_link}")
        episode_response = requests.get(episode_link)
        episode_soup = BeautifulSoup(episode_response.text, 'html.parser')
        article_links = episode_soup.find('body').find('div', attrs={'id':'content'}).find('main', attrs={'id':'main'}).find('div', attrs={'class':'region region-content'}).find('div', attrs={'id':'block-system-main','class':'block block-system'}).find('div', attrs={'class':'content'}).find('article').find('header',attrs={'class':'episode-header'}).find('div',attrs={'class':'container clearfix'}).find('ul',attrs={'class':'actions'}).find_all('li')
        for link in article_links:
            if not link.get('class'):
                transcript_link="https://www.thisamericanlife.org"+link.a['href']
            elif link.get('class')==['download']:
                audio_link=link.a['href']


        print(f"Processing episode: {audio_link} and {transcript_link}")

        # Download the audio file
        audio_response = requests.get(audio_link)
        audio_filename = os.path.basename(episode_name+'.mp3')
        audio_filepath = os.path.join('this_american_life', audio_filename)
        with open(audio_filepath, 'wb') as audio_file:
            audio_file.write(audio_response.content)

        # Download the transcript file
        transcript_response = requests.get(transcript_link)
        transcript_soup = BeautifulSoup(transcript_response.text, 'html.parser')
        iframe = transcript_soup.find_all('iframe',id="odh-popup")
        for item in iframe:
            item.decompose()
        footer=transcript_soup.find_all('footer',id="footer")
        for item in footer:
            item.decompose()
        header=transcript_soup.find_all('header',id="site-header",role="banner")
        for item in header:
            item.decompose()
        player=transcript_soup.find_all('div',id="player")
        for item in player:
            item.decompose()
        meta=transcript_soup.find_all('div',class_="transcript__meta")
        for item in meta:
            item.decompose()
        script=transcript_soup.find_all('script')
        for item in script:
            item.decompose()
        href=transcript_soup.find_all('a')
        for item in href:
            del item['href']

        #print(transcript_content)
        transcript_filename = os.path.basename(episode_name+'.html')
        transcript_filepath = os.path.join('this_american_life', transcript_filename)

        with open(transcript_filepath, 'w') as transcript_file:
           transcript_file.write(transcript_soup.prettify())

        print(f"Downloaded: {audio_filename} and {transcript_filename}")

print("Scraping completed.")
