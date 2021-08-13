from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey
from DatabaseInstance import Base

class Inventory(Base): 
	__tablename__  =  'book_inventory'
	inventoryID = Column("in_id" ,  Integer, primary_key = True) 
	bookID = Column("in_bookID" , Integer, ForeignKey('books.b_bookID')) 
	count = Column("in_count" ,Integer)  
	checkout_count = Column("in_checkout_count" ,Integer)  
	
	def __repr__(self):
		return f'<Inventory {self.inventoryID!r}>'