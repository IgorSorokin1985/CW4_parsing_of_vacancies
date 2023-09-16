import csv
import datetime

class CSVSaver:
    """
    This class for saving vacancies in CSV-file
    """

    def __init__(self):
        pass

    def save_vacancies(self, vacancies: list):
        """
        Saving information about vacancies in CSV-file
        :param vacancies: list of objects Vacancy
        :return: path file
        """
        path = self.get_path()
        with open(path, 'w', newline='', encoding='UTF-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                ['id', 'name', 'data_published', 'salary_from', 'salary_to', 'currency', 'area', 'url', 'employer', 'employer_url', 'requirement', 'experience', 'employment'])
            for vacancy in vacancies:
                writer.writerow([vacancy.id, vacancy.name, vacancy.data_published, vacancy.salary_from, vacancy.salary_to, vacancy.currency,
                                 vacancy.area, vacancy.url, vacancy.employer, vacancy.employer_url, vacancy.requirement, vacancy.experience, vacancy.employment])
        return path

    def get_path(self):
        """
        Getting path new file using date and time now.
        :return: path of new file
        """
        data_now = datetime.datetime.now()
        result = 'data/research/' + str(data_now)[:19] + ' vacancies.csv'
        return result
