import selenium
import aircanada.constants as const
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re


class AirCanBot(uc.Chrome):
  teardown = False

  def __init__(self, trip_type: str = "Round-trip"):
    self.options = webdriver.ChromeOptions()
    self.options.add_argument('proxy-server=106.122.8.54.3128')
    self.trip_type = trip_type
    # self.options.add_experimental_option('detach', True)
    # not sure how to handle the options for now
    super(AirCanBot, self).__init__(options=self.options)
    self.get(const.AIR_CANADA_HOME_PAGE)
    self.set_window_size(800, 600)
    sleep(2)

  def scrape(self):

    if self.trip_type == "Round-trip":
      self.scrape_round_trip(start_airport="YUL", to_airport="TUN", from_date="26/08", to_date="17/09")

    elif self.trip_type == "One-way":
      self.scrape_one_way_trip(start_airport="YUL", to_airport="TUN", from_date="26/08")

    elif self.trip_type == "Multi-city/Stopover":
      print("TODO")
      self.scrape_multi_city_trip()

  def scrape_round_trip(self, start_airport: str = None, to_airport: str = None, from_date: str = None,
                        to_date: str = None):
    self.find_element(By.XPATH, '//*[@id="bkmgFlights_tripTypeSelector_R"]').click()
    from_location = WebDriverWait(self, 3).until(
      Ec.presence_of_element_located((By.XPATH, '//*[@id="bkmgFlights_origin_trip_1"]'))
    )
    from_location.clear()
    from_text = "Montr"
    for char in from_text:
      from_location.send_keys(char)
      sleep(0.5)

    self.execute_script("window.scrollTo(0, 700)")
    self.maximize_window()
    sleep(0.2)

    self.find_element(By.XPATH, '//*[@id="bkmgFlights_origin_trip_1SearchResult1"]').click()

    to_location = WebDriverWait(self, 3).until(
      Ec.presence_of_element_located((By.XPATH, '//*[@id="bkmgFlights_destination_trip_1"]'))
    )

    to_text = "Tuni"
    for char in to_text:
      to_location.send_keys(char)
      sleep(0.5)
    sleep(0.2)
    self.find_element(By.XPATH, '//*[@id="bkmgFlights_destination_trip_1SearchResult0"]/abc-ripple/div').click()
    # sleep(2)

    self.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1-formfield-1"]').click()
    sleep(0.4)
    self.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1_clearDates"]').click()

    # aircanada accepts DD/MM/YYYY, but YYYY is not necessary
    month_start = self.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1-formfield-1"]')
    month_start.send_keys(from_date)

    month_return = self.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1-formfield-2"]')
    month_return.send_keys(to_date)

    select_period = self.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1_confirmDates"]')
    select_period.click()
    sleep(0.1)

    # search the results
    self.find_element(By.XPATH, '//*[@id="bkmgFlights_findButton"]').click()

    title = WebDriverWait(self, 10).until(
      Ec.presence_of_element_located((By.TAG_NAME, 'h1'))
    )
    print(f'title: {title.text}')
    if title.text == "Departing flight":
      #scraping details of flights
      ul_tag = self.find_element(By.XPATH, '//*[@id="flightBlockWrapper"]/div[2]/div/ul')
      tickets = ul_tag.find_elements(By.TAG_NAME, 'li')
      if len(tickets) > 0:
        ticket_number = 0
        for ticket in tickets:
          layovers = []
          details = ''
          num: int = 0
          num_2: int = 1
          while True:
            try:
              layovers_duration = self.find_element(By.XPATH, f'//*[@id="flightBlockWrapper"]/div[2]/div/ul/li[{ticket_number+1}]/flight-row/div/div/div/div[1]/bound-itinerary/div[3]/div/div/div[2]/div[{num_2}]/span/span[2]')
              stopovers_airports = self.find_element(By.CSS_SELECTOR, f'span[id^=itineraryConnectingLocation_{num}_{ticket_number}]')
              layovers.append((stopovers_airports.text, layovers_duration.text))
              num += 1
              num_2 += 1
            except selenium.common.exceptions.NoSuchElementException:
              num = 0
              num_2 = 1
              break

          if len(layovers) == 0:
            details = 'Non-stop'

          depart_time = self.find_element(By.CSS_SELECTOR, f'div[id^=itineraryDepartTime_{ticket_number}]')
          arrival_time = self.find_element(By.CSS_SELECTOR, f'div[id^=itineraryArrivalTime_{ticket_number}]')
          flight_duration = self.find_element(By.CSS_SELECTOR, f'span[id^=flightDuration_{ticket_number}] :nth-child(2)')

          tickets_price = ticket.find_elements(By.CSS_SELECTOR, 'div[class=display-on-hover]')
          prices = [price.text for price in tickets_price]

          print(f'departtime :{depart_time.text}, arrival_time: {arrival_time.text}, layovers: {details},  flightduration: {flight_duration.text}, {len(layovers)} stopovers: {layovers}, prices: {prices}')
          ticket_number += 1
      self.find_element(By.CSS_SELECTOR, 'button.no-style-btn').click()
      print("------Return Flights----------------")
      # return_title = WebDriverWait(self, 10).until(
      #   Ec.presence_of_element_located((By.TAG_NAME, 'h1'))
      # )
      # if return_title.text == "Return flight":
      #   btns_return = self.find_elements(By.CSS_SELECTOR, 'button[id^="cabinBtnECO"]')
      #   for btn_return in btns_return:
      #     btn_return.click()
      #     table_rows = self.find_elements(By.CSS_SELECTOR,
      #                                     'table > tr:last-child > td:not(:first-child) button.no-style-btn '
      #                                     'div.btn-value span')
      #     for row in table_rows:
      #       print(row.text)
      # self.quit()

  def scrape_one_way_trip(self, start_airport: str = None, to_airport: str = None, from_date: str = None):
    # self.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
    # self.__init__(trip_type="One-way")
    self.find_element(By.XPATH, '//*[@id="bkmgFlights_tripTypeSelector_O"]').click()
    from_location = WebDriverWait(self, 3).until(
      Ec.presence_of_element_located((By.XPATH, '//*[@id="bkmgFlights_origin_trip_1"]'))
    )
    from_location.clear()
    from_text = "Montr"
    for char in from_text:
      from_location.send_keys(char)
      sleep(0.5)

    self.execute_script("window.scrollTo(0, 700)")
    self.maximize_window()
    sleep(0.2)

    self.find_element(By.XPATH, '//*[@id="bkmgFlights_origin_trip_1SearchResult1"]').click()

    to_location = WebDriverWait(self, 3).until(
      Ec.presence_of_element_located((By.XPATH, '//*[@id="bkmgFlights_destination_trip_1"]'))
    )

    to_text = "Tuni"
    for char in to_text:
      to_location.send_keys(char)
      sleep(0.5)
    sleep(0.2)

    self.find_element(By.XPATH, '//*[@id="bkmgFlights_destination_trip_1SearchResult0"]/abc-ripple/div').click()
    sleep(0.2)

    self.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1"]').click()
    sleep(0.4)
    self.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1_clearDates"]').click()

    # aircanada accepts DD/MM/YYYY, but YYYY is not necessary
    month_start = self.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1"]')
    month_start.send_keys(from_date)
    self.find_element(By.XPATH, '//*[@id="bkmgFlights_travelDates_1AbcCalendarDialogCloseButton"]').click()

    sleep(0.1)
    # search flights
    self.find_element(By.XPATH, '//*[@id="bkmgFlights_findButton"]').click()

  def scrape_multi_city_trip(self, start_airport: str = None, to_airport: str = None, from_date: str = None,
                             to_date: str = None):
    self.find_element(By.XPATH, '//*[@id="bkmgFlights_tripTypeSelector_M"]').click()
    pass

  def set_trip_type(self, trip_type: str):
    self.trip_type = type
