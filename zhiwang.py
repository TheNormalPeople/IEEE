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

start = 1994
end = 2023
journal_name = "太阳能学报"
download_path = 'C:\\Users\\c50034984\\Downloads'
paper_path = 'D:\\电力数据集'
for y in range(end - start + 1):
    year = y + start
    driver = webdriver.Chrome('chromedriver.exe') #, options=opt
    driver.get(url="http://cnki.huawei.com/kns55/brief/result.aspx")
    s1 = Select(driver.find_element_by_id('year_from'))  # 实例化Select
    s1.select_by_value(str(year))  # 选择value="o2"的项

    s2 = Select(driver.find_element_by_id('year_to'))  # 实例化Select
    s2.select_by_value(str(year))  # 选择value="o2"的项
    
    s3 = Select(driver.find_element_by_id('magazine_special1'))  # 实例化Select
    s3.select_by_value('=')  # 选择value="o2"的项

    driver.find_element_by_id("magazine_value1").send_keys(journal_name)#输入内容
    driver.find_element_by_id("btnSearch").click()#点击该元素
    driver.switch_to_frame('iframeResult')
    time.sleep(2)
    print(driver.find_element_by_name('lastpage').get_attribute('value'))
    page_len = int(driver.find_element_by_name('lastpage').get_attribute('value'))
    for i in range(page_len):
        tr_lens = len(driver.find_elements_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr'))
        links = []
        for j in range(tr_lens - 1):
            link = driver.find_elements_by_xpath(f'//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[{j+2}]/td[2]/a')[0].get_attribute("href")
        #     links.append()
            try:
                driver1 = webdriver.Chrome('chromedriver.exe')
                driver1.get(url=link)
                driver1.find_element(By.LINK_TEXT,'PDF下载').click()   
                time.sleep(4.5)
                driver1.quit()
            except Exception as e:
                print(f"下载失败")
        if i + 1 == page_len:
            driver.quit()
        else:
            driver.find_element(By.LINK_TEXT,'下页').click()   
    file_names = os.listdir(download_path)
    if not os.path.exists(f"{paper_path}\\{journal_name}\\{year}"):
        os.makedirs(f"{paper_path}\\{journal_name}\\{year}")
    for name in file_names:
        shutil.move(f"{download_path}\\{name}", f"{paper_path}\\{journal_name}\\{year}")
