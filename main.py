import pycurl
import os
import re
from sys import stderr as STREAM

kb = 1024

anime_global_directory = os.path.realpath("/home/damon/Video")

print(anime_global_directory)


def status(download_t, download_d, upload_t, upload_d):
    STREAM.write(
        "Downloading: {}/{} kiB ({}%)\r".format(
            str(int(download_d / kb)),
            str(int(download_t / kb)),
            str(int(download_d / download_t * 100) if download_t > 0 else 0),
        )
    )
    STREAM.flush()


def scarica_episodio(link_episodio):

    curl = pycurl.Curl()

    split = link_episodio.split("/")
    directory = split[-2]
    directory = directory[:-3]

    directory = ("_").join(re.split("(?<=.)(?=[A-Z])", directory))
    episode_name = split[-1]

    anime_path = os.path.join(anime_global_directory, directory)
    file_path = os.path.join(anime_path, episode_name)

    if not os.path.exists(anime_path):
        os.makedirs(anime_path)

    with open(file_path, "wb") as f:
        curl.setopt(pycurl.URL, link_episodio)
        curl.setopt(pycurl.WRITEDATA, f)
        curl.setopt(pycurl.NOPROGRESS, False)
        curl.setopt(pycurl.XFERINFOFUNCTION, status)

        curl.perform()
        curl.close()


if __name__ == "__main__":
    STREAM.write("Menu:\n1)Cerca anime\n2)Inserisci link anime")
    selection = int(input("\nscegli: "))

    match selection:
        case 1:
            nome_anime = input("Inserisci il nome dell'anime che vuoi cercare: ")
            """
            res = aw.find(nome_anime)
            for item in res:
                print(
                    f"{res.index(item)}: {item['name']} - {item['episodes']} - {item['link']}"
                )
            anime_selection = int(input("Seleziona un anime: "))
            selected_anime = aw.Anime(res[anime_selection]["link"])
            episode_link = selected_anime.getEpisodes()[0].fileInfo()["url"]
            scarica_episodio(episode_link)
            """

        case 2:
            # TODO da implementare
            episode_link = input("Inserisci il link dell'episodio da scaricare: ")
            scarica_episodio(episode_link)
    STREAM.flush()
