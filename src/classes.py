import requests
import json

class HeadHunterAPI:
    HH_API_URL = 'https://api.hh.ru/vacancies'
    def __init__(self):
        self.params = {'per_page': 100}

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
        pass

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


