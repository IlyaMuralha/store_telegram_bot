from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from settings import config
from data_base.dbalchemy import DBManager


class Keyboards:
    '''
    класс предназначен для создания разметки бота
    '''
    def __init__(self):
        self.markup = None
        self.DB = DBManager()

    def set_btn(self, name, step=0, quantity=0):
        '''
        Создаёт и возвращает кнопку по входным параметрам
        '''
        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):
        '''
        метод создаёт и возвращает разметку кнопок для команды "/start"
        '''
        self.markup = ReplyKeyboardMarkup(True, True)
        choose_goods_btn = self.set_btn('CHOOSE_GOODS')
        info_btn = self.set_btn('INFO')
        setting_btn = self.set_btn('SETTINGS')
        # расположение кнопок в меню
        self.markup.row(choose_goods_btn)
        self.markup.row(info_btn, setting_btn)
        return self.markup

