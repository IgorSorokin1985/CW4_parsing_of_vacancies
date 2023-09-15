from src.class_save_csv import CSVSaver

class Mylist:
    def __init__(self):
        self.vacancy_list = []
        self.csv_saver = CSVSaver()

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

    def sorting_vacancies_data(self):
        return sorted(self.vacancy_list, reverse=True, key=lambda vacancy: vacancy.data_published)

    def sorting_vacancies_salary(self):
        return sorted(self.vacancy_list, reverse=True, key=lambda vacancy: vacancy.salary_average)

    def filter_list_word(self, word):
        for vacancy in self.vacancy_list:
            if word in vacancy.requirement or word in vacancy.name:
                pass
            else:
                self.vacancy_list.remove(vacancy)
        return self

    def filter_list_salary(self, salary):
        for vacancy in self.vacancy_list:
            if vacancy.salary_average >= salary:
                pass
            else:
                self.vacancy_list.remove(vacancy)
        return self

    def save_csv(self):
        path = self.csv_saver.save_vacancies(self.vacancy_list)
        return path

    def __str__(self):
        return '\n'.join([f'Vacancy N {index+1}\n{vacancy.__str__()}' for index, vacancy in enumerate(self.vacancy_list)])
