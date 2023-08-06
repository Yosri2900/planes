from aircanada.air_can_bot import AirCanBot
from tunisair.tunis_air_bot import TunisairBot

if __name__ == '__main__':
  # with AirCanBot(trip_type="One-way") as can_bot:
  #   res = can_bot.scrape()
  #   print(res)
  #   can_bot.quit()

  # with TunisairBot(trip_type="One-way") as tunis_bot:
  #   res = tunis_bot.scrape()
  #   print(res)
  # with AirCanBot(trip_type="Round-trip") as can_bot:
  #   res = can_bot.scrape()
  #   print(res)
  #   can_bot.quit()

  with TunisairBot(trip_type="Round-trip") as tunis_bot:
    res = tunis_bot.scrape()
    print(res)
