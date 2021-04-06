from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser

import datetime, re, requests, io, time, random, string
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

PATH = "./chromedriver"

option = webdriver.ChromeOptions()
option.add_argument('headless')

# driver = webdriver.Chrome('path/to/chromedriver',options=option)

def testing():
    return 'tested successfully'

# Create dict with name:links for job searches from linkedin site
def job_quick_search():
    driver = webdriver.Chrome(PATH, options=option)
    driver.get('https://linkedin.com')
    driver.find_element_by_xpath('//*[@id="main-content"]/section[2]/div/div[2]/div/div/label[1]/span[1]').click()
    time.sleep(.5)
    content = driver.find_element_by_xpath('//*[@id="main-content"]/section[2]/div/div[2]/div').get_attribute('innerHTML')
    recommended_search = BeautifulSoup(content, 'lxml')
    result_list = recommended_search.find_all('a')
    driver.close()
    search_list = {}
    for t in result_list:
        temp = t.text
        temp = temp.replace(' ','')
        temp = temp.replace('\n','')
        search_list[temp] = t.attrs['href']
    return search_list

# job_search_list = job_quick_search()

def get_job_search(field = 'Engineering'):
    job_search_list = job_quick_search()
    driver = webdriver.Chrome(PATH, options=option)
    driver.get(job_search_list[field])
    time.sleep(.5)
    jobs_search = driver.find_element_by_xpath('//*[@id="main-content"]/div/section[2]/ul').get_attribute('innerHTML')
    search_content = BeautifulSoup(jobs_search, 'lxml')
    jobs_title = search_content.find_all('h3') # get the title - stored in h3
    jobs_comp = search_content.find_all('h4') # get the company name - in h4
    driver.close()
    jobs = {}
    x = len(search_content.find_all('a'))
    y=0
    i=0
    job_link_list = []
    while i < x:
        temp = search_content.find_all('a')[i].attrs['href']
        if "com/jobs" in temp:
            job_link_list.append(temp)
        i += 1
    for job in jobs_title:
        temp = job.text
        jobs[temp] = [jobs_comp[y].text, job_link_list[y]]
        y+=1
    return jobs


def the_detail(the_link):
    driver = webdriver.Chrome(PATH, options=option)
    driver.get(the_link)
    time.sleep(1)
    # driver.find_element_by_xpath('//*[@id="main-content"]/section[1]/section[3]/div/section/button[1]').click()
    content = driver.find_element_by_xpath('//*[@id="main-content"]/section[1]/section[3]').get_attribute('innerHTML')
    content2 = driver.find_element_by_xpath('//*[@id="main-content"]/section[1]/section[3]/div/section/div').get_attribute('innerHTML')
    data = BeautifulSoup(content,'html.parser')
    data2 = BeautifulSoup(content2,'html.parser').text
    driver.close()
    return data

