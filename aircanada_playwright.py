from playwright.sync_api import sync_playwright
import requests

url = "https://www.aircanada.com/ca/en/aco/home/app.html#/search?org1=YUL&dest1=TUN&orgType1=A&destType1=A&org2=TUN&dest2=YUL&orgType2=A&destType2=A&departure1=29%2F07%2F2023&departure2=28%2F08%2F2023&marketCode=INT&numberOfAdults=3&numberOfYouth=1&numberOfChildren=1&numberOfInfants=0&numberOfInfantsOnSeat=0&tripType=R&isFlexible=false"

def get_cookie_playwright():
  with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)

get_cookie_playwright()