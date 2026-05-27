import requests
import json
import os
import sys
from utils import *
from login import *

class Context:
    def __init__(self) -> None:
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        self.headers = {"User-Agent": user_agent}
        self.ok = False
        
        self.cookies = None
        self.all = None
        self.times = None

        self.login = None
        self.password = None
        self.base_url = None
        if self._get_configfile():

            cache = self._read_cache()
            if not cache:
                self._login()
        
            context_url = f"{self.base_url}/api/Context"

            while True:
                try:
                    self.all = requests.get(url=context_url, headers=self.headers, cookies=self.cookies).json()['uczniowie'][0]
                    break
                #except KeyError:
                except Exception:
                    if cache:
                        self._login()
                        continue
                    else:
                        print("Nie można się zalogować!")
                        break
            if self.all:
                self.ok = True
                porylekcji_url = f"{self.base_url}/api/PoryLekcji?key={self.all['key']}"
                times = requests.get(url=porylekcji_url, cookies=self.cookies, headers=self.headers).json()
                self.times = self._parse_times(times)
            else:
                sys.exit()

    def _login(self) -> None:
        if self.login and self.password:
            try:
                lgn = Login(self.login, self.password)
                self.cookies = lgn.cookies
                self.base_url = lgn.base_url
                self._save_cache()
            except AttributeError:
                print("Niepoprawny login lub hasło!")
                sys.exit()

    def _get_configfile(self) -> bool:
        if os.path.isfile(config_location):
            with open(config_location, "r") as f:
                data = json.load(f)
                self.login = data['Login']
                self.password = data['Password']
            return True
        else:
            with open(config_location, "w") as f:
                conf = {'Login': 'example', 'Password': 'example123'}
                f.write(json.dumps(conf))
                print(f"Skonfiguruj konto: {config_location}")
                return False
        
    def _save_cache(self) -> None:
        data = {"cookies": self.cookies, "url": self.base_url}
        with open(cache_location, "w") as f:
            f.write(json.dumps(data))
    def _read_cache(self) -> bool:
        if os.path.exists(cache_location):
            with open(cache_location, "r") as f:
                data = json.load(f)
                self.cookies = data['cookies']
                self.base_url = data['url']
                return True
        else:
            return False

    def _parse_times(self, data : tuple) -> dict:
        times = {}
        for i in data:
            times[format_hour(i['poczatek'])] = str(i['numer'])

        return times
