from aircanada.air_can_bot import AirCanBot

with AirCanBot() as can_bot:
  can_bot.scrape_home_page()

# can_bot = AirCanBot()
# can_bot.scrape_home_page()
