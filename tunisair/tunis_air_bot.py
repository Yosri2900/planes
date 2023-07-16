import tunisair.constants as const
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select


class TunisairBot(uc.Chrome):
  teardown = False

  def __init__(self, trip_type: str = "Round-trip"):
    self.options = webdriver.ChromeOptions()
    self.options.add_argument('proxy-server=106.122.8.54.3128')
    self.trip_type = trip_type
    # self.options.add_experimental_option('detach', True)
    # not sure how to handle the options for now
    super(TunisairBot, self).__init__(options=self.options)
    self.get(const.TUNISAIR_HOME_PAGE)
    self.set_window_size(800, 600)
    sleep(2)

  def scrape(self):

    if self.trip_type == "Round-trip":
      self.scrape_round_trip(from_date="17/08", to_date="26/09")

    elif self.trip_type == "One-way":
      self.scrape_one_way_trip(start_airport="YUL", to_airport="TUN", from_date="26/08")

    elif self.trip_type == "Multi-city/Stopover":
      print("TODO")
      self.scrape_multi_city_trip()

  def scrape_round_trip(self, from_location:str =None, to_location:str =None, from_date:str =None, to_date: str=None):
    self.find_element(By.XPATH, '//*[@id="lignesearch"]/input[2]').click()
    # This option can later be specified by the user
    from_location = "Montreal"
    to_location = "Tunis"
    # sleep(0.3)
    WebDriverWait(self, 3).until(
      Ec.presence_of_element_located((By.CSS_SELECTOR, 'select[id="input_list_res"]'))
    )
    fdd = Select(self.find_element(By.CSS_SELECTOR, 'select[id="input_list_res"]'))
    fdd.select_by_visible_text(from_location)

    # WebDriverWait(self, 3).until(
    #   Ec.presence_of_element_located((By.CSS_SELECTOR, 'select[name=E_LOCATION_1]'))
    # )
    tdd = Select(self.find_element(By.CSS_SELECTOR, 'select[name=E_LOCATION_1]'))
    tdd.select_by_visible_text(to_location)
    sleep(0.2)

    self.find_element(By.CSS_SELECTOR, 'input[id=f_depart]').send_keys("17/08/2023")
    sleep(0.1)
    self.find_element(By.CSS_SELECTOR, 'input[id=f_inbound]').send_keys("17/08/2023")
    sleep(0.1)
    self.find_element(By.CSS_SELECTOR, 'a[class=calendarOKButton]').click()
    sleep(0.1)
    self.find_element(By.CSS_SELECTOR, 'input[value=valider]').click()
    print('done!')

    # for i in range(1, 61):
    #   xpath = f'//*[@id="input_list_res"]/option[{i}]'
    #   name = self.find_element(By.XPATH, xpath).text
    #   value = self.find_element(By.XPATH, xpath).get_attribute('value')
    #   print(f'"{value}" "{name}" "{xpath}"', end="\n")
