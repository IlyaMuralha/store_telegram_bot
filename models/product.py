from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
# импортируем модуль для связки таблиц
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from models.category import Category

Base = declarative_base()


class Products(Base):
    '''
    класс для создания таблицы "товар"
    основан на декларативном методе sqlalchemy
    '''

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    title = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    is_active = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))

    # для каскадного удаления данных из таблицы
    category = relationship(
        Category,
        backref=backref('products',
                        uselist=True,
                        cascade='delete, all')
    )

    def __str__(self):
        return f'{self.name} {self.title} {self.price}'
