import re
import time
import requests 
from bs4 import BeautifulSoup
import pandas as pd 
from urllib.request import Request, urlopen

#extracts lyrics to eminem RINGER
base_url = 'https://api.genius.com' 
genius_url = 'https://genius.com'

def lyrics_from_link(link):
    print(link)
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        soup = BeautifulSoup(webpage, "html.parser")
        lyrics = soup.find('div', class_='lyrics').get_text()
        song_title = soup.find('h1', class_='header_with_cover_art-primary_info-title').get_text()
    except :
        return '', ''
    return lyrics, song_title

def songs_from_album(artist,album):
    search_url = genius_url + "/albums/" + artist_name + '/' + album_title
    print(search_url)
    req = Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    soup = BeautifulSoup(webpage, "html.parser")
    link_list = []
    for link in soup.findAll(href = re.compile('https://genius.com/'+artist+'-')):
        if 'lyrics' in link['href']:
            link_list.append( link['href'])
    return link_list #song_titles
    

if __name__ == "__main__":
    album_df = pd.read_csv("/home/casey/projects/YearFour/ML/rapgenius/album_title.csv")
    #album_df = pd.read_csv("/home/casey/projects/YearFour/ML/rapgenius/album_title2.csv")
    #song_df = pd.read_csv("/home/casey/projects/YearFour/ML/rapgenius/song_database")
    song_df = pd.DataFrame(columns = ['Song', 'Album', 'Year', 'Artist', 'Lyrics']) 
    #print (album_df.loc[0]) 
    for index, row in album_df.iterrows():
        album_title = re.sub(r'[^a-zA-Z\d]','-',album_df.loc[index,'Album']).lower()
        album_title = album_title.capitalize()
        artist_name = re.sub(r'[^a-zA-Z\d]','-', album_df.loc[index,'Artist']).lower()
        artist_name = artist_name.capitalize()

        year = album_df.loc[index,'Year']

        song_links = songs_from_album(artist_name, album_title)
       
        for link in song_links:
            lyrics,song_title = lyrics_from_link(link)
            time.sleep(1.5)
            song_entry = pd.DataFrame({'Song': [song_title],
                                        'Album': [album_title], 
                                        'Year': [year], 
                                        'Artist': [artist_name],
                                        'Lyrics': [lyrics]})
            
            frames = [song_df, song_entry]
            song_df = pd.concat(frames)
    
    song_df.to_csv('song_database')
