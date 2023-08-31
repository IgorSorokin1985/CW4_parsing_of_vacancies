from src.classes import HeadHunterAPI
import json

class Userinput:
    def __init__(self):
        self.hh_api = HeadHunterAPI()

    def __call__(self):
        while True:
            self.__info()
            user_input = input()
            if user_input == '0':
                break
            elif user_input == '1':
                city = input('Add city for researching\n')
                self.hh_api.add_area(city)
            elif user_input == '2':
                word = input('Add word for researching\n')
                self.hh_api.add_text(word)
            elif user_input == '3':
                vacancies = self.hh_api.get_vacancies()
                print(json.dumps(vacancies, indent=2, ensure_ascii=False))
                print(len(vacancies['items']))
            elif user_input == '4':
                pass
            elif user_input == '5':
                pass
            else:
                print('Unknown command')


    def __info(self):
        print('Commands:')
        print('1 - Choose city')
        print('2 - Add words for research')
        print('3 - Research vacancies')
        print('4 - Choose vacancy for adding in MyList')
        print('5 - Show MyList')
        print('0 - Exit')

class Usertelebot:
    pass