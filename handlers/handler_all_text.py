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

    def handle(self):
        '''
        обоаботчик(декоратор) сообщений для входящих команд
        '''

        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)
            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)
            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)
