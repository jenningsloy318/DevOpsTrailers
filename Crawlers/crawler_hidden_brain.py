import requests
#write crawler to scripe hidden brain podcast audio and transcript, save it locally, from https://hiddenbrain.org/, use class


import bs4
import requests
import os
from lxml import html
import time
for n in range(1,10):
    url = f'https://hiddenbrain.org/category/podcast/page/{n}/'
    response = requests.get(url,allow_redirects=True)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    articales= soup.find_all('article',attrs={'itemscope':'itemscope',})
    os.makedirs('hidden_brain',exist_ok=True)
    for arti in articales:
        episode_link = arti.find('a', attrs={'rel':'bookmark'})['href']
        print(f'starting process episode {episode_link}')
        episode_title=episode_link.split('/')[-2]
        episode_response=requests.get(episode_link)
        episode_soup= bs4.BeautifulSoup(episode_response.text,'html.parser')
        #dom = etree.HTML(str(episode_soup))
        dom = html.fromstring(episode_response.content)
        audio_link = dom.xpath('/html/body/div[2]/div/div/div[1]/main/article/div/div/figure/audio[last()]/@src')[0]
        audio_file_path=f'hidden_brain/{episode_title}.mp3'
        if not os.path.exists(audio_file_path) or os.path.getsize(audio_file_path) == 0 :
            with requests.get(audio_link,stream=True) as r:
                r.raise_for_status()
                with open(audio_file_path, 'wb') as audio_file:
                    for chunk in r.iter_content(chunk_size=4096):
                        audio_file.write(chunk)
            print(f'Saved {audio_file_path}')
        else:
            print(f'{audio_file_path} already exists')
        if episode_soup.find('div',attrs={'id':'ub-content-toggle-panel-0-transcript','role':'region'}):
            transcript_file_path=f'hidden_brain/{episode_title}.txt'
            transcript_content=episode_soup.find('div',attrs={'id':'ub-content-toggle-panel-0-transcript','role':'region'})
            transcript_title=episode_soup.find('h1',attrs={'class':'entry-title','itemprop':'headline'}).get_text()
            #transcript_content=dom.xpath('/html/body/div[2]/div/div/div[1]/main/article/div/div/div[1]/div/div[2]')[0]
            if not os.path.exists(transcript_file_path) or os.path.getsize(transcript_file_path) == 0:
                with  open(transcript_file_path,'w') as html_file:
                    html_file.write(transcript_title)
                    html_file.write(str(transcript_content.get_text(separator='\n\n',strip=False)))
                print(f'Saved {transcript_file_path}')
            else:
                print(f'{transcript_file_path} already exists')
            time.sleep(10)