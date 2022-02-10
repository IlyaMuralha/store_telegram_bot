from sqlalchemy import Column, Integer, DateTime, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from data_base.db_core import Base
from models.product import Products

# Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    created = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer)

    products = relationship(
        Products,
        backref=backref('products',
                        uselist=True,
                        cascade='delete, all')
    )

    def __str__(self):
        return f'{self.quantity} {self.created}'
