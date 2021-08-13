from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey
from DatabaseInstance import Base

class Bag(Base): 
	__tablename__  =  'member_book_bag' 
	bagId = Column("mb_id" ,  Integer, primary_key = True) 
	bookID = Column("b_id" , Integer, ForeignKey('books.b_bookID')) 
	memberID = Column("m_id" , Integer, ForeignKey('members.m_id')) 
	status = Column("b_status" ,Integer)
	checkout_date = Column("b_checkout_date" ,String(100))
	checkin_date = Column("b_checkin_date" ,String(100))	
	
	def __repr__(self):
		return f'<Bag {self.bookID!r}>'