#!/home/damon/Video/anime_downloader/.env/bin/python

from time import sleep
from main import *


configuration = read_configuration()

for anime in configuration:
    anime_obj = aw.Anime(anime['link'])
    anime_path = os.path.join(anime_global_directory, anime['name'])

    if not os.path.exists(anime_path):
        os.makedirs(anime_path)

    directory = os.listdir(anime_path)
    file_count = len(directory)
    if file_count < anime['download_amount']:
        last_episode = directory[-1] if directory else 1
        if last_episode != 1:
            last_episode_number = int(
                re.search(r"Ep_(\d+)_", last_episode).group(1))
        else:
            last_episode_number = 1

        episodes_to_download = anime['download_amount'] - file_count

        anime_episodes = anime_obj.getEpisodes()
        for i in range(last_episode_number, last_episode_number + episodes_to_download):
            print(i)
            continue
            episode_link = anime_episodes[i].links[0].fileLink()
            download_episode(episode_link, anime['name'], i)
