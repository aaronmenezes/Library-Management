from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from DatabaseInstance import Base

class Book(Base): 
	__tablename__  =  'books' 

	bookID = Column("b_bookID", Integer, primary_key = True)
	title = Column("b_title", String(100))
	authors = Column("b_authors", String(100))
	average_rating = Column("b_average_rating", String(100))
	isbn = Column("b_isbn", String(100))
	isbn13 = Column("b_isbn13", String(100))
	language_code = Column("b_language_code", String(100))
	num_pages = Column("b_num_pages", String(100))
	ratings_count = Column("b_ratings_count", String(100))
	text_reviews_count = Column("b_text_reviews_count", String(100))
	publication_date = Column("b_publication_date", String(100))
	publisher = Column("b_publisher", String(100))
	
	
	def __repr__(self):
		return f'<Book {self.title!r}>'