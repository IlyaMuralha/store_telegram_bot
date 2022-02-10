from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_base.db_core import Base
from models.product import Products
from settings import config


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
