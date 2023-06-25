import csv
import httpx
import asyncio
from bs4 import BeautifulSoup
import requests, time
from requests_html import HTMLSession
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

HOME_PAGE = "https://www.aircanada.com/ca/en/aco/home.html"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Accept-Language': 'en'}

if __name__ == '__main__':
  #scraping with selenium
  options = webdriver.ChromeOptions()
  options.add_argument('proxy-server=106.122.8.54.3128')
  # options.add_argument(r'--user-data-dir=C:\Users\yosri\AppData\Local\Google\Chrome\User Data\Default')

  # driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
  driver = uc.Chrome(options=options)
  driver.get(HOME_PAGE)
  driver.set_window_size(800, 600)
  time.sleep(2)

  # -------------------------------------------------------------------------------------------
  # selecting from location
  from_location1 = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="bkmgFlights_origin_trip_1"]'))
  )
  from_location1.clear()
  from_text = "Montr"
  for char in from_text:
    from_location1.send_keys(char)
    # driver.implicitly_wait(0.5)
    time.sleep(0.5)
  scroll_down = driver.execute_script("window.scrollTo(0, 550)")
  driver.maximize_window()
  time.sleep(0.2)
  # driver.implicitly_wait(2)
  driver.find_element(By.XPATH, '//*[@id="bkmgFlights_origin_trip_1SearchResult1"]').click()

  # ------------------------------------------------------------------------------------------
  # selecting to location
  to_location1 = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="bkmgFlights_destination_trip_1"]'))
  )
  to_location1.clear()
  to_text = "Tuni"
  for char in to_text:
    to_location1.send_keys(char)
    # driver.implicitly_wait(0.5)
    time.sleep(0.5)
  time.sleep(0.2)
  driver.implicitly_wait(2)
  driver.find_element(By.XPATH, '//*[@id="bkmgFlights_destination_trip_1SearchResult0"]/abc-ripple/div').click()
  time.sleep(2)
  # ------------------------------------------------------------------------------------------
  #clear dates if possible

  # ------------------------------------------------------------------------------------------
  #selecting from date
  calendar_button = driver.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1-showCalendar"]')
  calendar_button.click()
  time.sleep(2)
  driver.implicitly_wait(2)
  driver.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1_clearDates"]').click()
  driver.implicitly_wait(0.6)

  # June 25
  month_start = driver.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1AbcCalendarDialogBody"]/abc-calendar/div/abc-calendar-month[1]/table/tr[6]/td[6]')
  month_start.click()
  time.sleep(2)
  # print(month_start.get_attribute("data-date"))

  # ------------------------------------------------------------------------------------------
  # selection to date
  # july 30
  month_return = driver.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1AbcCalendarDialogBody"]/abc-calendar/div/abc-calendar-month[2]/table/tr[7]/td[1]')
  month_return.click()
  time.sleep(2)
  # driver.implicitly_wait(2)
  # print(month_start.get_attribute("data-date"))
  select_period = driver.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1_confirmDates"]')
  select_period.click()
  # ------------------------------------------------------------------------------------------
  # number of passengers (2 adults, 1 youth, 1 child, 1 indant on lap, 1 infant in seat)
  # passengers_btn = driver.find_element(By.XPATH, '//*[@id="bkmgFlights_selectTravelers"]')
  # passengers_btn.click()
  # time.sleep(0.1)

  # add_adult = WebDriverWait(driver, 5).until(
  #   EC.element_to_be_clickable((By.XPATH, '//*[@id="bkmgFlights_selectTravelers_addTraveler_ADT"]')))
  # add_adult.click()
  # time.sleep(0.3)

  # add_youth = WebDriverWait(driver, 5).until(
  #   EC.element_to_be_clickable((By.XPATH, '//*[@id="bkmgFlights_selectTravelers_addTraveler_YTH"]')))
  # add_youth.click()
  # time.sleep(0.3)
  #
  # add_child = WebDriverWait(driver, 5).until(
  #   EC.element_to_be_clickable((By.XPATH, '//*[@id="bkmgFlights_selectTravelers_addTraveler_CHD"]')))
  # add_child.click()
  # time.sleep(0.3)
  #
  # add_infant_lap = WebDriverWait(driver, 5).until(
  #   EC.element_to_be_clickable((By.XPATH, '//*[@id="bkmgFlights_selectTravelers_addTraveler_INF"]')))
  # add_infant_lap.click()
  #
  # close_btn = WebDriverWait(driver, 5).until(
  #   EC.element_to_be_clickable((By.XPATH, '//*[@id="bkmgFlights_selectTravelers_confirmTravelers"]')))
  # close_btn.click()


  # xpath for adults: '//*[@id="selectTravelersPanel"]/div[1]/div[1]', + btn: //*[@id="bkmgFlights_selectTravelers_addTraveler_ADT"]
  #xpath for youth: //*[@id="selectTravelersPanel"]/div[1]/div[2], + btn: //*[@id="bkmgFlights_selectTravelers_addTraveler_YTH"]
  #xpath for child: //*[@id="selectTravelersPanel"]/div[1]/div[3], + btn: //*[@id="bkmgFlights_selectTravelers_addTraveler_CHD"]
  #xpath for infant on lap: //*[@id="selectTravelersPanel"]/div[1]/div[4], +btn: //*[@id="bkmgFlights_selectTravelers_addTraveler_INF"]
  #xpath for infant in seat: //*[@id="selectTravelersPanel"]/div[1]/div[5], + btn: //*[@id="bkmgFlights_selectTravelers_addTraveler_INS"]

  # ------------------------------------------------------------------------------------------
  # confirm selection
  time.sleep(0.5)
  confirm_btn = driver.find_element(By.XPATH, '//*[@id="bkmgFlights_findButton"]')
  driver.implicitly_wait(2)
  confirm_btn.click()
  time.sleep(2)
  # ------------------------------------------------------------------------------------------
  # searching results
  # driver.execute_script("window.scrollBy(0, 0)")
  # search_flight = driver.find_element(By.XPATH, '//*[@id="bkmgFlights_findButton"]')
  # search_flight.click()
  # title = WebDriverWait(driver, 30).until(
  #   EC.presence_of_element_located((By.XPATH, '//*[@id="flightBlockMainTitle"]'))
  # )
  # for i in range(10):
  #   driver.execute_script("window.scrollTo(0, 600);")
  #   driver.implicitly_wait(i+1)
  # print(title.text)
  # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  # ------------------------------------------------------------------------------------------
  # driver.implicitly_wait(10)
  # resultSet = WebDriverWait(driver, 10).until(
  #   EC.element_to_be_clickable((By.XPATH, '//*[@id="flightBlockWrapper"]/div[2]/div/ul')))
  # time.sleep(0.1)
  # options = resultSet.find_elements(By.TAG_NAME, 'li')
  # for option in options:
  #   print(option.text)
  while (True):
    pass

  # driver.quit()
