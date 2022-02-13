from datetime import datetime
from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_base.db_core import Base
from models.order import Order
from models.product import Products
from settings import config, utility


class Singletone(type):
    '''
    Паттерн проектирования который позволяет создать один и только один объект класса
    '''
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singletone):
    '''
    класс менеджер для работы с базой
    '''
    def __init__(self):
        '''
        инициализация сессии и подключение к БД
        '''
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_product_category(self, category):
        '''
        возвращает все товары заданной категории
        '''
        result = self._session.query(Products).filter_by(
            category_id=category).all()
        self.close()
        print(result)
        return result

    def close(self):
        self._session.close()

    # работа с заказом
    def _add_orders(self, quantity, product_id, user_id,):
        '''
        метод заполнения заказа
        '''
        # получаем список всех product_id
        all_id_product = self.select_all_product_id()
        # если данные есть в списке, обновляем таблицы заказа и продуктов
        if product_id in all_id_product:
            quantity_order = self.select_order_quantity(product_id)
            quantity_order += 1
            self.update_order_value(product_id, 'quantity', quantity_order)

            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
            return
        # если данных нет, создаем новый объект заказа
        else:
            order = Order(quantity=quantity, product_id=product_id,
                          user_id=user_id, data=datetime.now())
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)

        self._session.add(order)
        self._session.commit()
        self.close()

    def select_all_product_id(self):
        '''
        возвращает все id товара в заказе
        '''
        result = self._session.query(Order.product_id).all()
        self.close()
        # конвертируем результат в вид [1,2,3]
        return utility._convert(result)

    def select_order_quantity(self, product_id):
        '''
        возвращает количество товара в заказе
        '''
        result = self._session.query(Order.quantity).filter_by(product_id=product_id).one()
        self.close()
        return result.quantity

    def select_single_product_quantity(self, rownum):
        '''
        возвращает колличество товара на складе в соответствии с номером товара - rownum
        номер определяется при выборе товара в интерфейсе
        '''
        result = self._session.query(Products.quantity).filter_by(id=rownum).one()
        self.close()
        return result.quantity

    def update_product_value(self, rownum, name, value):
        '''
        обновляет колличество товаров на складе
        '''
        self._session.query(Products).filter_by(id=rownum).update({name: value})
        self._session.commit()
        self.close()

    def update_order_value(self, product_id, name, value):
        '''
        обновляет данные указанной позиции заказа
        '''
        self._session.query(Order).filter_by(product_id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def select_single_product_name(self, rownum):
        '''
        возвращает название товара в соответствии с номером - rownum
        '''
        result = self._session.query(Products).filter_by(id=rownum).one()
        self.close()
        return result.name

    def select_single_product_title(self, rownum):
        '''
        возвращает торговую марку товара в соответствии с номером - rownum
        '''
        result = self._session.query(Products).filter_by(id=rownum).one()
        self.close()
        return result.title

    def select_single_product_price(self, rownum):
        '''
        возвращает цену товара в соответствии с номером - rownum
        '''
        result = self._session.query(Products).filter_by(id=rownum).one()
        self.close()
        return result.price

    # def select_order_quantity(self, product_id):
    #     '''
    #     возвращает колличество товара в заказе
    #     '''
    #     result = self._session.query(Order.quantity).filter_by(product_id=product_id).one()
    #     self.close()
    #     return result.quantity

    def count_rows_order(self):
        '''
        возвращает колличество позиций в заказе
        '''
        result = self._session.query(Order).count()
        self.close()
        return result
