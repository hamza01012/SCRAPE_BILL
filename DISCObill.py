import requests
from bs4 import BeautifulSoup

class DISCOBill:

    def __init__(self,city_disco="fesco"):
        self.city_disco = city_disco
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://bill.pitc.com.pk/{city_disco}bill"
            }
        self.url = f"https://bill.pitc.com.pk/{city_disco}bill"
        self.r = self.session.get(self.url, headers=self.headers)

        self.soup = BeautifulSoup(self.r.text, "html.parser")

        # STEP 2 — Extract ASP.NET tokens
        self.viewstate = self.soup.find("input", {"name": "__VIEWSTATE"})["value"]
        self.eventvalidation = self.soup.find("input", {"name": "__EVENTVALIDATION"})["value"]
        self.viewstategen = self.soup.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"]
        self.token = self.soup.find("input", {"name": "__RequestVerificationToken"})["value"]


    def show(self,APP_NO):

                # STEP 3 — Prepare POST payload
        payload = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": self.viewstate,
            "__VIEWSTATEGENERATOR": self.viewstategen,
            "__EVENTVALIDATION": self.eventvalidation,
            "__RequestVerificationToken": self.token,
            "rbSearchByList": "appno",      # search by customer id
            "searchTextBox": APP_NO,
            "ruCodeTextBox": "",
            "btnSearch": "Search"
            }

        # STEP 4 — Send POST request
        post = self.session.post(self.url, data=payload, headers=self.headers)

        # STEP 5 — Parse bill page
        soup = BeautifulSoup(post.text, "html.parser")

        with open(f"templates/{self.city_disco}/{APP_NO}.html", "w",encoding="utf-8") as f:
            f.write(post.text)       
       
        return post.text
