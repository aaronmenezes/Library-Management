from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from DatabaseInstance import Base

class Member(Base): 
	__tablename__  =  'members'
	id = Column("m_id" , Integer, primary_key = True) 
	first_name = Column("m_first_name" ,String(100)) 
	last_name = Column("m_last_name" ,String(100))
	dob = Column("m_dob" ,String(100))
	join_date = Column("m_join_date" ,String(100))
	
	def __repr__(self):
		return f'<Member {self.firstname!r}>'