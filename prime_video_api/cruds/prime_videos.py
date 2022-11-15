import time
from typing import List
from prime_video_api.schemas import prime_videos as prime_videos_schema
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

async def search_videos(keyword: str) -> List[prime_videos_schema.Video]:
  url = f'https://www.amazon.co.jp/s?k={keyword}&i=instant-video'
  options = Options()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-gpu')
  options.add_argument("--disable-dev-shm-usage")

  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  wait = WebDriverWait(driver=driver, timeout=15)

  driver.get(url)
  wait.until(EC.presence_of_all_elements_located)
  html = driver.page_source.encode('utf-8')
  soup = BeautifulSoup(html, 'html.parser')
  elements = soup.find_all('a', class_='a-link-normal s-no-outline')
  videos = []
  for element in elements:
    data = {
      'title': element.contents[0].contents[0].attrs['alt'], 
      'url': 'https://www.amazon.co.jp' + element.attrs['href'],
      'image': element.contents[0].contents[0].attrs['src']
    }
    videos.append(data)

  time.sleep(5)
  driver.close()
  return videos

async def get_video_info(getVideoInfoDto: prime_videos_schema.GetVideoInfoDto) -> prime_videos_schema.VideoInfo:
  options = Options()
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
  leaving_schedule = soup.find('div', class_='NgssYl zNwind _2IIDsE av-playback-messages')
  is_leaving_soon = False if leaving_schedule is None else True

  driver.close()

  return {
    'is_available': is_available,
    'is_leaving_soon': is_leaving_soon,
  }

async def get_leaving_soon_videos() -> prime_videos_schema.LeavingSoonVideos:
  options = Options()
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