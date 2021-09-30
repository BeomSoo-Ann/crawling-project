import os
import time
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


youtube_url = "https://www.youtube.com/results?search_query="
youtube_basic_url = "https://www.youtube.com"


def format_keys(keyword):
    return keyword.replace(" ", "+")


def get_youtube_url(keyword):
    os.system("clear")

    driver = webdriver.Chrome(
        "/Users/annbeomsu/projects/pythonproject/project2021/webcrawling/chromedriver")
    driver.get(f'{youtube_url}{format_keys(keyword)}')
    time.sleep(10.0)
    end_k = 5

    while end_k:
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(3)
        end_k -= 1

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    html = soup.select('ytd-video-renderer>div>div>div>div>h3>a')
    img_vid = soup.select(
        'ytd-video-renderer>div>ytd-thumbnail>a>yt-img-shadow>img')

    keyurl_list = []
    name_list = []
    thumb_list = []

    for href in html:

        if href.get('href')[:7] != '/watch?':
            pass

        else:
            name_list.append(href.get_text())
            keyurl_list.append(youtube_basic_url + href.get('href'))

    for src in img_vid:

        if src.get('src') == None:
            thumb_list.append('No Image')

        else:
            thumb_list.append(src.get('src'))

    youtubeDic = {
        '썸네일': thumb_list,
        '제목': name_list,
        '주소': keyurl_list
    }

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    youtubeDf = pd.DataFrame(youtubeDic)

    youtubeDf.to_csv(f'{keyword} monitoring.csv',
                     mode='a', encoding='utf-8-sig')

    return
