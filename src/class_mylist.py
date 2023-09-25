from src.class_save_csv import Saver

class Mylist:
    """
    This class for working with list of vacancies.
    """
    def __init__(self):
        self.vacancy_list = []
        self.csv_saver = Saver()

    def __len__(self):
        return len(self.vacancy_list)

    def clear_list(self):
        """
        Delete all vacancies from list
        :return: None
        """
        self.vacancy_list.clear()

    def add_vacancy(self, vacancy: object):
        """
        Adding vacancy in list
        :param vacancy:
        :return:
        """
        self.vacancy_list.append(vacancy)

    def get_vacancy(self, index: int):
        """
        Getting vacancy with index
        :param index: int
        :return: vacancy
        """
        return self.vacancy_list[index-1]

    def delete_vacancy(self, vacancy: object):
        """
        Deleting one vacancy in list
        :param vacancy: object Vacancy
        :return: None
        """
        if vacancy in self.vacancy_list:
            self.vacancy_list.remove(vacancy)
        else:
            pass

    def sorting_vacancies_data(self):
        """
        Sorting vacancies in list by date
        :return: None
        """
        self.vacancy_list.sort(reverse=True, key=lambda vacancy: vacancy.data_published)

    def sorting_vacancies_salary(self):
        """
        Sorting vacancies in list by average salary
        :return: None
        """
        self.vacancy_list.sort(reverse=True, key=lambda vacancy: vacancy.salary_average)

    def filter_list_word(self, word: str):
        """
        Filter vacancies with word from user
        :param word: str
        :return: self
        """
        delete_list = []
        for vacancy in self.vacancy_list:
            if word in vacancy.requirement or word in vacancy.name:
                pass
            else:
                delete_list.append(vacancy)
        for vacancy in delete_list:
            self.vacancy_list.remove(vacancy)
        return self

    def filter_list_salary(self, salary: int):
        """
        Filter vacancies with salary from user
        :param salary: int
        :return: self
        """
        delete_list = []
        for vacancy in self.vacancy_list:
            if vacancy.salary_average >= salary:
                pass
            else:
                delete_list.append(vacancy)
        for vacancy in delete_list:
            self.vacancy_list.remove(vacancy)
        return self

    def save_csv(self):
        """
        Saving vacancies in list in CSV-file
        :return: path of file
        """
        path = self.csv_saver.save_vacancies_csv(self.vacancy_list)
        return path

    def save_xlsx(self):
        """
        Saving vacancies in list in CSV-file
        :return: path of file
        """
        path = self.csv_saver.save_vacancies_xlsx(self.vacancy_list)
        return path

    def __str__(self):
        return '\n'.join([f'Vacancy N {index+1}\n{vacancy.__str__()}' for index, vacancy in enumerate(self.vacancy_list)])
