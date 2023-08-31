import requests
import json

class HeadHunterAPI:
    HH_API_URL = 'https://api.hh.ru/vacancies'
    def __init__(self):
        self.params = {'per_page': 100}

    def get_vacancies(self):
        response = requests.get(self.HH_API_URL, self.params)
        response_data = json.loads(response.text)
        return response_data

    def add_text(self, text):
        self.params['text'] = text

    def add_area(self, city):
        result = HeadHunterAPI.find_city_number(city)
        self.params['area'] = result

    @staticmethod
    def find_city_number(city):
        pass

class SuperJobAPI:
    pass

class Vacancy:
    pass

class JSONSaver:
    pass

class CSVSaver:
    pass


