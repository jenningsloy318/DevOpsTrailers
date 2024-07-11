import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL of the archive page
# #https://aliabdaal.com/podcast/
url = 'https://up.audio/podcasts/itunes1587142091'
os.makedirs('Deep_Dive_with_Ali_Abdaal', exist_ok=True)
requests.adapters.DEFAULT_RETRIES = 10
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}
proxies = {
    'http': 'socks5://192.168.8.1:38080',
    'https': 'socks5://192.168.8.1:38080',
}
# Send a GET request to the archive page
response = requests.get(url, allow_redirects=True, headers=headers, proxies=proxies)
root_soup = BeautifulSoup(response.text, 'html.parser')
if root_soup.find_all('ul', attrs={'class': 'no-style episodes-list mt-2'}):
    episode_list = root_soup.find_all('ul', attrs={'class': 'no-style episodes-list mt-2'})[0].find_all('li', attrs={'class': 'boldish'})
    for episode in episode_list:
        episode_title = episode.find('a')['onclick'].split(',')[2].replace('"', '').strip()
        episode_date = episode.find('span', attrs={'class': 'title tight-lines'}).find('span', attrs={'class': 'tiny text-muted weight-300 nowrap'}).get_text().strip().split('–')[0].strip()
        episode_index = datetime.strptime(episode_date, '%b %d, %Y').date().strftime("%Y-%m-%d")
        episode_name = episode_index + '-' + episode_title
        print(f"process episode {episode_name}")
        audio_link = episode.find('a')['onclick'].split(',')[0].split('"')[1]
        print(f"audio_link {audio_link}")
        audio_filename = os.path.basename(episode_name + '.mp3')
        audio_filepath = os.path.join('Deep_Dive_with_Ali_Abdaal', audio_filename)
        if not os.path.exists(audio_filepath):
            audio_response = requests.get(audio_link, proxies=proxies)
            with open(audio_filepath, 'wb') as audio_file:
                audio_file.write(audio_response.content)
                print(f"Downloaded: {audio_filename}")
        else:
            print(f"{audio_filename} already exists, skipped")
