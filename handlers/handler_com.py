# импортируем класс родитель
from handlers.handler import Handler
from settings import config


class HandlerCommands(Handler):
    '''
    класс обрабатывает входящие команды
    '''

    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        '''
        обработчик команды старт
        :param message:
        '''
        self.bot.send_message(message.chat.id,
                              f'{message.from_user.first_name},'
                              f'Здравствуйте, выберете команду!',
                              reply_markup=self.keyboards.start_menu())

    def handle(self):
        '''
        обоаботчик(декоратор) сообщений для входящих команд
        '''

        @self.bot.message_handler(commands=['start'])
        def handle(message):
            print(message)
            if message.text == '/start':
                self.pressed_btn_start(message)
