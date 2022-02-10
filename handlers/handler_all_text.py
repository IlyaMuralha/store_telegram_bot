from handlers.handler import Handler
from settings import config
from settings.message import MESSAGES


class HandlerAllText(Handler):
    '''
    класс обрабатывает входящие текстовые сообщения от нажатия кнопок
    '''

    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_category(self, message):
        '''
        обработчик сообщений от нажатия на кнопку choose product
        :param message:
        '''
        self.bot.send_message(message.chat.id, "Каталог категорий товара",
                              reply_markup=self.keyboards.remove_menu())
        self.bot.send_message(message.chat.id, "Сделайте свой выбор",
                              reply_markup=self.keyboards.category_menu())

    def pressed_btn_info(self, message):
        '''
        обработчик сообщений от нажатия на кнопку инфо
        :param message:
        '''
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode='HTML',
                              reply_markup=self.keyboards.info_menu())

    def pressed_btn_settings(self, message):
        '''
        обработчик сообщений от нажатия на кнопку settings
        :param message:
        '''
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode='HTML',
                              reply_markup=self.keyboards.settings_menu())

    def pressed_btn_back(self, message):
        '''
        обработчик сообщений от нажатия на кнопку back
        :param message:
        '''
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keyboards.start_menu())

    def pressed_btn_product(self, message, product):
        '''
        обработчик сообщений от нажатия на кнопку каталога товаров
        :param message:
        :param product
        '''
        self.bot.send_message(message.chat.id, "Категория " + config.KEYBOARD[product],
                              reply_markup=self.keyboards.set_select_category(config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ok",
                              reply_markup=self.keyboards.category_menu())

    def handle(self):
        '''
        обоаботчик(декоратор) сообщений для входящих команд
        '''

        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            # **********menu********** #
            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)
            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)
            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            # **********menu category********** #
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')
            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')
            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')
