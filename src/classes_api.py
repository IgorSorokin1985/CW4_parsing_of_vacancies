from abc import ABC, abstractmethod
import requests
import json
import datetime
import time


class API(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def change_date(self, days=14):
        pass

    @abstractmethod
    def add_words(self, text):
        pass

    @abstractmethod
    def add_area(self, city):
        pass

    @abstractmethod
    def all_areas(self):
        pass

class HeadHunterAPI(API):
    HH_API_URL = 'https://api.hh.ru/vacancies'
    HH_API_URL_AREAS = 'https://api.hh.ru/areas'
    def __init__(self):
        self.params = {
            'per_page': 100,
        }
        self.change_date()
        self.areas = self.all_areas()

    def get_vacancies(self):
        response = requests.get(self.HH_API_URL, self.params)
        response_data = json.loads(response.text)
        if 'items' in response_data:
            return response_data['items']
        else:
            return []

    def change_date(self, days=14):
        self.params['period'] = days

    def add_words(self, text):
        self.params['text'] = text

    def add_area(self, city):
        self.params['area'] = self.areas[city]

    def all_areas(self):
        req = requests.get(HeadHunterAPI.HH_API_URL_AREAS)
        data = req.content.decode()
        req.close()
        dict_areas = json.loads(data)
        areas = {}
        for k in dict_areas:
            for i in range(len(k['areas'])):
                if len(k['areas'][i]['areas']) != 0:  # Если у зоны есть внутренние зоны
                    for j in range(len(k['areas'][i]['areas'])):
                        areas[k['areas'][i]['areas'][j]['name'].lower()] = k['areas'][i]['areas'][j]['id']
                else:  # Если у зоны нет внутренних зон
                    areas[k['areas'][i]['name'].lower()] = k['areas'][i]['id']
        return areas

class SuperJobAPI(API):
    SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
    SJ_API_URL_AREAS = 'https://api.superjob.ru/2.0/towns/'
    SJ_SPI_TOKIN = 'v3.r.137807815.17181db4d5258989a59988d60bd12edf13ee0a71.bed98dc22a081d987b5c629d7799d55d36f58bb9'

    def __init__(self):
        self.params = {
        'count': 100,
        'page': 0
        }
        self.change_date()
        self.areas = self.all_areas()

    def change_date(self, days=14):
        search_from = datetime.datetime.now() - datetime.timedelta(days=days)
        unix_time = int(time.mktime(search_from.timetuple()))
        self.params['date_published_from'] = unix_time

    def add_words(self, words):
        self.params['keyword'] = words

    def add_area(self, city):
        self.params['town'] = self.areas[city]

    def get_vacancies(self):
        headers = {
            'X-Api-App-Id': self.SJ_SPI_TOKIN
        }
        response = requests.get(self.SJ_API_URL, headers=headers, params=self.params)
        response_data = json.loads(response.text)
        if 'objects' in response_data:
            return response_data['objects']
        else:
            return []

    def all_areas(self):
        headers = {
            'X-Api-App-Id': self.SJ_SPI_TOKIN
        }
        result = {}
        response = requests.get(self.SJ_API_URL_AREAS, headers=headers, params={'id_country': 1, 'all': 1})
        response_data = json.loads(response.text)
        for area in response_data['objects']:
            result[area["title"].lower()] = area["id"]

        return result

class JSONSaver:
    pass

class CSVSaver:
    pass