from telebot.types import KeyboardButton

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
        :param name:
        :param step:
        :param quantity:
        :return:
        '''
        return KeyboardButton(config.KEYBOARD[name])
