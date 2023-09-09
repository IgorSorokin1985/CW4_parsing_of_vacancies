from src.classes import HeadHunterAPI, Vacancy, Mylist, SuperJobAPI

class Userinput:
    def __init__(self):
        self.hh_api = HeadHunterAPI()
        self.all_list = Mylist()
        self.mylist = Mylist()


    def __call__(self):
        while True:
            self.__info()
            user_input = input()

            if user_input == '0':
                break

            elif user_input in ['1', '2', '3']:
                self.research()

            elif user_input == '4':
                self.choosing()

            elif user_input == '5':
                self.showing()

            elif user_input == '6':
                self.saving()

            else:
                print('Unknown command')

    def research(self):
        city = input('Add city for researching\n')
        self.hh_api.add_area(city)

        word = input('Add word for researching\n')
        self.hh_api.add_text(word)

        vacancies = self.hh_api.get_vacancies()
        count = 1
        for item in vacancies:
            vacancy = Vacancy(item)
            print(f'{count}\n{vacancy}')
            count += 1
            self.all_list.add_vacancy(vacancy)

    def choosing(self):
        numbers_vacancies = input('Which vacancies are you choose? Write number.')
        numbers = []
        if ' ' in numbers_vacancies:
            numbers_str = numbers_vacancies.split()
            for number_str in numbers_str:
                numbers.append(int(number_str))
            for number in numbers:
                self.mylist.add_vacancy(self.all_list.get_vacancy(number))

    def showing(self):
        print(self.mylist)

    def sorting(self):
        for item in self.mylist.sorting_vacancies('salary_to'):
            print(item)

    def saving(self):
        pass

    def __info(self):
        print('Commands:')
        print('1 - Choose city')
        print('2 - Add words for research')
        print('3 - Research vacancies')
        print('4 - Choose vacancy for adding in MyList')
        print('5 - Show MyList')
        print('6 - Sorting MyList')
        print('0 - Exit')

class Userinput_2:
    new_param = {
            'website': [],
            'city': [],
            'words': [],
            'data': ''
        }
    def __init__(self):
        self.hh_api = HeadHunterAPI()
        self.sj_api = SuperJobAPI()
        self.all_list = Mylist()
        self.mylist = Mylist()
        self.param = self.new_param

    def __call__(self):
        while True:
            self.__info()
            user_input = input()

            if user_input == '0':
                break
            elif user_input == '1':
                self.choosing_parameters()
            else:
                print('Unknown command')

    def choosing_parameters(self):
        self.param = self.new_param
        while True:
            self.delete_dublicates()
            print('You need choose websites, city, date and words for research')

            if self.param['website'] != []:
                print(f"You choosed next website - {', '.join(self.param['website'])}")
            if self.param['city'] != []:
                print(f"You choosed next city - {', '.join(self.param['city'])}")
            if self.param['words'] != []:
                print(f"You choosed next words - {', '.join(self.param['words'])}")
            print('1 - choose websites')
            print('2 - add words for research')
            print('3 - choose city')
            print('4 - research vacancies')
            print('0 - Exit')
            user_input = input()

            if user_input == '0':
                break
            elif user_input == '1':
                self.choosing_website()
            elif user_input == '2':
                self.choosing_words()
            elif user_input == '3':
                self.choosing_city()
            elif user_input == '4':
                self.research()
            else:
                print('Unknown command')

        vacancies = self.hh_api.get_vacancies()
        count = 1
        for item in vacancies:
            vacancy = Vacancy(item)
            print(f'{count}\n{vacancy}')
            count += 1
            self.all_list.add_vacancy(vacancy)

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
            print('Add word for researching or press 0 for Exit')
            user_input = input().lower()
            if user_input == '0':
                break
            else:
                self.param['words'].append(user_input)

        #self.hh_api.add_text(word)

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

        #self.hh_api.add_area(city)

    def check_city(self, user_input):
        if user_input in self.hh_api.areas or user_input in self.sj_api.areas:
            return True
        else:
            return False

    def research(self):
        vacancies = self.hh_api.get_vacancies()
        count = 1
        for item in vacancies:
            vacancy = Vacancy(item)
            print(f'{count}\n{vacancy}')
            count += 1
            self.all_list.add_vacancy(vacancy)
        self.sorting()

    def sorting(self):
        while True:
            print(f'We found {len(self.all_list)} vacancies. We can sort or filter these. Choose what we should doing?')
            print('1 - Sorting vacancies')
            print('2 - Filter')
            print('3 - Go to show vacancies and add in your favorite list')

            user_input = input()

            if user_input == '0':
                break
            elif user_input == '1':
                for item in self.mylist.sorting_vacancies('salary_to'):
                    print(item)
            elif user_input == '2':
                pass
            elif user_input == '3':
                self.showing()
            else:
                print('Unknown command')

    def showing(self):
        print(self.mylist)

    def choosing_vacancies(self):
        numbers_vacancies = input('Which vacancies are you choose? Write number.')
        numbers = []
        if ' ' in numbers_vacancies:
            numbers_str = numbers_vacancies.split()
            for number_str in numbers_str:
                numbers.append(int(number_str))
            for number in numbers:
                self.mylist.add_vacancy(self.all_list.get_vacancy(number))

    def saving(self):
        pass

    def delete_dublicates(self):
        self.param = {
            'website': list(set(self.param['website'])),
            'city': list(set(self.param['city'])),
            'words': list(set(self.param['words'])),
            'data': ''
        }

    def __info(self):
        print('Commands:')
        print('1 - Research vacancies')
        print('0 - Exit')

class Usertelebot:
    pass