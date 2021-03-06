from sqlalchemy import Column, String, Integer, Boolean
from data_base.db_core import Base
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()


class Category(Base):
    '''
    Класс-модель описывает сущность категорий
    '''
    #
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_active = Column(Boolean)

    def __str__(self):
        '''
        метод возвращает строковое представление объекта класса
        :return:
        '''
        return self.name
