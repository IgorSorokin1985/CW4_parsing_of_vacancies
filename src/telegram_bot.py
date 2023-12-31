from src.classes_api import HeadHunterAPI, SuperJobAPI
from src.class_vacancy import Vacancy
from src.class_mylist import Mylist
from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
import copy

class Userinput_telebot:
    new_param = {
            'website': [],
            'city': [],
            'words': [],
            'date': 14
        }

    TOKEN: str = os.getenv('TELEBOT_TOKEN')

    def __init__(self):
        self.hh_api = HeadHunterAPI()
        self.sj_api = SuperJobAPI()
        self.all_list = Mylist()
        self.param = copy.deepcopy(self.new_param)
        self.bot = Bot(self.TOKEN)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())

    def __call__(self):
        class Data_reserch(StatesGroup):
            choosing_websites = State()
            add_word = State()
            add_city = State()
            choose_number_days = State()
            sorting_vacancyes = State()

        b1 = KeyboardButton('/Research_vacancies')

        kb_client_1 = ReplyKeyboardMarkup(resize_keyboard=True)

        kb_client_1.add(b1)

        b4 = KeyboardButton('/HeadHunter')
        b5 = KeyboardButton('/SuperJob')
        b6 = KeyboardButton('/HeadHunter_and_SuperJob')
        kb_client_2 = ReplyKeyboardMarkup(resize_keyboard=True)

        kb_client_2.add(b4).add(b5).add(b6)

        kb_client_3 = ReplyKeyboardMarkup(resize_keyboard=True)
        b7 = KeyboardButton('/30_days')
        b8 = KeyboardButton('/14_days')
        b9 = KeyboardButton('/7_days')
        b10 = KeyboardButton('/1_day')

        kb_client_3.add(b7).add(b8).add(b9).add(b10)

        kb_client_4 = ReplyKeyboardMarkup(resize_keyboard=True)

        b11 = KeyboardButton('/Sorting_by_date')
        b12 = KeyboardButton('/Sorting_by_salary')

        kb_client_4.add(b11).add(b12)

        result = {}

        @self.dp.message_handler(commands=['start', 'help'])
        async def command_start(message: types.Message):
            await self.bot.send_message(message.from_user.id, 'GO!!!!', reply_markup=kb_client_1)

        @self.dp.message_handler(commands=['Research_vacancies'], state=None)
        async def command_start(message: types.Message):
            await Data_reserch.choosing_websites.set()
            await self.bot.send_message(message.from_user.id, 'We can research vacancies om HeadHunter and SuperJob. Which website you would like to choose?', reply_markup=kb_client_2)

        @self.dp.message_handler(content_types=['text'], state=Data_reserch.choosing_websites)
        async def input_websites(message: types.Message):

            if message.text == '/HeadHunter':
                self.param['website'].append('HeadHunter')
            elif message.text == '/SuperJob':
                self.param['website'].append('SuperJob')
            elif message.text == '/HeadHunter_and_SuperJob':
                self.param['website'].append('HeadHunter')
                self.param['website'].append('SuperJob')
            else:
                self.param['website'].append('HeadHunter')
                self.param['website'].append('SuperJob')

            await Data_reserch.next()
            await message.reply('Add word for researching', reply_markup=ReplyKeyboardRemove())

        @self.dp.message_handler(state=Data_reserch.add_word)
        async def input_word(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                self.param['words'].append(message.text.lower())
            await Data_reserch.next()
            await message.reply('Add city for researching (on russian)')

        @self.dp.message_handler(state=Data_reserch.add_city)
        async def input_city(message: types.Message):

            if self.check_city(message.text.lower()):
                self.param['city'].append(message.text.lower())
                await Data_reserch.next()
                await message.reply('Choose number of days for research', reply_markup=kb_client_3)
            else:

                await message.reply('Add city for researching (on russian)')


        @self.dp.message_handler(state=Data_reserch.choose_number_days)
        async def input_text4(message: types.Message):
            if message.text == '/30':
                self.param['date'] = 30
            elif message.text == '/14':
                self.param['date'] = 14
            elif message.text == '/7':
                self.param['date'] = 7
            elif message.text == '/1':
                self.param['date'] = 1
            else:
                self.param['date'] = 7

            self.research()
            await Data_reserch.next()
            await message.reply(f'We found {len(self.all_list)} vacancies. How we should sort vacancies?', reply_markup=kb_client_4)

        @self.dp.message_handler(state=Data_reserch.sorting_vacancyes)
        async def input_city(message: types.Message):

            if message.text == '/Sorting_by_date':
                self.all_list.sorting_vacancies_data()
            elif message.text == '/Sorting_by_salary':
                self.all_list.sorting_vacancies_salary()
            else:
                pass

            for index, vacancy in enumerate(self.all_list.vacancy_list[:10]):
                await self.bot.send_message(message.from_user.id, f'Vacancy N {index+1}\nName - {vacancy.name}\nUrl - {vacancy.url}', reply_markup=kb_client_1)

            path = self.all_list.save_xlsx()

            await message.reply_document(open(path, 'rb'))

            await self.bot.send_message(message.from_user.id,
                                        f'I showed few vacancies late, in file all vacancies.',
                                        reply_markup=kb_client_1)

            self.all_list.clear_list()
            await Data_reserch.next()

        @self.dp.message_handler()
        async def echo_send(message: types.Message):
           await message.answer("Unknown command!")

        executor.start_polling(self.dp, skip_updates=True)

    def research(self):
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

        self.param = copy.deepcopy(self.new_param)

    def check_city(self, user_input:str):
        """
        Checking city from user
        :param user_input: str
        :return: True or False
        """
        if self.hh_api.saver_areas.open_and_find_info(user_input) or self.sj_api.saver_areas.open_and_find_info(user_input):
            return True
        else:
            return False
