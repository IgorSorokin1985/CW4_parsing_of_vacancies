import requests
import json

class HeadHunterAPI:
    HH_API_URL = 'https://api.hh.ru/vacancies'
    HH_API_URL_AREAS = 'https://api.hh.ru/areas'
    def __init__(self):
        self.params = {'per_page': 10}
        self.areas = self.all_areas()

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
    SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
    SJ_API_URL_AREAS = 'https://api.superjob.ru/2.0/towns/'
    SJ_SPI_TOKIN = 'v3.r.137807815.17181db4d5258989a59988d60bd12edf13ee0a71.bed98dc22a081d987b5c629d7799d55d36f58bb9'

    def __init__(self):
        self.params = {
        'keyword': ['excel'],
        'town': 397,
        #'no_agreement': 1,
        'page': 0}
        #self.areas = self.all_areas()
        self.areas = {}

    def get_vacancies(self):
        headers = {
            'X-Api-App-Id': self.SJ_SPI_TOKIN
        }
        response = requests.get(self.SJ_API_URL, headers=headers, params=self.params)
        response_data = json.loads(response.text)
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
        print(len(response_data['objects']))
        #return response_data['items']

    def get_areas(self):
        headers = {
            'X-Api-App-Id': self.SJ_SPI_TOKIN
        }
        response = requests.get(self.SJ_API_URL_AREAS, headers=headers, params={'page': 1})
        response_data = json.loads(response.text)
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
        print(len(response_data['objects']))

    @staticmethod
    def all_areas():
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
                    if type(vacancy_information[param1][param2]) == str and vacancy_information[param1][param2].isdigit():
                        return int(vacancy_information[param1][param2])
                    else:
                        return vacancy_information[param1][param2]
                else:
                    return None
        else:
            return None


class JSONSaver:
    pass

class CSVSaver:
    pass

class Mylist:
    def __init__(self):
        self.vacancy_list = []

    def __len__(self):
        return len(self.vacancy_list)

    def add_vacancy(self, vacancy):
        self.vacancy_list.append(vacancy)

    def get_vacancy(self, index):
        return self.vacancy_list[index-1]

    def delete_vacancy(self, vacancy):
        if vacancy in self.vacancy_list:
            self.vacancy_list.remove(vacancy)
        else:
            pass

    def sorting_vacancies(self, param=None):
        if param == 'data_published':
            return sorted(self.vacancy_list, reverse=True, key=lambda vacancy: vacancy.data_published)
        elif param == 'salary_to':
            none_list = []
            all_list = self.vacancy_list.copy()
            for vacancy in self.vacancy_list:
                if vacancy.salary_to == None:
                    all_list.remove(vacancy)
                    none_list.append(vacancy)
            result = sorted(all_list, reverse=True, key=lambda vacancy: vacancy.salary_to)
            for vacancy in none_list:
                result.append(vacancy)
            return result
        else:
            return sorted(self.vacancy_list, reverse=True, key=lambda vacancy: vacancy.data_published)

    def __str__(self):
        result = ''
        for item in self.vacancy_list:
            result += f'''Vacancy - {item.name}
            Type - {item.type}
            Data published - {item.data_published}
            Employer - {item.employer}
            Salary - {item.salary_from} - {item.salary_to}
            Requirement - {item.requirement}
            Experience - {item.experience}
            Employment - {item.employment}
            Area - {item.area}
            Url - {item.url}
    
            '''
        return result