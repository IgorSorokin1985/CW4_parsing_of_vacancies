from src.classes import HeadHunterAPI, Vacancy, Mylist

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

class Usertelebot:
    pass