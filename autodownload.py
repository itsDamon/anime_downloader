#!/home/damon/Video/anime_downloader/.env/bin/python

from time import sleep
from main import * 


configuration = read_configuration()

for anime in configuration:
    anime_obj = aw.Anime(anime['link'])
    anime_path = os.path.join(anime_global_directory, anime['name'])

    directory = os.listdir(anime_path)
    file_count = len(directory)
    if file_count < anime['download_amount']:
        last_episode = directory[-1]
        last_episode_number = int(re.search(r"Ep_(\d+)_", last_episode).group(1))

        episodes_to_download = anime['download_amount'] - file_count

        anime_episodes = anime_obj.getEpisodes()
        for i in range (last_episode_number, last_episode_number + episodes_to_download):
            episode_link = anime_episodes[i].links[0].fileLink()
            download_episode(episode_link)

