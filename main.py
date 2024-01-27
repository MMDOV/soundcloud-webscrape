from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
import numpy as np

# url to soundcloud top 50 weekly charts
URL = r'https://soundcloud.com/charts/top'

# default parameters
PARAMS = {
    'genre': 'all-music',
    'country': 'all-countries'
}


def to_csv(params, path=''):
    """
    :param params: genre and country of list
    :param path: path to the csv file (if it doesn't exist, will make it)
    :return: makes a csv file
    """
    if params is None:
        params = {
            'genre': 'all-music',
            'country': 'all-countries'
        }
    response = requests.get(URL, params=params)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    all_items = soup.find(name='section', class_='sounds')
    all_music = all_items.find_all(name='h2')
    title = []
    artist = []
    for music in all_music[1:]:
        title_artist = music.text.split('by')
        title.append(title_artist[0].strip("\n"))
        artist.append(title_artist[1])
    music_dic = {
        "title": title,
        "artist": artist
    }
    data_frame = pd.DataFrame(music_dic)
    data_frame.index = np.arange(1, len(data_frame) + 1)
    data_frame.to_csv(path)


# examples of lists that can be made
to_csv(params=PARAMS, path='top_all_genre.csv')
PARAMS['genre'] = 'pop'
to_csv(params=PARAMS, path='top_pop.csv')
PARAMS['genre'] = 'rock'
to_csv(params=PARAMS, path='top_rock.csv')
PARAMS['genre'] = 'classical'
to_csv(params=PARAMS, path='top_classical.csv')
