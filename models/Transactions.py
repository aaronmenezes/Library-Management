from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey
from DatabaseInstance import Base

class Transactions(Base): 
	__tablename__  =  'transactions'
	
	t_id = Column("t_id", Integer, primary_key = True)
	m_id = Column("m_id", Integer, ForeignKey('members.m_id'))
	book = Column("t_book",Integer, ForeignKey('books.b_bookID') )
	amount = Column("t_amount", Integer)
	date = Column("t_date", String(100)) 
	
	
	def __repr__(self):
		return f'<Transactions {self.bookID!r}>'