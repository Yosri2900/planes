from aircanada.air_can_bot import AirCanBot
from tunisair.tunis_air_bot import TunisairBot

if __name__ == '__main__':
  # with AirCanBot(trip_type="Round-trip") as can_bot:
  #   can_bot.scrape()
  with TunisairBot() as tunis_bot:
    tunis_bot.scrape()

# can_bot = AirCanBot()
# can_bot.scrape_home_page()

