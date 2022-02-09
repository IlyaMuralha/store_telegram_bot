from handlers.handler_com import HandlerCommands


class HandlerMain:
    '''
    класс компановщик хэндлеров
    '''
    def __init__(self, bot):
        # получаем нашего бота
        self.bot = bot
        # инициализируем обработчик команд
        self.handler_commands = HandlerCommands(self.bot)

    def handle(self):
        self.handler_commands.handle()
