from src.classes_api import HeadHunterAPI, SuperJobAPI
from src.class_mylist import Mylist
from src.class_vacancy import Vacancy

class Userinput:
    new_param = {
            'website': [],
            'city': [],
            'words': [],
            'date': 14
        }
    def __init__(self):
        self.hh_api = HeadHunterAPI()
        self.sj_api = SuperJobAPI()
        self.all_list = Mylist()
        self.mylist = Mylist()
        self.param = self.new_param

    def __call__(self):
        while True:
            print('Commands:')
            print('1 - Research vacancies')

            if self.mylist.vacancy_list != []:
                print('2 - Show favorite vacancies')

            print('0 - Exit')
            user_input = input()

            if user_input == '0':
                quit()
            elif user_input == '1':
                self.choosing_parameters()
            elif user_input == '2':
                print(self.mylist)
            else:
                print('Unknown command')

    def choosing_parameters(self):
        self.param = self.new_param
        while True:
            self.delete_dublicates()
            print('You need choose websites, city, date and words for research')
            print(f'We are looking for vacancies in the last {self.param["date"]} days')
            if self.param['website'] != []:
                print(f"You choosed next website - {', '.join(self.param['website'])}")
            if self.param['city'] != []:
                print(f"You choosed next city - {', '.join(self.param['city'])}")
            if self.param['words'] != []:
                print(f"You choosed next words - {', '.join(self.param['words'])}")
            print('1 - choose websites')
            print('2 - add words for research')
            print('3 - choose city')
            print('4 - change the search date (by default, the last 14 days)')
            print('5 - research vacancies')
            print('0 - Exit')
            user_input = input()

            if user_input == '0':
                self.__call__()
            elif user_input == '1':
                self.choosing_website()
            elif user_input == '2':
                self.choosing_words()
            elif user_input == '3':
                self.choosing_city()
            elif user_input == '4':
                self.choosing_date()
            elif user_input == '5':
                self.research_vacancies()
            else:
                print('Unknown command')

    def choosing_website(self):
        while True:
            print('We can research vacancies om HeadHunter and SuperJob. Which website you would like to choose?')
            print('1 - HeadHunter')
            print('2 - SuperJob')
            print('3 - HeadHunter and SuperJob')
            print('0 - Exit')
            user_input = input()

            if user_input == '0':
                break
            elif user_input == '1':
                self.param['website'].append('HeadHunter')
                break
            elif user_input == '2':
                self.param['website'].append('SuperJob')
                break
            elif user_input == '3':
                self.param['website'].append('HeadHunter')
                self.param['website'].append('SuperJob')
                break
            else:
                print('Unknown command')

    def choosing_words(self):
        while True:
            self.delete_dublicates()
            if self.param['words'] != []:
                print(f"You choosed next words - {', '.join(self.param['words'])}")
            print('Add word for researching or "delete" for delete all words or press 0 for Exit')
            user_input = input().lower()
            if user_input == '0':
                break
            elif user_input == 'delete':
                self.param['words'].clear()
                break
            else:
                self.param['words'].append(user_input)
                break

    def choosing_city(self):
        print('Add city for researching or press 0 for Exit')
        while True:
            user_input = input().lower()
            if user_input == '0':
                break
            if self.check_city(user_input):
                self.param['city'].append(user_input)
                break
            else:
                print('Try again. Because we did not find this city or press 0 for Exit')

    def check_city(self, user_input):
        if self.hh_api.saver_areas.open_and_find_info(user_input) or self.sj_api.saver_areas.open_and_find_info(user_input):
            return True
        else:
            return False

    def choosing_date(self):
        while True:
            print('Choose number of days for research')
            print('1 - 1 day')
            print('2 - 7 day')
            print('3 - 14 day')
            print('4 - 30 day')
            print('0 - Exit')
            user_input = input()
            if user_input == '0':
                break
            elif user_input == '1':
                self.param['date'] = 1
                break
            elif user_input == '2':
                self.param['date'] = 7
                break
            elif user_input == '3':
                self.param['date'] = 14
                break
            elif user_input == '4':
                self.param['date'] = 30
                break
            else:
                print('Unknown command')

    def research_vacancies(self):
        if 'HeadHunter' in self.param['website']:
            if self.param['city'] != []:
                for item in range(len(self.param['city'])):
                    self.hh_api.add_area(self.param['city'][item])
            if self.param['words'] != []:
                self.hh_api.add_words(self.param['words'])
            self.hh_api.change_date(self.param['date'])

            vacancies_hh = self.hh_api.get_vacancies()

            if vacancies_hh != []:
                for item in vacancies_hh:
                   vacancy = Vacancy.create_vacancy_from_hh(item)
                   self.all_list.add_vacancy(vacancy)

        if 'SuperJob' in self.param['website']:
            if self.param['city'] != []:
                for item in range(len(self.param['city'])):
                    self.sj_api.add_area(self.param['city'][item])
            if self.param['words'] != []:
                self.sj_api.add_words(self.param['words'])
            self.sj_api.change_date(self.param['date'])

            vacancies_sj = self.sj_api.get_vacancies()

            if vacancies_sj != []:
                for item in vacancies_sj:
                   vacancy = Vacancy.create_vacancy_from_sj(item)
                   self.all_list.add_vacancy(vacancy)

        self.sorting_vacancies()

    def sorting_vacancies(self):
        while True:
            print(f'We found {len(self.all_list)} vacancies. We can sort or filter these. Choose what we should doing?')
            print('1 - Sorting vacancies on data')
            print('2 - Sorting vacancies on salary')
            print('3 - Filter word')
            print('4 - Filter salary')
            print('5 - Show all vacancies')
            print('6 - Save all vacancies in CSV-file')
            print('7 - Go to showing vacancies and adding in your favorite list')
            print('0 - Exit')

            user_input = input()

            if user_input == '0':
                self.__call__()
            elif user_input == '1':
                self.all_list.sorting_vacancies_data()
                self.showing_all_list_vacancies()
            elif user_input == '2':
                self.all_list.sorting_vacancies_salary()
                self.showing_all_list_vacancies()
            elif user_input == '3':
                print('Which word we should use for filtering?')
                word_filter = input().lower()
                self.all_list.filter_list_word(word_filter)
                self.showing_all_list_vacancies()
            elif user_input == '4':
                print('Which salary we should use for filtering?')
                while True:
                    salary = input()
                    if salary.isdigit():
                        self.all_list.filter_list_salary(int(salary))
                        self.showing_all_list_vacancies()
                        break
                    else:
                        print('Incorrect salary')
            elif user_input == '5':
                self.showing_all_list_vacancies()
            elif user_input == '6':
                path = self.all_list.save_csv()
                print(f'Your favorite vacancies were saved in CSV-file - {path}')
                self.__call__()
            elif user_input == '7':
                self.showing_all_list_vacancies()
                self.choosing_vacancies_in_my_list()
            else:
                print('Unknown command')

    def showing_all_list_vacancies(self):
        print(self.all_list)

    def choosing_vacancies_in_my_list(self):
        while True:
            print('Which vacancies are you choose? Write numbers (separated by space, fx "1 2 3 4 5"). You can write "all" for adding all vacancies in your favorite list.')
            numbers_vacancies = input().lower()
            if numbers_vacancies == '0':
                break
            elif numbers_vacancies == 'all':
                for vacancy in self.all_list.vacancy_list:
                    self.mylist.add_vacancy(vacancy)

                self.saving_my_list_vacancies()
            else:
                numbers = []

                numbers_str = numbers_vacancies.split()
                for number_str in numbers_str:
                    if number_str.isdigit():
                        numbers.append(int(number_str))
                if numbers == []:
                    print('Try again or press 0 for Exit')
                    continue

                for number in numbers:
                    if self.all_list.get_vacancy(number-1):
                        self.mylist.add_vacancy(self.all_list.get_vacancy(number-1))

                self.saving_my_list_vacancies()

    def saving_my_list_vacancies(self):
        while True:
            print(f'We added {len(self.mylist)} vacancies. We can save these or we can vake new research. Choose what we should doing?')
            print('1 - Save my favorite vacancies in CSV file')
            print('2 - Print my favorite vacancies')
            print('3 - New research')
            print('0 - Exit')

            user_input = input()

            if user_input == '0':
                self.__call__()
            elif user_input == '1':
                path = self.mylist.save_csv()
                print(f'Your favorite vacancies were saved in CSV-file - {path}')
                self.__call__()
            elif user_input == '2':
                print(self.mylist)
            elif user_input == '3':
                self.choosing_parameters()
            else:
                print('Unknown command')

    def delete_dublicates(self):
        self.param = {
            'website': list(set(self.param['website'])),
            'city': list(set(self.param['city'])),
            'words': list(set(self.param['words'])),
            'date': self.param['date']
        }

class Usertelebot:
    pass