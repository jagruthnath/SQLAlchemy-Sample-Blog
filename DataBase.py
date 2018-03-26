import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///Blog.db',echo = False)

class User(Base):
	__tablename__ = "blog_entries"

	Id = Column('Id', Integer, primary_key = True, autoincrement=True)
	Title = Column('Title',String(100))
	Message = Column('Message',String(500))
	Timestamp = Column('Timestamp',DateTime, default=func.now())
	
	def __init__(self,Title,Message):
		self.Title = Title
		self.Message = Message

	def insert(self):
		session=Session()
		session.add(self)
		session.commit()
	
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)