#from argparse import ArgumentParser
from pathlib import Path
import json
import os
import sys
import random

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from yt_dlp import YoutubeDL
import requests

#parser = ArgumentParser()
#parser.add_argument("playlist_link", type=str, help="link to the album playlist (must be wraped in quotes)")
#args = parser.parse_args()
#if args.playlist_link == "":
#    print("Usage: python3 downloader.py \"<link-to-album-playlist>\"")
#    print("Note: Quotes are required around the link")
#    sys.exit()

def download_song(url: str, audio_only: bool=True, proxy: str=""):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    # Enable proxy if provided
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")

    # Disable automation indicator WebDriver flags
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Assign a random user-agent string
    response = requests.get("https://www.useragents.me/", timeout=10)
    response.raise_for_status()
    textarea = BeautifulSoup(response.text, "html.parser").select_one(
        "#most-common-desktop-useragents-json-csv textarea"
    )
    if not textarea:
        raise RuntimeError("Could not find json")
    ua_json = json.loads(textarea.text)
    ua_str = ua_json[random.randint(0, len(ua_json)-1)]["ua"]
    
    # Init driver
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": ua_str})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(url)
    driver.implicitly_wait(5)
    
    title = driver.find_element(By.ID, "above-the-fold").find_element(By.ID, "title").find_element(By.TAG_NAME, "yt-formatted-string").get_attribute("title")
    title = title.replace("/", "_slash_")
    title = title.replace("\\", "_back_slash_")
    
    ydl_opts = {
        "http_headers": {"User-Agent": ua_str},
        "noplaylist": True,
        "outtmpl": title,
        "sleep_interval_requests": 0.75,
        "sleep_interval": 10,
        "max_sleep_interval": 20,
        "ratelimmit": 50000,
    }
    if (audio_only):
        ydl_opts.update({
            "format": "m4a/bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "opus",
            }]
        })
    if (proxy):
        ydl_opts["proxy"] = proxy

    with YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)
    
def download_album(url: str, audio_only: bool=True, proxy: str=""):
    #options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    #driver = webdriver.Chrome(options=options)
    #driver.get(url)
    #driver.implicitly_wait(5)
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    # Enable proxy if provided
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")

    # Disable automation indicator WebDriver flags
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Assign a random user-agent string
    response = requests.get("https://www.useragents.me/", timeout=10)
    response.raise_for_status()
    textarea = BeautifulSoup(response.text, "html.parser").select_one(
        "#most-common-desktop-useragents-json-csv textarea"
    )
    if not textarea:
        raise RuntimeError("Could not find json")
    ua_json = json.loads(textarea.text)
    ua_str = ua_json[random.randint(0, len(ua_json)-1)]["ua"]
    
    # Init driver
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": ua_str})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
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

    ydl_opts = {}
    if (audio_only):
        ydl_opts = {
            "format": "m4a/bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "opus",
            }],
            "noplaylist": True,
        }
    else:
        ydl_opts = {
            "noplaylist": True,
        }
    if (proxy):
        ydl_opts["proxy"] = proxy 

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

