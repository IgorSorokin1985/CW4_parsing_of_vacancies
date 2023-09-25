import csv
import datetime
from xlsxwriter.workbook import Workbook

class Saver:
    """
    This class for saving vacancies in CSV-file
    """

    def __init__(self):
        pass

    def save_vacancies_csv(self, vacancies: list):
        """
        Saving information about vacancies in CSV-file
        :param vacancies: list of objects Vacancy
        :return: path file
        """
        path = self.get_path_csv()
        with open(path, 'w', newline='', encoding='UTF-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                ['id', 'name', 'data_published', 'salary_from', 'salary_to', 'currency', 'area', 'url', 'employer', 'employer_url', 'requirement', 'experience', 'employment'])
            for vacancy in vacancies:
                writer.writerow([vacancy.id, vacancy.name, datetime.datetime.fromtimestamp(vacancy.data_published).strftime('%Y-%m-%d %H:%M:%S'), vacancy.salary_from, vacancy.salary_to, vacancy.currency,
                                 vacancy.area, vacancy.url, vacancy.employer, vacancy.employer_url, vacancy.requirement, vacancy.experience, vacancy.employment])
        return path


    def get_path_csv(self):
        """
        Getting path new file using date and time now.
        :return: path of new file
        """
        data_now = datetime.datetime.now()
        result = 'data/research/' + str(data_now)[:19] + ' vacancies.csv'
        return result

    def save_vacancies_xlsx(self, vacancies: list):
        """
        Saving information about vacancies in XLS-file
        :param vacancies: list of objects Vacancy
        :return: path file
        """
        path = self.get_path_xlsx()

        workbook = Workbook(path)
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 1, 'id')
        worksheet.write(0, 2, 'name')
        worksheet.write(0, 3, 'data_published')
        worksheet.write(0, 4, 'salary_from')
        worksheet.write(0, 5, 'salary_to')
        worksheet.write(0, 6, 'currency')
        worksheet.write(0, 7, 'area')
        worksheet.write(0, 8, 'url')
        worksheet.write(0, 9, 'employer')
        worksheet.write(0, 10, 'employer_url')
        worksheet.write(0, 11, 'requirement')
        worksheet.write(0, 12, 'experience')
        worksheet.write(0, 13, 'employment')

        for r, vacancy in enumerate(vacancies):
            worksheet.write(r+1, 0, r+1)
            worksheet.write(r+1, 1, vacancy.id)
            worksheet.write(r+1, 2, vacancy.name)
            worksheet.write(r+1, 3, datetime.datetime.fromtimestamp(vacancy.data_published).strftime('%Y-%m-%d %H:%M:%S'))
            worksheet.write(r+1, 4, vacancy.salary_from)
            worksheet.write(r+1, 5, vacancy.salary_to)
            worksheet.write(r+1, 6, vacancy.currency)
            worksheet.write(r+1, 7, vacancy.area)
            worksheet.write(r+1, 8, vacancy.url)
            worksheet.write(r+1, 9, vacancy.employer)
            worksheet.write(r+1, 10, vacancy.employer_url)
            worksheet.write(r+1, 11, vacancy.requirement)
            worksheet.write(r+1, 12, vacancy.experience)
            worksheet.write(r+1, 13, vacancy.employment)

        workbook.close()

        return path

    def get_path_xlsx(self):
        """
        Getting path new file using date and time now.
        :return: path of new file
        """
        data_now = datetime.datetime.now()
        result = 'data/research/' + str(data_now)[:19] + ' vacancies.xlsx'
        return result
