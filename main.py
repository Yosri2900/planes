import datetime

from datetime import datetime


if __name__ == '__main__':
  currentSecond = datetime.now().second
  currentMinute = datetime.now().minute
  currentHour = datetime.now().hour

  currentDay = datetime.now().day
  currentMonth = datetime.now().month
  currentYear = datetime.now().year

  print(currentYear, type(currentYear))