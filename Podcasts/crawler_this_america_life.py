import os
import requests
from bs4 import BeautifulSoup,Tag

# URL of the archive page
for pageNum in range(1, 10):
    url = 'https://www.thisamericanlife.org/archive'+'?page='+pageNum
    print(f"Processing page: {url}")
    # Create a folder to save the audio and transcript files
    os.makedirs('this_american_life', exist_ok=True)

    # Send a GET request to the archive page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the episode container
    episode_container = soup.find('div', id='content').find('main', id='main').find('div', class_='region region-content').find('div', id='block-system-main').find('div', class_='content')

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
        article_links = episode_soup.find('body').find('div', id='content').find('main', id='main').find('div', class_='region region-content').find('div', id='block-system-main',class_='block block-system').find('div', class_='content').find('article').find('header',class_='episode-header').find('div',class_='container clearfix').find('ul',class_='actions').find_all('li')
        for link in article_links:
            if not link.get('class'):
                transcript_link="https://www.thisamericanlife.org"+link.a['href']
            elif link.get('class')==['download']:
                audio_link=link.a['href']


    #    print(f"Processing episode: {audio_link} and {transcript_link}")

        # Download the audio file
        audio_response = requests.get(audio_link)
        audio_filename = os.path.basename(episode_name+'.mp3')
        audio_filepath = os.path.join('this_american_life', audio_filename)
        with open(audio_filepath, 'wb') as audio_file:
            audio_file.write(audio_response.content)

        # Download the transcript file
        transcript_response = requests.get(transcript_link)
        transcript_filename = os.path.basename(episode_name+'.html')
        transcript_filepath = os.path.join('this_american_life', transcript_filename)
        with open(transcript_filepath, 'wb') as transcript_file:
            transcript_file.write(transcript_response.content)

        print(f"Downloaded: {audio_filename} and {transcript_filename}")

    print("Scraping completed.")
