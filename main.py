
import json
import os
import re
from sys import stderr as STREAM
import animeworld as aw

kb = 1024

anime_global_directory = os.path.realpath(
    "/media/damon-ssd/mediaserver/downloads")
parallel_downloads = 20
print(anime_global_directory + "\n")


def getAnimeName(episode_link):
    split = episode_link.split("/")
    directory = split[-2]
    directory = directory.rstrip('ITA')
    return ("_").join(re.split("(?<=.)(?=[A-Z])", directory))


def read_configuration():
    file = open('/home/damon/Video/anime_downloader/anime_monitor.json')

    return json.load(file)


def write_configuration(p_configuration):
    file = open('/home/damon/Video/anime_downloader/anime_monitor.json', 'w')
    file.write(json.dumps(p_configuration))


def download_episode(episode_link, anime_name=None, episode_number=None):
    split = episode_link.split("/")
    if anime_name:
        directory = anime_name
    else:
        directory = getAnimeName(episode_link)

    if episode_number:
        episode_name = directory + "_Ep_" + str(episode_number)
    else:
        episode_name = split[-1]

    anime_path = os.path.join(anime_global_directory, directory)
    file_path = os.path.join(anime_path, episode_name)

    command = f"axel -a -n {parallel_downloads} {episode_link} -o {file_path}"

    if not os.path.exists(anime_path):
        os.makedirs(anime_path)

    if os.path.exists(file_path):
        return

    os.system(command)


if __name__ == "__main__":
    breakCondition = False
    while not breakCondition:
        STREAM.write("Menu:\n1)Search anime\n2)Enter anime link")
        selection = int(input("\nChoose: "))

        match selection:
            case 1:
                anime_name = input(
                    "Enter the name of the anime you want to search: ")
                allAnime = aw.find(anime_name)
                print("\n")
                for i in range(len(allAnime)):
                    print(str(i + 1) + " - " + allAnime[i]["name"])

                print("\n0 - Return")

                select_anime_index = int(input("\nChoose: "))
                if select_anime_index == 0:
                    continue
                select_anime_index -= 1
                selected_anime = aw.Anime(allAnime[select_anime_index]["link"])
                print(allAnime[select_anime_index]["link"])
                anime_real_name = allAnime[select_anime_index]["name"].strip(
                    " (ITA)")

                anime_info = selected_anime.getInfo()
                print(anime_real_name, anime_info)
                anime_episodes = selected_anime.getEpisodes()

                start_episode = int(input("Choose starting episode: "))
                end_episode = int(input("Choose ending episode: "))
                for i in range(start_episode-1, end_episode, 1):
                    episode_link = anime_episodes[i].links[0].fileLink()
                    print(episode_link)
                    download_episode(episode_link)
                breakCondition = True
            case 2:
                server_host = input("Enter the server where it's hosted:")
                server_host = server_host[:-1]
                anime = server_host.split("/")[-1][:-3]
                print(anime)
                start_episode = int(input("Choose starting episode: "))
                end_episode = int(input("Choose ending episode: "))
                for i in range(start_episode, end_episode + 1, 1):
                    episode_link = f"{server_host}/{anime}"
                    episode_link += f"_Ep_{('00' + str(i))[-3:]}_ITA.mp4"
                    download_episode(episode_link)
                    STREAM.flush()
                    print(f"Episode {i} downloaded!\n")
            case 3:
                anime_name = input(
                    "Enter the name of the anime you want to search: ")
                allAnime = aw.find(anime_name)
                print("\n")
                for i in range(len(allAnime)):
                    print(str(i) + " - " + allAnime[i]["name"])

                print("\n0 - Return")

                select_anime_index = int(input("\nChoose: "))
                if select_anime_index == 0:
                    continue
                anime_link = allAnime[select_anime_index]["link"]
                selected_anime = aw.Anime(anime_link)

                configuration = read_configuration()
                new_name = getAnimeName(selected_anime.getEpisodes()[
                                        0].links[0].fileLink())
                total_episodes = selected_anime.getInfo()['Episodi']

                download_amount = int(
                    input('How many downloads you want to keep?'))

                new_anime = {'name': new_name, 'link': anime_link,
                             'download_amount': download_amount, 'totalEpisodes': total_episodes}
                print(new_anime)
                configuration.append(new_anime)
                write_configuration(configuration)

            case 0:
                breakCondition = True

            case _:
                continue

        STREAM.flush()
