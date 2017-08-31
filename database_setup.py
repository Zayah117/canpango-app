import sys
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    password_hash = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'password_hash': self.password_hash
        }


class Beer(Base):
    __tablename__ = 'bear'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ibu = Column(Integer, nullable=False)
    calories = Column(Integer, nullable=False)
    abv = Column(Float, nullable=False)
    style = Column(String(80), nullable=False)
    brewery_location = Column(String(80), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'IBU': self.ibu,
            'calories': self.calories,
            'ABV': self.abv,
            'style': self.style,
            'brewery_location': self.brewery_location
        }


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    aroma = Column(Integer, nullable=False)
    appearance = Column(Integer, nullable=False)
    taste = Column(Integer, nullable=False)
    overall = Column(Integer, nullable=False)


engine = create_engine('sqlite:///data.db')
Base.metadata.create_all(engine)
