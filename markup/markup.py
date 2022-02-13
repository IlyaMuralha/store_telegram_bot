from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup

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

        if name == 'AMOUNT_ORDERS':
            config.KEYBOARD['AMOUNT_ORDERS'] = '{} {} {}'.format(step + 1, ' из ', str(self.DB.count_rows_order()))
        if name == 'AMOUNT_PRODUCT':
            config.KEYBOARD['AMOUNT_PRODUCT'] = f'{quantity}'

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

    def info_menu(self):
        '''
        метод создаёт и возвращает разметку кнопок для команды "info"
        '''
        self.markup = ReplyKeyboardMarkup(True, True)
        back_btn = self.set_btn('<<')
        # расположение кнопок в меню
        self.markup.row(back_btn)
        return self.markup

    def settings_menu(self):
        '''
        метод создаёт и возвращает разметку кнопок для команды "settings"
        '''
        self.markup = ReplyKeyboardMarkup(True, True)
        back_btn = self.set_btn('<<')
        # расположение кнопок в меню
        self.markup.row(back_btn)
        return self.markup

    def remove_menu(self):
        return ReplyKeyboardRemove()

    def category_menu(self):
        '''
        метод создаёт и возвращает разметку кнопок для команды "выбрать продукт"
        '''
        self.markup = ReplyKeyboardMarkup(True, True, row_width=1)
        self.markup.add(self.set_btn('SEMIPRODUCT'))
        self.markup.add(self.set_btn('GROCERY'))
        self.markup.add(self.set_btn('ICE_CREAM'))
        self.markup.row(self.set_btn('<<'), self.set_btn('ORDER'))
        return self.markup

    def set_inline_btn(self, name):
        '''
        создает и возвращает инлайн кнопку под входные параметры
        '''
        print('create inline-button')
        return InlineKeyboardButton(str(name),
                                    callback_data=str(name.id))

    def set_select_category(self, category):
        '''
        создаем и возвращаем разметку инлайн-кнопок выбранной категории
        '''
        self.markup = InlineKeyboardMarkup(row_width=1)
        # загружаем в название инлайн кнопок данные
        # из БД в соответствии с категорией
        for itm in self.DB.select_all_product_category(category):
            self.markup.add(self.set_inline_btn(itm))

        return self.markup

    def orders_menu(self, step, quantity):
        '''
        метод создаёт и возвращает разметку кнопок для команды "заказ"
        '''
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_cancel_order = self.set_btn('X', step, quantity)
        itm_btn_down = self.set_btn('DOWN', step, quantity)
        itm_btn_amount_product = self.set_btn('AMOUNT_PRODUCT', step, quantity)
        itm_btn_up = self.set_btn('UP', step, quantity)

        itm_btn_back_step = self.set_btn('BACK_STEP', step, quantity)
        itm_btn_amount_orders = self.set_btn('AMOUNT_ORDERS', step, quantity)
        itm_btn_next_step = self.set_btn('NEXT_STEP', step, quantity)
        itm_btn_back = self.set_btn('<<', step, quantity)
        itm_btn_pay = self.set_btn('APPLAY', step, quantity)

        self.markup.row(itm_btn_cancel_order, itm_btn_down, itm_btn_amount_product, itm_btn_up)
        self.markup.row(itm_btn_back_step, itm_btn_amount_orders, itm_btn_next_step)
        self.markup.row(itm_btn_back, itm_btn_pay)

        return self.markup

