from telebot import TeleBot
from settings import config
from handlers.handler_main import HandlerMain


class StoreBot:
    '''
    Основной класс бота(сервер) на основе библиотеки PyTelegramBotApi
    '''
    __version__ = config.VERSION
    __author__ = config.VERSION

    def __init__(self):
        self.token = config.TOKEN
        self.bot = TeleBot(self.token)
        self.handler = HandlerMain(self.bot)

    def start(self):
        '''
        метод для старта обработчика событий
        :return:
        '''
        self.handler.handle()

    def run_bot(self):
        '''
        запускаем основные события сервера
        :return:
        '''
        self.start()
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    bot = StoreBot()
    bot.run_bot()
