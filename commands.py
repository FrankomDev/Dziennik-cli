import requests
from datetime import datetime
from context import Context
from utils import *

class Commands:
    def __init__(self, context : Context) -> None:
        self.context = context

    def get_oceny(self, przedmiot = None, okresklasyfikacyjny = None) -> None:
        if self.context.all:
            okresyklasyfikacyjne_url = f"{self.context.base_url}/api/OkresyKlasyfikacyjne?key={self.context.all['key']}&idDziennik={self.context.all['idDziennik']}"
            okresyklasyfikacyjne = requests.get(url=okresyklasyfikacyjne_url, cookies=self.context.cookies, headers=self.context.headers).json()
    
            okres = okresyklasyfikacyjne[len(okresyklasyfikacyjne)-1]['id']
            if okresklasyfikacyjny:
                for i in okresyklasyfikacyjne:
                    if i['numerOkresu'] == okresklasyfikacyjny:
                        okres = i['id']
    
            oceny_url = f"{self.context.base_url}/api/Oceny?key={self.context.all['key']}&idOkresKlasyfikacyjny={okres}"
            oceny = requests.get(url=oceny_url, cookies=self.context.cookies, headers=self.context.headers).json()['ocenyPrzedmioty']
    
            if przedmiot:
                for i in oceny:
                    if i['przedmiotNazwa'] == przedmiot:
                        print(f"{przedmiot}:")
                        for j in i['kolumnyOcenyCzastkowe']:
                            for k in j['oceny']:
                                print(f"{k['wpis']} -> {k['nazwaKolumny']}, {k['kategoriaKolumny']}")
                        break
            else:
                for i in oceny:
                    text = f"{i['przedmiotNazwa']}: "
                    for j in i['kolumnyOcenyCzastkowe']:
                        for k in j['oceny']:
                            text += f"{k['wpis']}, "
                    print(text)
    
    def _parse_od_do(self, od, do) -> tuple[str, str]:
        if od:
            od = reformat_date(od)
            if do:
                do = reformat_date(do)
            else:
                do = od
        else:
            od = datetime.now().strftime("%Y-%m-%d")
            do = od

        return od, do


    def get_plan(self, od = None, do = None) -> None:
        if self.context.all:
            od, do = self._parse_od_do(od=od, do=do)
    
            planlekcji_url = f"{self.context.base_url}/api/PlanZajec?key={self.context.all['key']}&dataOd={od}T01:00:00.000Z&dataDo={do}T01:59:59.999Z&zakresDanych=2"
            planlekcji = requests.get(url=planlekcji_url, cookies=self.context.cookies, headers=self.context.headers).json()
    
            last_date = None
            for i in planlekcji:
                date = format_date(i['data'])
                if last_date != date:
                    if last_date is not None:
                        print("")
                    last_date = date
                    print(date+":")
                text = "0. "
                if self.context.times:
                    text = f"{self.context.times[format_hour(i['godzinaOd'])]}. "
                text += i['przedmiot']
                text += f": {i['sala']}, {format_hour(i['godzinaOd'])}-{format_hour(i['godzinaDo'])}"
                print(text)
    
    def get_frekwencja(self, od = None, do = None) -> None:
        # need to sort because api can give unsorted :/
        if self.context.all:
            od, do = self._parse_od_do(od=od, do=do)

            frekwencja_url = f"{self.context.base_url}/api/Frekwencja?key={self.context.all['key']}&dataOd={od}T01:00:00.000Z&dataDo={do}T01:59:59.999Z"
            frekwencja = requests.get(url=frekwencja_url, cookies=self.context.cookies, headers=self.context.headers).json()['oddzialy']

            first_print = True
            sort = {}
            for i in frekwencja:
                try:
                    sort[i['data']].append(i)
                except KeyError:
                    sort[i['data']] = [i]
        
            for i in sort:
                sorted_list = sorted(sort[i], key=lambda x: x['numerLekcji'])
                if first_print:
                    first_print = False
                else:
                    print("")
                print(format_date(i)+":")
        
                for j in sorted_list:
                    text = f"{j['numerLekcji']}. {j['opisZajec']}: {frekwencja_str[int(j['kategoriaFrekwencji'])]}"
                    print(text)

    def get_sprawdziany(self, od = None, do = None) -> None:
        if self.context.all:
            od, do = self._parse_od_do(od=od, do=do)

            sprawdziany_url = f"{self.context.base_url}/api/SprawdzianyZadaniaDomowe?key={self.context.all['key']}&dataOd={od}T01:00:00.000Z&dataDo={do}T01:59:59.999Z"
            sprawdziany = requests.get(url=sprawdziany_url, cookies=self.context.cookies, headers=self.context.headers).json()

            sort = {}
            for i in sprawdziany:
                i['data'] = format_date(i['data'])
                try:
                    sort[i['data']].append(i)
                except KeyError:
                    sort[i['data']] = [i]
        
            first_print = True
            for i in sorted(sort, key=lambda x: datetime.strptime(x, '%d.%m.%Y')):
                if first_print:
                    first_print = False
                else:
                    print("")
                print(i+":")
                for j in sort[i]:
                    szczegoly_url = f"{self.context.base_url}/api/SprawdzianSzczegoly?key={self.context.all['key']}&id={j['id']}"
                    szczegoly = requests.get(url=szczegoly_url, cookies=self.context.cookies, headers=self.context.headers).json()
                    print(f"{szczegoly['przedmiotNazwa']}: {szczegoly['opis'].replace("\n", " ")} - {sprawdziany_str[szczegoly['typ']]}")


    def get_uwagi(self) -> None:
        if self.context.all:
            uwagi_url = f"{self.context.base_url}/api/Uwagi?key={self.context.all['key']}"
            uwagi = requests.get(url=uwagi_url, cookies=self.context.cookies, headers=self.context.headers).json()
        
            for i in uwagi:
                text = format_date(i['data'])+" - "
                text += str(i['tresc']).replace("\n", " ")+" - "
                text += i['kategoria']
                print(text)
