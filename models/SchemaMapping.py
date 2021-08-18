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

class Member(Schema):  
    id = fields.Int()
    first_name = fields.Str()     
    last_name = fields.Str()    
    user_id = fields.Str()
    psswd = fields.Str() 
    dob = fields.Str()
    join_date = fields.Str()
    role = fields.Str()
    
class Bag(Schema): 
    bagId = fields.Int()
    bookID = fields.Int()
    memberID = fields.Int()
    status = fields.Int()
    checkout_date = fields.Str() 
    checkin_date = fields.Str() 
    
class CheckedBooks(Schema): 
    bag_item = fields.Nested(Bag)
    book_item = fields.Nested(Book)
    member_item = fields.Nested(Member,exclude={"psswd"})

class InventoryView(Schema): 
    inventory_item = fields.Nested(Inventory)
    book_item = fields.Nested(Book)
