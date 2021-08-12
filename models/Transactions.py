from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from DatabaseInstance import Base

class Transactions(Base): 
	__tablename__  =  'transactions'
	
	t_id = Column("t_id", Integer, primary_key = True)
	m_id = Column("m_id", INTEGER,  ForeignKey('member.id') )
	book = Column("t_book",   ForeignKey('book.bookID') )
	amount = Column("t_amount", INTEGER)
	date = Column("t_date", String(100)) 
	
	
	def __repr__(self):
		return f'<Transactions {self.bookID!r}>'