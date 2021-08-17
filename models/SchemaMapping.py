from marshmallow import Schema, fields

class Book(Schema):
    name = fields.Str()
    bookID = fields.Int()
    title = fields.Str()
    authors = fields.Str()
    average_rating = fields.Str()
    isbn = fields.Str()
    isbn13 = fields.Str()
    language_code = fields.Str()
    num_pages = fields.Str()
    ratings_count = fields.Str()
    text_reviews_count = fields.Str()
    publication_date = fields.Str()
    publisher = fields.Str()
    

class Inventory(Schema): 
    inventoryID = fields.Int()
    bookID = fields.Int()
    count = fields.Int()
    checkout_count = fields.Int() 


class Bag(Schema): 
    bagId = fields.Int()
    bookID = fields.Int()
    memberID = fields.Int()
    status = fields.Int()
    checkout_date = fields.Str() 
    checkin_date = fields.Str() 
