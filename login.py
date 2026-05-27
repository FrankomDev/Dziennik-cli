import requests
from bs4 import BeautifulSoup
import sys

class Login:
    def __init__(self, login : str, password : str) -> None:
        login_url = "https://eduvulcan.pl/logowanie"
        query_url = "https://eduvulcan.pl/Account/QueryUserInfo"
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        headers = {"User-Agent": user_agent}

        r = requests.get(url=login_url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.find("input", {"name": "__RequestVerificationToken"}).get('value') 

        form_headers = {"User-Agent": user_agent, "Content-Type": "application/x-www-form-urlencoded"}
        data_query = {
            'Alias': login,
            '__RequestVerificationToken': token
        }
        query = requests.post(url=query_url, headers=form_headers, data=data_query)

        data_login = {
            'UserName': login, # before it was named Alias but they changed it? idk why
            'Password': password,
            'captcha-response': "",
            '__RequestVerificationToken': token
        }


        s = requests.session()
        s.cookies.update(dict(r.cookies))
        s.headers.update(form_headers)

        # when you log in there's button with your name and here i need to get url
        r = s.post(url=login_url, data=data_login)
        soup = BeautifulSoup(r.text, 'html.parser')
        href = soup.find("a", class_="connected-account access-row bg-on-hover flex-grow-1").get("href")
        url = "https://eduvulcan.pl"+str(href)
        r = s.get(url=url)

        # it does some shitty redirecting and i need to handle it to get user's token
        soup = BeautifulSoup(r.text, 'html.parser')
        url = soup.find("form").get("action")
        wa = soup.find("input", {'name': 'wa'}).get("value")
        wresult = soup.find("input", {'name': 'wresult'}).get("value")
        wctx = soup.find("input", {'name': 'wctx'}).get("value")
        data = {
            'wa': wa,
            'wresult': wresult,
            'wctx': wctx
        }
        r = s.post(url=str(url), data=data)

        soup = BeautifulSoup(r.text, 'html.parser')
        url = soup.find("form").get("action")
        wa = soup.find("input", {'name': 'wa'}).get("value")
        wresult = soup.find("input", {'name': 'wresult'}).get("value")
        wctx = soup.find("input", {'name': 'wctx'}).get("value")
        data = {
            'wa': wa,
            'wresult': wresult,
            'wctx': wctx
        }
        r = s.post(url=str(url), data=data)

        self.cookies = dict(s.cookies)
        self.base_url = str(r.url).split("/App")[0]
