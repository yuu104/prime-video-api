import time
from typing import List
from prime_video_api.schemas import prime_videos as prime_videos_schema
import chromedriver_binary # noqa
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

async def search_videos(keyword: str) -> List[prime_videos_schema.Video]:
  url = f'https://www.amazon.co.jp/s?k={keyword}&i=instant-video'
  options = Options()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-gpu')
  options.add_argument("--disable-dev-shm-usage")
  driver = webdriver.Chrome(options=options)
  driver.get(url)
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
  driver = webdriver.Chrome(options=options)
  driver.get(getVideoInfoDto.url)
  html = driver.page_source.encode('utf-8')
  soup = BeautifulSoup(html, 'html.parser')
  available_button = soup.find('a', class_='SPqQmU _3RF4FN _1D7HW3 _1c8faI _3cSKlv _1ITy4O dv-signup-button')
  is_available = False if available_button is None else True
  leaving_schedule = soup.find('span', class_='_36qUej _1jE1N6')
  is_leaving_soon = False if leaving_schedule is None else True
  time.sleep(5)
  driver.close()
  return {
    'is_available': is_available,
    'is_leaving_soon': is_leaving_soon
  }