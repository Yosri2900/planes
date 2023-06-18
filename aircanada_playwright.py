from playwright.sync_api import sync_playwright
import requests, json

url = "https://www.aircanada.com/ca/en/aco/home/app.html#/search?org1=YUL&dest1=TUN&orgType1=A&destType1=A&org2=TUN&dest2=YUL&orgType2=A&destType2=A&departure1=29%2F07%2F2023&departure2=28%2F08%2F2023&marketCode=INT&numberOfAdults=3&numberOfYouth=1&numberOfChildren=1&numberOfInfants=0&numberOfInfantsOnSeat=0&tripType=R&isFlexible=false"


def test_json(response, results):
    try:
        results.append({"url": response.url, "data": response.json()})
    except:
        pass


def get_cookie_playwright():
    res = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # context = browser.new_context()
        page = browser.new_page()
        # page.on("request", lambda request: print(">>", request.method, request.url))
        page.on("response", lambda response: test_json(response, res))

        page.goto(url)
        browser.close()
    return res


data = get_cookie_playwright()
print(len(data))
with open("results.json", "w") as f:
    json.dump(data, f)
