import argparse, logging
from pytube import YouTube
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.request, time
from selenium import webdriver
import pandas as pd
import os
import webbrowser

def get_url_from_query(query):
    return "https://www.youtube.com/results?search_query=%s" % query

def get_destination():
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '/videos')
    return path

def check_existed(video):
    path = get_destination()
    for file in os.listdir(path):
        if video in file:
            return True
    return False

def get_video_path(video):
    path = get_destination()
    for file in os.listdir(path):
        if video in file:
            path = os.path.join(path, file)
            return path
    return None

def run(query):
    destination = get_destination()

    path = os.path.dirname(os.path.realpath(__file__))
    print(path)
    url = get_url_from_query(query)
    print("Loading web driver")
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--disable-popup-blocking')
    driver = webdriver.Chrome(executable_path='%s/chromedriver' % (path))
    print("Loading the url contains query")
    driver.get(url)
    driver.minimize_window()
    # results = driver.find_elements_by_xpath('//*[@class="style-scope ytd-video-renderer"]')
    results = driver.find_elements_by_xpath('//*[@id="contents"]')[1]
    x = results.find_elements_by_xpath('.//*[@id="dismissable"]')
    for _ in x:
        xa = _.find_element_by_xpath('.//*[@id="thumbnail"]').get_attribute('href')
        xy = _.find_element_by_xpath('.//*[@id="video-title"]').get_attribute('aria-label')
        print('%d. %s %s' % (x.index(_), xa, xy))

    n = int(input('Choose one link to open in Google Chrome: '))
    link = x[n].find_element_by_xpath('.//*[@id="thumbnail"]').get_attribute('href')
    driver.close()
    # # Just open in Google Chrome
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    # chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(link)

    # Wants to download? Uncomment the code below :))

    # try:
    #     yt = YouTube(link)
    # except:
    #     print("Connection error")

    # # video = yt.filter('mp4')
    # video = yt.streams.filter(subtype='mp4', type='video', progressive=True).order_by('res').desc().first()

    # if check_existed(video.title):
    #     # extension = get_extension(video.title)
    #     audio_link_generator = get_video_path(video.title)
    #     # print(audio_link_generator)
    #     chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    #     webbrowser.get(chrome_path).open(audio_link_generator)
    # else:
    #     try:
    #         print("Downloading the audio of video")
    #         video.download(destination)
    #     except:
    #         print("Download error")
    #     print("Video is downloaded")
    #     audio_link_generator = get_video_path(video.title)
    #     chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    #     webbrowser.get(chrome_path).open(audio_link_generator)
    # driver.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search', default='death bed', type=str, help="Search term")
    args = parser.parse_args()
    run(args.search)

if __name__ == '__main__':
    main()