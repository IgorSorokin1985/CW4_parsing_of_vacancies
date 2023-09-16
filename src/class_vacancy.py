import datetime

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
        self.salary_average = self.salary_average()

    def __str__(self):
        return f'''Vacancy - {self.name}
Type - {self.type}
Data published - {datetime.datetime.fromtimestamp(self.data_published).strftime('%Y-%m-%d %H:%M:%S')}
Employer - {self.employer}
Salary - {self.salary_from} - {self.salary_to}
Requirement - {self.requirement[:200]}
Experience - {self.experience}
Employment - {self.employment}
Area - {self.area}
Url - {self.url}

'''

    def salary_average(self):
        if self.salary_from:
            if self.salary_to:
                result = int((self.salary_to + self.salary_from) / 2)
            else:
                result = self.salary_from
        else:
            if self.salary_to:
                result = self.salary_to
            else:
                result = 0

        return result

    @classmethod
    def create_vacancy_from_hh(cls, vacancy_info_hh):
        result = {
            "id": vacancy_info_hh["id"],
            "website": 'HeadHunter',
            "type": vacancy_info_hh["type"]["name"],
            "name": vacancy_info_hh["name"],
            "data_published": datetime.datetime.strptime(vacancy_info_hh["published_at"], '%Y-%m-%dT%H:%M:%S+%f').timestamp(),
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
