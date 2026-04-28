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
        
        self.cookies = None
        self.all = None
        self.times = None

        self.login = None
        self.password = None
        self.base_url = None
        if self._get_configfile():

            if self.login and self.password:
                lgn = Login(self.login, self.password)
                self.cookies = lgn.cookies
                self.base_url = lgn.base_url
        
            context_url = f"{self.base_url}/api/Context"
            self.all = requests.get(url=context_url, headers=self.headers, cookies=self.cookies).json()['uczniowie'][0]

            porylekcji_url = f"{self.base_url}/api/PoryLekcji?key={self.all['key']}"
            times = requests.get(url=porylekcji_url, cookies=self.cookies, headers=self.headers).json()
            self.times = self._parse_times(times)

    def _get_configfile(self) -> bool:
        filename = "config.json"
        if sys.platform == "linux":
            dir = os.path.join(os.getenv('HOME'), ".config", "dziennik-cli")
            filelocation = os.path.join(dir, filename)
            if os.path.isfile(filelocation):
                with open(filelocation, "r") as f:
                    data = json.load(f)
                    self.login = data['Login']
                    self.password = data['Password']
                return True
            else:
                os.mkdir(dir)
                with open(filelocation, "w") as f:
                    conf = {'Login': 'example', 'Password': 'example123'}
                    f.write(json.dumps(conf))
                    print(f"Configure account: {filelocation}")
                    return False

        else:
            return False

    def _parse_times(self, data : tuple) -> dict:
        times = {}
        for i in data:
            times[format_hour(i['poczatek'])] = str(i['numer'])

        return times
