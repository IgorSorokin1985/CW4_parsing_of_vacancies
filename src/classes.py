import requests
import json

class HeadHunterAPI:
    HH_API_URL = 'https://api.hh.ru/vacancies'
    HH_API_URL_AREAS = 'https://api.hh.ru/areas'
    def __init__(self):
        self.params = {'per_page': 10}

    def get_vacancies(self):
        response = requests.get(self.HH_API_URL, self.params)
        response_data = json.loads(response.text)
        # print(json.dumps(response_data, indent=2, ensure_ascii=False))
        return response_data['items']

    def add_text(self, text):
        self.params['text'] = text

    def add_area(self, city):
        result = HeadHunterAPI.find_city_number(city)
        self.params['area'] = result

    @staticmethod
    def find_city_number(city):
        areas = HeadHunterAPI.all_areas()
        if city.lower() in areas:
            return areas[city.lower()]
        else:
            return None

    @staticmethod
    def all_areas():
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

class SuperJobAPI:
    pass

class Vacancy:
    def __init__(self, vacancy_information):
        self.id = self.check_params(vacancy_information,"id")
        self.type = self.check_params(vacancy_information, "type", "name")
        self.name = self.check_params(vacancy_information,"name")
        self.data_published = self.check_params(vacancy_information, "published_at")
        self.salary_from = self.check_params(vacancy_information, "salary", "from")
        self.salary_to = self.check_params(vacancy_information, "salary", "to")
        self.currency = self.check_params(vacancy_information, "salary", "currency")
        self.area = self.check_params(vacancy_information, "area", "name")
        self.url = self.check_params(vacancy_information, "alternate_url")
        self.employer = self.check_params(vacancy_information, "employer", "name")
        self.employer_url = self.check_params(vacancy_information, "employer", "alternate_url")
        self.requirement = self.check_params(vacancy_information, "snippet", "requirement")
        self.experience = self.check_params(vacancy_information, "experience", "name")
        self.employment = self.check_params(vacancy_information, "employment", "name")

    def __str__(self):
        return f'''Vacancy - {self.name}
Type - {self.type}
Data published - {self.data_published}
Employer - {self.employer}
Salary - {self.salary_from} - {self.salary_to}
Requirement - {self.requirement}
Experience - {self.experience}
Employment - {self.employment}
Area - {self.area}
Url - {self.url}

'''

    @staticmethod
    def check_params(vacancy_information, param1, param2=None):
        if param1 in vacancy_information:
            if param2 is None:
                return vacancy_information[param1]
            else:
                if type(vacancy_information[param1]) == dict and param2 in vacancy_information[param1]:
                    return vacancy_information[param1][param2]
                else:
                    return None
        else:
            return None


class JSONSaver:
    pass

class CSVSaver:
    pass


