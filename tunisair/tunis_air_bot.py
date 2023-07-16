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
      self.scrape_round_trip(from_date="17/08/2023", to_date="26/09/2023")

    elif self.trip_type == "One-way":
      self.scrape_one_way_trip(from_date="17/08/2023", to_date="26/09/2023")

    elif self.trip_type == "Multi-city/Stopover":
      print("TODO")
      self.scrape_multi_city_trip()

  def scrape_round_trip(self, from_location: str = None, to_location: str = None, from_date: str = None,
                        to_date: str = None):
    self.find_element(By.XPATH, '//*[@id="lignesearch"]/input[2]').click()
    # This option can later be specified by the user
    from_location = "Montreal"
    to_location = "Tunis"
    # sleep(0.3)
    WebDriverWait(self, 3).until(
      Ec.presence_of_element_located((By.CSS_SELECTOR, 'select[id="input_list_res"]'))
    )
    fdd = Select(self.find_element(By.CSS_SELECTOR, 'select[id="input_list_res"]'))
    fdd.select_by_visible_text(const.TUNISAIR_AIRPORT.get(from_location))

    tdd = Select(self.find_element(By.CSS_SELECTOR, 'select[name=E_LOCATION_1]'))
    tdd.select_by_visible_text(const.TUNISAIR_AIRPORT.get(to_location))
    sleep(0.1)

    self.find_element(By.CSS_SELECTOR, 'input[id=f_depart]').send_keys(from_date)
    self.find_element(By.CSS_SELECTOR, 'input[id=f_inbound]').send_keys(to_date)
    self.find_element(By.CSS_SELECTOR, 'a[class=calendarOKButton]').click()
    self.find_element(By.CSS_SELECTOR, 'input[value=valider]').click()

    self.maximize_window()
    warning_message = ''
    try:
      warning_message = WebDriverWait(self, 10).until(
        Ec.presence_of_element_located((By.XPATH, '//*[@id="global-warning-message"]/div/ul/li/span'))
      )
      # print(warning_message.text)
    except TimeoutException:
      print('the warning is not there... TimeOutException')
    except NoSuchElementException:
      print("the warning is not there... NoSuchElementException")

    dtable = self.find_element(By.CSS_SELECTOR, 'table[id=calendar-table-outbound] tbody')
    dtd_tags = dtable.find_elements(By.CLASS_NAME, 'calendarPerBound-fare')
    dinfos = []
    for dtag in dtd_tags:
      # date_section = dtag.find_element(By.CLASS_NAME, 'calendarPerBound-date-section')
      date = dtag.find_element(By.CSS_SELECTOR, 'div.calendarPerBound-date').text.strip()
      month = dtag.find_element(By.CSS_SELECTOR, 'div.calendarPerBound-month').text.strip()
      try:
        price_section = dtag.find_element(By.CSS_SELECTOR, 'div.fare-checkbox-label-content '
                                                           'span.calendarPerBound-price span').text.strip()
        # 'div.fare-checkbox-label-content'
        # 'div.fare-checkbox-label-content span.calendarPerBound-price span'

        dinfos.append({
          'date': date,
          'month': month,
          'price': f'${price_section} USD'
        })
      except NoSuchElementException:
        dinfos.append({
          'date': date,
          'month': month,
          'price': 'NOT AVAILABLE'
        })
        continue
    print(dinfos)
    print('---------------------------Return Tickets---------------------------------')
    rtable = self.find_element(By.CSS_SELECTOR, 'table[id=calendar-table-inbound] tbody')
    rtd_tags = rtable.find_elements(By.CLASS_NAME, 'calendarPerBound-fare')
    rinfos = []
    for rtag in rtd_tags:
      # date_section = rtag.find_element(By.CSS_SELECTOR, 'div.calendarPerBound-date-section '
      #                                                   'div.calendarPerBound-dayOfWeek')
      date = rtag.find_element(By.CSS_SELECTOR, 'div.calendarPerBound-date-section '
                                                'div.calendarPerBound-date').text.strip()
      month = rtag.find_element(By.CSS_SELECTOR, 'div.calendarPerBound-date-section '
                                                 'div.calendarPerBound-month').text.strip()
      try:
        price_section = rtag.find_element(By.CSS_SELECTOR, 'div.fare-checkbox-label-content '
                                                           'span.calendarPerBound-price span').text.strip()
        # 'div.fare-checkbox-label-content'
        # 'div.fare-checkbox-label-content span.calendarPerBound-price span'

        rinfos.append({
          'date': date,
          'month': month,
          'price': f'${price_section} USD'
        })
      except NoSuchElementException:
        rinfos.append({
          'date': date,
          'month': month,
          'price': 'NOT AVAILABLE'
        })
        continue
    print(rinfos)
    if warning_message != '':
      return dinfos, rinfos, warning_message.text

    return dinfos, rinfos

  def scrape_one_way_trip(self, from_location: str = None, to_location: str = None, from_date: str = None,
                          to_date: str = None):
    self.find_element(By.XPATH, '//*[@id="lignesearch"]/input[1]').click()
    # This option can later be specified by the user
    from_location = "Montreal"
    to_location = "Tunis"
    WebDriverWait(self, 3).until(
      Ec.presence_of_element_located((By.CSS_SELECTOR, 'select[id="input_list_res"]'))
    )
    fdd = Select(self.find_element(By.CSS_SELECTOR, 'select[id="input_list_res"]'))
    fdd.select_by_visible_text(const.TUNISAIR_AIRPORT.get(from_location))

    tdd = Select(self.find_element(By.CSS_SELECTOR, 'select[name=E_LOCATION_1]'))
    tdd.select_by_visible_text(const.TUNISAIR_AIRPORT.get(to_location))
    sleep(0.1)

    self.find_element(By.CSS_SELECTOR, 'input[id=f_depart]').send_keys(from_date)
    self.find_element(By.CSS_SELECTOR, 'input[id=f_inbound]').send_keys(to_date)
    self.find_element(By.CSS_SELECTOR, 'a[class=calendarOKButton]').click()
    self.find_element(By.CSS_SELECTOR, 'input[value=valider]').click()
    self.maximize_window()
    warning_message = ''
    try:
      warning_message = WebDriverWait(self, 10).until(
        Ec.presence_of_element_located((By.XPATH, '//*[@id="global-warning-message"]/div/ul/li/span'))
      )
      print(warning_message.text)
    except TimeoutException:
      print('the warning is not there... TimeOutException')
    except NoSuchElementException:
      print("the warning is not there... NoSuchElementException")

    dtable = self.find_element(By.CSS_SELECTOR, 'table[id=calendar-table-outbound] tbody')
    dtd_tags = dtable.find_elements(By.CLASS_NAME, 'calendarPerBound-fare')
    dinfos = []
    for dtag in dtd_tags:
      # date_section = dtag.find_element(By.CLASS_NAME, 'calendarPerBound-date-section')
      date = dtag.find_element(By.CSS_SELECTOR, 'div.calendarPerBound-date').text.strip()
      month = dtag.find_element(By.CSS_SELECTOR, 'div.calendarPerBound-month').text.strip()
      try:
        price_section = dtag.find_element(By.CSS_SELECTOR, 'div.fare-checkbox-label-content '
                                                           'span.calendarPerBound-price span').text.strip()
        # 'div.fare-checkbox-label-content'
        # 'div.fare-checkbox-label-content span.calendarPerBound-price span'

        dinfos.append({
          'date': date,
          'month': month,
          'price': f'${price_section} USD'
        })
      except NoSuchElementException:
        dinfos.append({
          'date': date,
          'month': month,
          'price': 'NOT AVAILABLE'
        })
        continue
    print(dinfos)
    if warning_message != '':
      return dinfos, warning_message

    return dinfos
