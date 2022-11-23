import time
import random
from typing import List
from prime_video_api.schemas import prime_videos as prime_videos_schema
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

user_agent = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
]

async def search_videos(keyword: str) -> List[prime_videos_schema.Video]:
  UA = user_agent[random.randrange(0, len(user_agent), 1)]
  options = Options()
  options.add_argument('--user-agent=' + UA)
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-gpu')
  options.add_argument("--disable-dev-shm-usage")

  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  wait = WebDriverWait(driver=driver, timeout=15)

  url = f'https://www.amazon.co.jp/s?k={keyword}&i=instant-video'
  driver.get(url)
  wait.until(EC.presence_of_all_elements_located)
  html = driver.page_source.encode('utf-8')
  soup = BeautifulSoup(html, 'html.parser')
  elements = soup.find_all('div', class_='a-section a-spacing-base')
  videos = []
  for element in elements:
    video_info = element.find('a', class_='a-link-normal s-no-outline')
    available = element.find('div', class_='a-section a-spacing-none a-spacing-top-mini')
    data = {
      'title': video_info.contents[0].contents[0].attrs['alt'], 
      'url': 'https://www.amazon.co.jp' + video_info.attrs['href'],
      'image': video_info.contents[0].contents[0].attrs['src'],
      'is_available': False if available is None else True
    }
    videos.append(data)

  driver.close()
  return videos

async def search_videos_v2(keyword: str) -> List[prime_videos_schema.Video]:
  UA = user_agent[random.randrange(0, len(user_agent), 1)]
  options = Options()
  options.add_argument('--user-agent=' + UA)
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-gpu')
  options.add_argument("--disable-dev-shm-usage")

  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  wait = WebDriverWait(driver=driver, timeout=15)

  driver.get('https://www.amazon.co.jp/Amazon-Video/b/?ie=UTF8&node=2351649051&ref_=nav_cs_prime_video')
  wait.until(EC.presence_of_all_elements_located)
  time.sleep(3)
  search_bar = driver.find_element(By.ID, 'twotabsearchtextbox')
  search_bar.send_keys(keyword)
  search_bar.submit()
  wait.until(EC.presence_of_all_elements_located)
  html = driver.page_source.encode('utf-8')
  soup = BeautifulSoup(html, 'html.parser')
  elements = soup.find_all('div', class_='a-section a-spacing-base')
  videos = []
  for element in elements:
    video_info = element.find('a', class_='a-link-normal s-no-outline')
    available = element.find('div', class_='a-section a-spacing-none a-spacing-top-mini')
    data = {
      'title': video_info.contents[0].contents[0].attrs['alt'], 
      'url': 'https://www.amazon.co.jp' + video_info.attrs['href'],
      'image': video_info.contents[0].contents[0].attrs['src'],
      'is_available': False if available is None else True
    }
    videos.append(data)

  driver.close()
  return videos

async def get_video_info(getVideoInfoDto: prime_videos_schema.GetVideoInfoDto) -> prime_videos_schema.VideoInfo:
  UA = user_agent[random.randrange(0, len(user_agent), 1)]
  options = Options()
  options.add_argument('--user-agent=' + UA)
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-gpu')
  options.add_argument("--disable-dev-shm-usage")

  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  wait = WebDriverWait(driver=driver, timeout=15)
  driver.get(getVideoInfoDto.url)
  wait.until(EC.presence_of_all_elements_located)

  html = driver.page_source.encode('utf-8')
  soup = BeautifulSoup(html, 'html.parser')
  available_button = soup.find('a', class_='SPqQmU _3RF4FN _1D7HW3 _1c8faI _3cSKlv _1ITy4O dv-signup-button')
  is_available = False if available_button is None else True
  leaving_schedule = soup.find('span', class_='_36qUej _1jE1N6')
  is_leaving_soon = False if leaving_schedule is None else True

  driver.close()

  return {
    'is_available': is_available,
    'is_leaving_soon': is_leaving_soon,
  }

async def get_leaving_soon_videos() -> prime_videos_schema.LeavingSoonVideos:
  UA = user_agent[random.randrange(0, len(user_agent), 1)]
  options = Options()
  options.add_argument('--user-agent=' + UA)
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-gpu')
  options.add_argument("--disable-dev-shm-usage")

  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  wait = WebDriverWait(driver=driver, timeout=15)

  url = 'https://www.amazon.co.jp/gp/video/search/ref=atv_cat_leaving_soon_quest?phrase=%E3%82%82%E3%81%86%E3%81%99%E3%81%90%E9%85%8D%E4%BF%A1%E7%B5%82%E4%BA%86&queryToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOmZhbHNlLCJwdCI6ImJyb3dzZSIsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoiYmJuPTQyMTc1MjAwNTEmc2VhcmNoLWFsaWFzPWluc3RhbnQtdmlkZW8mbm9kZT00MjE3NTIwMDUxJnBfbl93YXlzX3RvX3dhdGNoPTM3NDYzMzAwNTEiLCJ0eHQiOiLjgoLjgYbjgZnjgZDphY3kv6HntYLkuoYiLCJvZmZzZXQiOjAsIm5wc2kiOjMwfQ%3D%3D&ie=UTF8&pageId=default&queryPageType=browse'
  driver.get(url)
  wait.until(EC.presence_of_all_elements_located)

  winHeight = driver.execute_script("return window.innerHeight")
  lastTop = 1

  while True:
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    top = lastTop

    while top < lastHeight:
      top += int(winHeight * 0.8)
      driver.execute_script("window.scrollTo(0, %d)" % top)
      time.sleep(1)

    time.sleep(1)
    newLastHeight = driver.execute_script("return document.body.scrollHeight")

    if lastHeight == newLastHeight:
      break

    lastTop = lastHeight
  
  html = driver.page_source.encode('utf-8')
  soup = BeautifulSoup(html, 'html.parser')
  leaving_soon_elements = soup.find_all('a', class_='av-beard-title-link')
  videos: List[str] = []
  for element in leaving_soon_elements:
    videos.append(element.get_text())

  driver.close()

  return {
    'videos': videos
  }