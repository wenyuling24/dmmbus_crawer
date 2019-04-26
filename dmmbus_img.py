#!/usr/bin/env python
# coding=utf-8

import os
import time
import threading
from multiprocessing import Pool, cpu_count

import requests
from bs4 import BeautifulSoup
import sys

from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')
HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "https://www.dmmbus.us"
}

DIR_PATH = r"E:\dmmbus"  # 下载图片保存路径


def create_folder(path, name):
    # 创建文件夹
    folder_path = os.path.join(path, name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def save_pic(pic_src, pic_title):
    """
    将图片下载到本地文件夹
    """
    try:
        img = requests.get(pic_src, headers=HEADERS, timeout=10)
        img_name = pic_title + ".jpg"
        with open(img_name, 'ab') as f:
            f.write(img.content)
            print(img_name)
    except Exception as e:
        print(e)


# 写文件
def save_file(title, text):
    try:
        file_name = title.replace('\n', '').replace('\t', '').replace(' ', '') + '.txt'
        with open(file_name.decode('utf-8'), 'w') as f:
            f.write(text)
    except Exception as e:
        print e


def make_dir(folder_name):
    """
    新建套图文件夹并切换到该目录下
    """
    path = os.path.join(DIR_PATH, folder_name)
    # 如果目录已经存在就不用再次爬取了，去重，提高效率。存在返回 False，否则反之
    if not os.path.exists(path):
        os.makedirs(path)
        print(path)
        os.chdir(path)
        return True
    print("Folder has existed!")
    return False


def delete_empty_dir(save_dir):
    """
    如果程序半路中断的话，可能存在已经新建好文件夹但是仍没有下载的图片的
    情况但此时文件夹已经存在所以会忽略该套图的下载，此时要删除空文件夹
    """
    if os.path.exists(save_dir):
        if os.path.isdir(save_dir):
            for d in os.listdir(save_dir):
                path = os.path.join(save_dir, d)  # 组装下一级地址
                if os.path.isdir(path):
                    delete_empty_dir(path)  # 递归删除空文件夹
        if not os.listdir(save_dir):
            os.rmdir(save_dir)
            print("remove the empty dir: {}".format(save_dir))
    else:
        print("Please start your performance!")  # 请开始你的表演


def selenium_request(url):
    # C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe
    browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    # browser.maximize_window()  # 浏览器窗口最大化
    browser.get(url)
    return browser.page_source


def urls_crawler(url):
    """
    爬虫入口，主要爬取操作
    """
    try:
        # 获取目标地址的html结构文档
        html_doc = requests.get(url, headers=HEADERS, timeout=10).text
        # 解析html
        folder_name = BeautifulSoup(html_doc, 'lxml')
        waterfall = folder_name.find('div', id='waterfall')
        all_waterfall_box = waterfall.find_all('a')
        for water_item in all_waterfall_box:
            href = water_item.get('href')
            img = water_item.find('img')
            img_title = img.get('title')
            title = water_item.find('date').text
            print href
            print img_title
            print title
            if make_dir(title):

                # 这里进入第二级界面
                # https://www.dmmbus.us/SSNI-473
                # html_doc = requests.get(href, headers=HEADERS, timeout=10).text
                html_doc = selenium_request(href)
                # print html_doc
                second_folder_name = BeautifulSoup(html_doc, 'lxml')
                # # 获得磁力链接
                movie_table = second_folder_name.find('table', id='magnet-table')
                movie_box = movie_table.find_all('a')
                # print movie_box
                for movie_item in movie_box:
                    movie_href = movie_item.get('href')
                    print movie_href
                    movie_size = movie_item.text
                    print movie_size
                    save_file(movie_size, movie_href)
                    break

                # 获得樣品圖像
                h4_box = second_folder_name.find_all('h4')
                for h4_item in h4_box:
                    h4_item_string = h4_item.text
                    if '樣品圖像' == h4_item_string:
                        row_movie = second_folder_name.find('div', class_='row movie')
                        img = row_movie.find('img')
                        sec_img_url = img.get('src')
                        sec_img_title = img.get('title')
                        # 保存封面图
                        save_pic(sec_img_url, sec_img_title)
                        sample_waterfall = second_folder_name.find('div', id='sample-waterfall')
                        all_sample_box = sample_waterfall.find_all('a')
                        for sample_item in all_sample_box:
                            href = sample_item.get('href')
                            pic_title = sample_item.find('img').get('title')
                            # 保存大图
                            save_pic(href, pic_title)
                        break
    except Exception as e:
        print('Exception: ' + e)


if __name__ == "__main__":
    urls = ['https://www.dmmbus.us/page/{cnt}'.format(cnt=cnt)
            for cnt in range(1, 2)]
    pool = Pool(processes=cpu_count())
    try:
        delete_empty_dir(DIR_PATH)
        pool.map(urls_crawler, urls)

    except Exception:
        time.sleep(30)
        delete_empty_dir(DIR_PATH)
        pool.map(urls_crawler, urls)
