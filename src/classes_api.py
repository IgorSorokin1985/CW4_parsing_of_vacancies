from abc import ABC, abstractmethod
import requests
import json
import datetime
import time
import os
from src.class_save_json import JSONSaver_Areas
import copy

class API(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def change_date(self, days=14):
        pass

    @abstractmethod
    def add_words(self, words):
        pass

    @abstractmethod
    def add_area(self, city):
        pass

    @abstractmethod
    def load_all_areas(self):
        pass

class HeadHunterAPI(API):
    """
    This class for getting information from headhanter API
    """
    HH_API_URL = 'https://api.hh.ru/vacancies'
    HH_API_URL_AREAS = 'https://api.hh.ru/areas'
    HH_AREAS_JSON = 'data/areas/headhunter_areas.json'
    params_zero = {
        'per_page': 100,
    }

    def __init__(self):
        self.params = copy.deepcopy(self.params_zero)
        self.change_date()
        self.saver_areas = JSONSaver_Areas(self.HH_AREAS_JSON)
        if self.saver_areas.check_file():
            pass
        else:
            self.load_all_areas()

    def get_vacancies(self):
        """
        Getting information about vacancies with params.
        :return: dict
        """
        response = requests.get(self.HH_API_URL, self.params)
        response_data = json.loads(response.text)
        self.params = copy.deepcopy(self.params_zero)
        if 'items' in response_data:
            return response_data['items']
        else:
            return []

    def change_date(self, days: int =14):
        """
        Changing number of days for research. Default - number = 14 days
        :param days: number of days or research
        :return: None
        """
        self.params['period'] = days

    def add_words(self, words: list):
        """
        Adding word for research.
        :param text: list
        :return: None
        """
        self.params['text'] = words

    def add_area(self, city: str):
        """
        Adding city for research.
        :param city: str
        :return: index of city
        """
        self.params['area'] = self.saver_areas.open_and_find_info(city)

    def load_all_areas(self):
        """
        This function for loadind all areas headhunter and saving JSON-file
        :return: None
        """
        req = requests.get(HeadHunterAPI.HH_API_URL_AREAS)
        dict_areas = req.json()

        areas = {}
        for k in dict_areas:
            for i in range(len(k['areas'])):
                if len(k['areas'][i]['areas']) != 0:
                    for j in range(len(k['areas'][i]['areas'])):
                        areas[k['areas'][i]['areas'][j]['name'].lower()] = k['areas'][i]['areas'][j]['id']
                else:
                    areas[k['areas'][i]['name'].lower()] = k['areas'][i]['id']
        self.saver_areas.save_file(areas)

class SuperJobAPI(API):
    SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
    SJ_API_URL_AREAS = 'https://api.superjob.ru/2.0/towns/'
    SJ_API_TOKEN: str = os.getenv('SJ_API_TOKEN')
    SJ_AREAS_JSON = 'data/areas/superjob_areas.json'
    params_zero = {
        'count': 100,
        'page': 0
    }

    def __init__(self):
        self.params = self.params_zero
        self.change_date()
        self.saver_areas = JSONSaver_Areas(self.SJ_AREAS_JSON)
        if self.saver_areas.check_file():
            pass
        else:
            self.load_all_areas()

    def change_date(self, days: int =14):
        """
        Changing number of days for research. Default - number = 14 days
        :param days: number of days or research
        :return: None
        """
        search_from = datetime.datetime.now() - datetime.timedelta(days=days)
        unix_time = int(time.mktime(search_from.timetuple()))
        self.params['date_published_from'] = unix_time

    def add_words(self, words: list):
        """
        Adding word for research.
        :param text: list
        :return: None
        """
        self.params['keyword'] = words

    def add_area(self, city: str):
        """
        Adding city for research.
        :param city: str
        :return: index of city
        """
        self.params['town'] = self.saver_areas.open_and_find_info(city)

    def get_vacancies(self):
        """
        Getting information about vacancies with params.
        :return: dict
        """
        headers = {
            'X-Api-App-Id': self.SJ_API_TOKEN
        }
        response = requests.get(self.SJ_API_URL, headers=headers, params=self.params)
        response_data = json.loads(response.text)
        self.params = copy.deepcopy(self.params_zero)
        if 'objects' in response_data:
            return response_data['objects']
        else:
            return []

    def load_all_areas(self):
        """
        This function for loadind all areas headhunter and saving JSON-file
        :return: None
        """
        headers = {
            'X-Api-App-Id': self.SJ_API_TOKEN
        }
        result = {}
        response = requests.get(self.SJ_API_URL_AREAS, headers=headers, params={'id_country': 1, 'all': 1})
        response_data = json.loads(response.text)
        for area in response_data['objects']:
            result[area["title"].lower()] = area["id"]

        self.saver_areas.save_file(result)
