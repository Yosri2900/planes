import csv
import httpx
import asyncio
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession

url = "https://www.aircanada.com/ca/en/aco/home/app.html#/search?org1=YUL&dest1=TUN&orgType1=A&destType1=A&org2=TUN&dest2=YUL&orgType2=A&destType2=A&departure1=29%2F07%2F2023&departure2=28%2F08%2F2023&marketCode=INT&numberOfAdults=3&numberOfYouth=1&numberOfChildren=1&numberOfInfants=0&numberOfInfantsOnSeat=0&tripType=R&isFlexible=false"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) Chrome/114.0.0.0 Safari/537.36'}
session = HTMLSession()
r = session.get(url, headers=headers)
print(r.status_code)
if r.ok:
  r.html.render(sleep=5)
  soup = BeautifulSoup(r.content, 'lxml')
# class_="itinerary-info-ctr itinerary-body large-info-ctr new-purc-itinerary ng-star-inserted"
print(soup.find_all('div', class_='display-on-hover'))
print(soup.prettify())

# with httpx.Client() as s:
#   r = s.get(url, headers=headers)
#   print(r.text)
# -------------------------------------------------------------------------------------------------------------
# trying out selenium
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def get_data(url: str):
  opts = Options()
  opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                    'like Gecko) Chrome/114.0.0.0 Safari/537.36')

  driver = Chrome(options=opts)
  driver.get(url)
  # try:
  #   myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cabinBtnECO30Content"]/div/div/div[2]/div[1]')))
  #   time.sleep(15)
  #   print("Page is ready!")
  # except TimeoutException:
  #   print("Loading took too much time!")
  # finally:
  #   driver.quit()

  myElem = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="cabinBtnECO30Content"]/div/div/div[2]/div[1]')))

if __name__ == '__main__':
  data = get_data(url)
