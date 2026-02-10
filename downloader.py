#from argparse import ArgumentParser
from pathlib import Path
import sys
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from yt_dlp import YoutubeDL

#parser = ArgumentParser()
#parser.add_argument("playlist_link", type=str, help="link to the album playlist (must be wraped in quotes)")
#args = parser.parse_args()
#if args.playlist_link == "":
#    print("Usage: python3 downloader.py \"<link-to-album-playlist>\"")
#    print("Note: Quotes are required around the link")
#    sys.exit()

def download_song(url: str):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(5)

    title = driver.find_element(By.ID, "above-the-fold").find_element(By.ID, "title").find_element(By.TAG_NAME, "yt-formatted-string").get_attribute("title")
    title = title.replace("/", "_slash_")
    title = title.replace("\\", "_back_slash_")

    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "opus",
        }],
        "noplaylist": True,
        #"remote-components": "ejs:github", # Doesn't work TT
        "outtmpl": title
    }
    with YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)
    
def download_album(url: str):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    driver.implicitly_wait(5)
    playlist = driver.find_element(By.ID, "playlist")
    videos = playlist.find_element(By.ID, "items")
    link_elements = videos.find_elements(By.ID, "wc-endpoint")
    video_title_elements = videos.find_elements(By.ID, "video-title")

    video_titles = []
    for t in video_title_elements:
        video_titles.append(t.get_attribute("title").replace("/", "_slash_").replace("\\", "_back_slash_"))

    links = []
    for l in link_elements:
        links.append(l.get_attribute("href"))

    title_element = driver.find_element(By.ID, "header-description")
    title = title_element.find_element(By.TAG_NAME, "yt-formatted-string").get_attribute("title")
    title = title.replace("/", "_slash_")
    title = title.replace("\\", "_back_slash_")
    Path(title).mkdir(exist_ok=True)

    ydl_opts = {
        #"format": "bestaudio", # This might be something that's deprecated (not sure)
        "format": "m4a/bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "opus",
        }],
        "noplaylist": True,
        #"outtmpl": title+"/%(title)s",
    }

    dir_sep = "/"
    if os.name == "nt":
        dir_sep = "\\"

    for i in range(len(links)):
        prefix = ""
        if i < 9:
            prefix = "0"+str(i+1)+" - "
        else:
            prefix = str(i+1)+" - "
        
        ydl_opts["outtmpl"] = title+dir_sep+prefix+video_titles[i]
        with YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(links[i])

