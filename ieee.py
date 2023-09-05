#导入库
import os
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import re
import urllib.parse
import time
import random
# import pdfkit
import subprocess
import pandas as pd
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import shutil
import json

start = 2008
end = 2024
journal_name = "IEEE Transactions on Power Electronics"
# download_path = 'C:\\Users\\c50034984\\Downloads'
paper_path = 'C:\\Users\\c50034984\\Desktop\\IEEE-main\\IEEE_papers'

for y in range(end - start + 1):
    year = y + start
    driver = webdriver.Chrome('chromedriver.exe') #, options=opt
    driver.get(url="https://ieeexplore.ieee.org/search/advanced")
    driver.maximize_window()  #浏览器最大化
    #-----------------------------------------------------------------------------------------------------------------------
    time.sleep(30)
    driver.find_elements_by_xpath('//*[@id="xplMainContentLandmark"]/div/xpl-advanced-search/div[2]/div[1]/xpl-advanced-search-advanced/div/div[2]/form/div[1]/div[1]/div[1]/div/div/input')[0].send_keys(journal_name)
    s = Select(driver.find_elements_by_xpath('/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-advanced-search/div[2]/div[1]/xpl-advanced-search-advanced/div/div[2]/form/div[1]/div[1]/div[2]/div/select')[0])  # 实例化Select
    s.select_by_value('5: Publication Title')
    #-----------------------------------------------------------------------------------------------------------------------
    current_position = 0
    page_height = driver.execute_script("return document.body.scrollHeight")
            # 设置滚动步长和间隔时间（可以根据需要进行调整）
    scroll_step = 500  # 每次滚动的像素步长
    scroll_interval = 1  # 每次滚动的时间间隔（秒）
    while current_position < page_height:
        # 滚动到当前位置 + 滚动步长
        driver.execute_script(f"window.scrollTo(0, {current_position + scroll_step});")
        current_position += scroll_step
        time.sleep(scroll_interval)
    time.sleep(10)
    #-----------------------------------------------------------------------------------------------------------------------
    driver.find_elements_by_xpath('/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-advanced-search/div[2]/div[1]/xpl-advanced-search-advanced/div/div[2]/form/div[4]/button[2]')[0].click()
    time.sleep(30)
    driver.find_elements_by_xpath('//*[@id="xplMainContent"]/div[2]/div[1]/xpl-facets/section/ul/li[1]/section/div[1]/xpl-nouislider-facet/span/span[3]/span[2]/span[1]/input')[0].clear()
    driver.find_elements_by_xpath('//*[@id="xplMainContent"]/div[2]/div[1]/xpl-facets/section/ul/li[1]/section/div[1]/xpl-nouislider-facet/span/span[3]/span[2]/span[1]/input')[0].send_keys(year)
    driver.find_elements_by_xpath('//*[@id="xplMainContent"]/div[2]/div[1]/xpl-facets/section/ul/li[1]/section/div[1]/xpl-nouislider-facet/span/span[3]/span[2]/span[2]/input')[0].clear()
    driver.find_elements_by_xpath('//*[@id="xplMainContent"]/div[2]/div[1]/xpl-facets/section/ul/li[1]/section/div[1]/xpl-nouislider-facet/span/span[3]/span[2]/span[2]/input')[0].send_keys(year)
    #-----------------------------------------------------------------------------------------------------------------------
    current_position = 0
    page_height = driver.execute_script("return document.body.scrollHeight")
            # 设置滚动步长和间隔时间（可以根据需要进行调整）
    scroll_step = 500  # 每次滚动的像素步长
    scroll_interval = 1  # 每次滚动的时间间隔（秒）
    while current_position < page_height:
        # 滚动到当前位置 + 滚动步长
        driver.execute_script(f"window.scrollTo(0, {current_position + scroll_step});")
        current_position += scroll_step
        time.sleep(scroll_interval)
    time.sleep(10)
    #-----------------------------------------------------------------------------------------------------------------------
    driver.find_elements_by_xpath('//*[@id="Year-apply-btn"]')[0].click()
    time.sleep(120)
    try:
        try:
            str = driver.find_elements_by_xpath('/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]/span[2]')[0].text
        except Exception as e:
            print('str error!')
            str = driver.find_elements_by_xpath('/html/body/div[6]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]/span[2]')[0].text
        nums = str.split(',')
        len_nums = len(nums)
        res = 0
        for i in range(len_nums):
            res = (1000 * res + int(nums[i]))
        if res % 25 == 0:
            pages = int(res / 25)
        else :
            pages = int(res / 25) + 1

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_experimental_option('prefs', {
        "download.default_directory": f"{paper_path}\\{journal_name}\\{year}", #Change default directory for downloads
        "download.prompt_for_download": False, #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True, #It will not show PDF directly in chrome,
        })
        if not os.path.exists(f"{paper_path}\\{journal_name}\\{year}"):
            os.makedirs(f"{paper_path}\\{journal_name}\\{year}")
        save_path = f"{paper_path}\\{journal_name}\\{year}"
        for page in range(pages - 1):
            for i in range(25):
                try:
                    ul = driver.find_elements_by_xpath('/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[2]/div[2]/xpl-results-list/div[9]/xpl-results-item/div[1]/div[2]/ul')[0]
                    paper_name = driver.find_elements_by_xpath(f'/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[2]/div[2]/xpl-results-list/div[{3 + i}]/xpl-results-item/div[1]/div[1]/div[2]/h3/a')[0].text
                    pdf_url = driver.find_elements_by_xpath(f'/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[2]/div[2]/xpl-results-list/div[{3 + i}]/xpl-results-item/div[1]/div[2]/ul/li[{len(ul.find_elements_by_xpath("li")) - 1}]/xpl-view-pdf/div/div/a')[0].get_attribute("href")
                    driver1 = webdriver.Chrome('chromedriver.exe', options=options) #, options=opt
                    driver1.get(url=pdf_url)
                    driver1.switch_to.frame(driver1.find_elements_by_xpath('/html/body/iframe')[0])
                    driver1.find_elements_by_xpath('/html/body/div/div/a')[0].click()
                    timeout = 180
                    while(not os.path.exists(f"{paper_path}\\{journal_name}\\{year}\\{paper_name.replace(' ', '_').replace('/', '_').replace(': ', '_').replace(':', '_') + '.pdf'}") and  timeout > 0):
                        time.sleep(1)
                        timeout -= 1
                    driver1.quit()
                except Exception as e1:
                    print("retry!")
                    try:
                        ul = driver.find_elements_by_xpath('/html/body/div[6]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[2]/div[2]/xpl-results-list/div[9]/xpl-results-item/div[1]/div[2]/ul')[0]
                        paper_name = driver.find_elements_by_xpath(f'/html/body/div[6]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[2]/div[2]/xpl-results-list/div[{3 + i}]/xpl-results-item/div[1]/div[1]/div[2]/h3/a')[0].text
                        pdf_url = driver.find_elements_by_xpath(f'/html/body/div[6]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[2]/div[2]/xpl-results-list/div[{3 + i}]/xpl-results-item/div[1]/div[2]/ul/li[{len(ul.find_elements_by_xpath("li")) - 1}]/xpl-view-pdf/div/div/a')[0].get_attribute("href")
                        driver1 = webdriver.Chrome('chromedriver.exe', options=options) #, options=opt
                        driver1.get(url=pdf_url)
                        driver1.switch_to.frame(driver1.find_elements_by_xpath('/html/body/iframe')[0])
                        driver1.find_elements_by_xpath('/html/body/div/div/a')[0].click()
                        timeout = 180
                        while(not os.path.exists(f"{paper_path}\\{journal_name}\\{year}\\{paper_name.replace(' ', '_').replace('/', '_').replace(': ', '_').replace(':', '_') + '.pdf'}") and  timeout > 0):
                            time.sleep(1)
                            timeout -= 1
                        driver1.quit()
                    except Exception as e2:
                        print("failed!")
            print(page + 2)
            current_position = 0
            page_height = driver.execute_script("return document.body.scrollHeight")
            # 设置滚动步长和间隔时间（可以根据需要进行调整）
            scroll_step = 500  # 每次滚动的像素步长
            scroll_interval = 1  # 每次滚动的时间间隔（秒）
            while current_position < page_height:
                # 滚动到当前位置 + 滚动步长
                driver.execute_script(f"window.scrollTo(0, {current_position + scroll_step});")
                current_position += scroll_step
                time.sleep(scroll_interval)
            next_btn = driver.find_element_by_class_name(f'stats-Pagination_arrow_next_{page + 2}').click()
            time.sleep(10)
        time.sleep(10)
    except Exception as e:
        print("no paper!")
        continue
    time.sleep(600)
    driver.quit()
