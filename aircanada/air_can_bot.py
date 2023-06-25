import undetected_chromedriver
import aircanada.constants as const
import time
import undetected_chromedriver as uc
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


class AirCanBot(uc.Chrome):
  teardown = False

  def __init__(self):
    self.options = webdriver.ChromeOptions()
    self.options.add_argument('proxy-server=106.122.8.54.3128')
    # self.options.add_experimental_option('detach', True)
    # not sure how to handle the options for now
    super(AirCanBot, self).__init__(options=self.options)

  def scrape_home_page(self):
    self.get(const.AIR_CANADA_HOME_PAGE)
    self.set_window_size(800, 600)
    time.sleep(2)
    self.select_destinations()

  def select_destinations(self, start: str = None, to: str = None):
    # from_location1 = WebDriverWait(self, 5).until(
    #   EC.presence_of_element_located((By.XPATH, '//*[@id="bkmgFlights_origin_trip_1"]'))
    # )
    from_location = WebDriverWait(self, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="bkmgFlights_origin_trip_1"]'))
    )
    from_location.clear()
    from_text = "Montr"
    for char in from_text:
      from_location.send_keys(char)
      # driver.implicitly_wait(0.5)
      time.sleep(0.5)
    self.execute_script("window.scrollTo(0, 700)")
    self.maximize_window()
    time.sleep(0.2)
    # WebDriverWait(self, 30).until(
    #   EC.presence_of_element_located((By.XPATH, '//*[@id="bkmgFlights_origin_trip_1SearchResult1"]'))
    # ).click()
    self.find_element(By.XPATH, '//*[@id="bkmgFlights_origin_trip_1SearchResult1"]').click()

    to_location = WebDriverWait(self, 30).until(
      EC.presence_of_element_located((By.XPATH, '//*[@id="bkmgFlights_destination_trip_1"]'))
    )
    to_location.clear()
    to_text = "Tuni"
    for char in to_text:
      to_location.send_keys(char)
      # driver.implicitly_wait(0.5)
      time.sleep(0.5)
    time.sleep(0.2)
    self.implicitly_wait(2)
    self.find_element(By.XPATH, '//*[@id="bkmgFlights_destination_trip_1SearchResult0"]/abc-ripple/div').click()
    time.sleep(2)

    # while True:
    #   pass
