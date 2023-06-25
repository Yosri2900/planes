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
    self.set_window_size(800, 800)
