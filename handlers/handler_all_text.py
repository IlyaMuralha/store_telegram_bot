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
        '''
        self.bot.send_message(message.chat.id, "Каталог категорий товара",
                              reply_markup=self.keyboards.remove_menu())
        self.bot.send_message(message.chat.id, "Сделайте свой выбор",
                              reply_markup=self.keyboards.category_menu())

    def pressed_btn_info(self, message):
        '''
        обработчик сообщений от нажатия на кнопку инфо
        '''
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode='HTML',
                              reply_markup=self.keyboards.info_menu())

    def pressed_btn_settings(self, message):
        '''
        обработчик сообщений от нажатия на кнопку settings
        '''
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode='HTML',
                              reply_markup=self.keyboards.settings_menu())

    def pressed_btn_back(self, message):
        '''
        обработчик сообщений от нажатия на кнопку back
        '''
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keyboards.start_menu())

    def pressed_btn_product(self, message, product):
        '''
        обработчик сообщений от нажатия на кнопку каталога товаров
        '''
        self.bot.send_message(message.chat.id, "Категория " + config.KEYBOARD[product],
                              reply_markup=self.keyboards.set_select_category(config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ok",
                              reply_markup=self.keyboards.category_menu())

    def pressed_btn_order(self, message):
        '''
        обработчик сообщений от нажатия на кнопку заказа
        '''
        # обнуляем данные шага
        self.step = 0
        # получаем список всех товаров в заказе
        count = self.DB.select_all_product_id()
        # получаем колличество по каждой позиции товара
        quantity = self.DB.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        '''
        отправляет ответ с заказом пользователю
        '''
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(self.step + 1), parse_mode='HTML')
        self.bot.send_message(message.chat.id, MESSAGES['order'].
                              format(self.DB.select_single_product_name(product_id),
                                     self.DB.select_single_product_title(product_id),
                                     self.DB.select_single_product_price(product_id),
                                     self.DB.select_order_quantity(product_id)),
                              parse_mode='HTML',
                              reply_markup=self.keyboards.orders_menu(self.step, quantity))

    def pressed_btn_up(self, message):
        '''
        обработчик сообщений от нажатия на кнопку up
        '''
        # получаем список всех товаров в заказе
        count = self.DB.select_all_product_id()
        # получаем колличество конкретной позиции в заказе
        quantity_order = self.DB.select_order_quantity(count[self.step])
        # получаем колличество конкретной позиции в продуктах
        quantity_product = self.DB.select_single_product_quantity(count[self.step])
        # если товар есть
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            # вносим изменения в БД orders
            self.DB.update_order_value(count[self.step], 'quantity', quantity_order)
            # вносим изменения в БД products
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)

        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_down(self, message):
        '''
        обработчик сообщений от нажатия на кнопку down
        '''
        # получаем список всех товаров в заказе
        count = self.DB.select_all_product_id()
        # получаем колличество конкретной позиции в заказе
        quantity_order = self.DB.select_order_quantity(count[self.step])
        # получаем колличество конкретной позиции в продуктах
        quantity_product = self.DB.select_single_product_quantity(count[self.step])
        # если товар есть
        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            # вносим изменения в БД orders
            self.DB.update_order_value(count[self.step], 'quantity', quantity_order)
            # вносим изменения в БД products
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)

        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_cancel_order(self, message):
        '''
        обработчик сообщений от нажатия на кнопку X удалить позицию шага
        '''
        # получаем список всех товаров в заказе
        count = self.DB.select_all_product_id()
        # если список не пуст
        if count.__len__() > 0:
            # получаем колличество конкретной позиции в заказе
            quantity_order = self.DB.select_order_quantity(count[self.step])
            # получаем колличество товара в конкретной позиции заказа
            quantity_product = self.DB.select_single_product_quantity(count[self.step])
            quantity_product += quantity_order
            # вносим изменения в БД orders
            self.DB.delete_order(count[self.step])
            # вносим изменения в БД products
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
            # уменьшаем шаг
            self.step -= 1

        count = self.DB.select_all_product_id()
        # если список не пуст
        if count.__len__() > 0:
            quantity_order = self.DB.select_order_quantity(count[self.step])
            # отправляем ответ пользователю
            self.send_message_order(count[self.step], quantity_order, message)
        else:
            # если товара нет в заказе отправляем сообщение
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode='HTML', reply_markup=self.keyboards.category_menu())

    def pressed_btn_back_step(self, message):
        '''
        обработчик сообщений от нажатия на кнопку back_step
        '''
        # уменьшаем шаг пока не будет равен "0"
        if self.step > 0:
            self.step -= 1
        # получаем список всех товаров в заказе
        count = self.DB.select_all_product_id()
        quantity_order = self.DB.select_order_quantity(count[self.step])
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_next_step(self, message):
        '''
        обрабатывает сообщения от нажатия на кнопку next_step
        '''
        if self.step < self.DB.count_rows_order() - 1:
            self.step += 1
        # получаем список всех товаров в заказе
        count = self.DB.select_all_product_id()
        quantity_order = self.DB.select_order_quantity(count[self.step])
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

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
            if message.text == config.KEYBOARD['ORDER']:
                # если есть заказ
                if self.DB.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode='HTML',
                                          reply_markup=self.keyboards.category_menu())

            # **********menu category********** #
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')
            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')
            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            # **********menu order********** #
            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)
            if message.text == config.KEYBOARD['DOWN']:
                self.pressed_btn_down(message)
            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_cancel_order(message)
            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)
            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)
