import selenium
import time
import sys
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

link = "https://www.facebook.com/alexander.zakharin?__tn__=,d-]-h-R&eid=ARDFa9K8zzPXzVRgLoOukJqPfr0JdOCn8vq_wuxZjV7XJYdCuaDEWjyH4aaw3Xygd5NmMBkW5fGnISSS"
con = requests.get(link).content
soup = BeautifulSoup(con, "html")
print(soup)


usr = ""
pwd = ""

usr_agents = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
]


opts = Options()
opts.add_argument("user-agent=" + random.choice(usr_agents))
opts.add_argument("--disable-notifications")
driver = webdriver.Chrome(executable_path="/Users/dimatimohin/bin/chromedriver", options=opts)
print(opts, driver)
driver.get(link)
a = driver.page_source  # получение html кода
soup = BeautifulSoup(a, "html.parser") # суп

username = login"
password = "password"
driver.get('https://www.facebook.com/')
UN = driver.find_element_by_id('email')
UN.send_keys(username)
PS = driver.find_element_by_id('pass')
PS.send_keys(password)
LI = driver.find_element_by_id('loginbutton')
LI.click()
driver.get(link)




print(1234)
print(a)
time.sleep(1)


print(" - " * 1000)

for i in range(0):
    SCROLL_PAUSE_TIME = 0.5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
time.sleep(1)


link = "https://www.facebook.com/alexander.zakharin?__tn__=,d-]-h-R&eid=ARDFa9K8zzPXzVRgLoOukJqPfr0JdOCn8vq_wuxZjV7XJYdCuaDEWjyH4aaw3Xygd5NmMBkW5fGnISSS"
con = requests.get(link).content
soup = BeautifulSoup(con, "html")
# print(soup)
print("--" * 100)
#parametrs



name = soup.find("a", {"class": "_2nlw _2nlv"}).get_text()  #имя пользователя
lives = soup.find("div", {"class": "_42ef"}).get_text()[:-16]
lived = soup.find("div", {"class": "_50f3"})
print(lived)
