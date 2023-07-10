import datetime, re
from datetime import datetime

ids = [
    'itineraryConnectingLocation_0_0',
    'itineraryConnectingLocation_0_1',
    'itineraryConnectingLocation_0_2',
    'itineraryConnectingLocation_0_3',
    'itineraryConnectingLocation_0_4',
    'itineraryConnectingLocation_0_5',
    'itineraryConnectingLocation_1_5',
    'itineraryConnectingLocation_0_6',
    'itineraryConnectingLocation_0_7',
    'itineraryConnectingLocation_1_7',
    'itineraryConnectingLocation_0_8',
    'itineraryConnectingLocation_0_9'
]

new_ids = [
    'itineraryConnectingLocation_0_0_0',
    'itineraryConnectingLocation_0_0_1',
    'itineraryConnectingLocation_0_0_2',
    'itineraryConnectingLocation_0_0_3',
    'itineraryConnectingLocation_0_0_4',
    'itineraryConnectingLocation_0_0_5',
    'itineraryConnectingLocation_0_1_5',
    'itineraryConnectingLocation_0_0_6',
    'itineraryConnectingLocation_0_0_7',
    'itineraryConnectingLocation_0_1_7',
    'itineraryConnectingLocation_0_0_8',
    'itineraryConnectingLocation_0_0_9'
]


if __name__ == '__main__':
  x: int = 20
  while True:
      try:
          y = 1/x
          print(f'1/{x} = {y}')
          x -= 1
      except ZeroDivisionError:
        x = 10
        break
  print(f'avoided the mistake. Value of x: {x}')
