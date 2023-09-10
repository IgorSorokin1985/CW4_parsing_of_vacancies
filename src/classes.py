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
        #print(json.dumps(response_data, indent=2, ensure_ascii=False))
        return response_data['items']

    def add_words(self, text):
        self.params['text'] = text

    def add_area(self, city):
        self.params['area'] = self.areas[city]

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
        'page': 0}
        self.areas = self.all_areas()

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
        #print(json.dumps(response_data, indent=2, ensure_ascii=False))
        #print(len(response_data['objects']))
        return response_data['objects']

    def all_areas(self):
        headers = {
            'X-Api-App-Id': self.SJ_SPI_TOKIN
        }
        result = {}
        response = requests.get(self.SJ_API_URL_AREAS, headers=headers, params={'id_country': 1, 'all': 1})
        response_data = json.loads(response.text)
        for area in response_data['objects']:
            result[area["title"].lower()] = area["id"]
        #print(json.dumps(result, indent=2, ensure_ascii=False))
        return result

class Vacancy:
    def __init__(self, vacancy_information):
        self.id = vacancy_information["id"]
        self.type = vacancy_information["type"]
        self.name = vacancy_information["name"]
        self.data_published = vacancy_information["data_published"]
        self.salary_from = vacancy_information["salary_from"]
        self.salary_to = vacancy_information["salary_to"]
        self.currency = vacancy_information["currency"]
        self.area = vacancy_information["area"]
        self.url = vacancy_information["url"]
        self.employer = vacancy_information["employer"]
        self.employer_url = vacancy_information["employer_url"]
        self.requirement = vacancy_information["requirement"]
        self.experience = vacancy_information["experience"]
        self.employment = vacancy_information["employment"]

    def __str__(self):
        return f'''Vacancy - {self.name}
Type - {self.type}
Data published - {self.data_published}
Employer - {self.employer}
Salary - {self.salary_from} - {self.salary_to}
Requirement - {self.requirement[:200]}
Experience - {self.experience}
Employment - {self.employment}
Area - {self.area}
Url - {self.url}

'''

    @classmethod
    def create_vacancy_from_hh(cls, vacancy_info_hh):
        result = {
            "id": vacancy_info_hh["id"],
            "website": 'HeadHunter',
            "type": vacancy_info_hh["type"]["name"],
            "name": vacancy_info_hh["name"],
            "data_published": vacancy_info_hh["published_at"],
            "salary_from": cls.check_params(vacancy_info_hh, "salary", "from"),
            "salary_to": cls.check_params(vacancy_info_hh, "salary", "to"),
            "currency": cls.check_params(vacancy_info_hh,"salary", "currency"),
            "area": vacancy_info_hh["area"]["name"],
            "url": vacancy_info_hh["alternate_url"],
            "employer": vacancy_info_hh["employer"]["name"],
            "employer_url": vacancy_info_hh["employer"]["alternate_url"],
            "requirement": vacancy_info_hh["snippet"]["requirement"],
            "experience": vacancy_info_hh["experience"]["name"],
            "employment": vacancy_info_hh["employment"]["name"]
        }
        return Vacancy(result)

    @classmethod
    def create_vacancy_from_sj(cls, vacancy_info_sj):
        result ={
            "id": vacancy_info_sj["id"],
            "website": 'SupurJob',
            "type": 'Открытая',
            "name": vacancy_info_sj["profession"],
            "data_published": vacancy_info_sj["date_published"],
            "salary_from": vacancy_info_sj["payment_from"],
            "salary_to": vacancy_info_sj["payment_to"],
            "currency": vacancy_info_sj["currency"],
            "area": vacancy_info_sj["client"]["town"]["title"],
            "url": vacancy_info_sj["link"],
            "employer": vacancy_info_sj["client"]["title"],
            "employer_url": vacancy_info_sj["client"]["link"],
            "requirement": vacancy_info_sj["candidat"],
            "experience": vacancy_info_sj["experience"]["title"],
            "employment": vacancy_info_sj["type_of_work"]["title"]
        }
        return Vacancy(result)

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
            Requirement - {item.requirement[:200]}
            Experience - {item.experience}
            Employment - {item.employment}
            Area - {item.area}
            Url - {item.url}
    
            '''
        return result