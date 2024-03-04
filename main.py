import pycurl
import os
import re
from io import BytesIO
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
    buffer = BytesIO()

    split = link_episodio.split("/")
    directory = split[-2]
    directory = directory[:-3]

    directory = ("_").join(re.split("(?<=.)(?=[A-Z])", directory))

    episode_name = directory + "_Ep_" + ("_").join(split[-1].split("_")[-2:])

    anime_path = os.path.join(anime_global_directory, directory)
    file_path = os.path.join(anime_path, episode_name)

    if not os.path.exists(anime_path):
        os.makedirs(anime_path)

    with open(file_path, "wb") as f:
        curl.setopt(pycurl.URL, link)
        curl.setopt(pycurl.WRITEDATA, f)
        curl.setopt(pycurl.NOPROGRESS, False)
        curl.setopt(pycurl.XFERINFOFUNCTION, status)

        curl.perform()
        curl.close()


link = input("Inserisci il link dell'episodio che vuoi scaricare: ")

scarica_episodio(link)
