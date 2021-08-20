from models.DBConnect import init_db,shutdown_session,db_session,Base 
from models.Book import Book 
from models.Inventory import Inventory
from models.Member import Member
from models.Bag import Bag
from models.Transactions import Transactions
from sqlalchemy import func

class DatabaseInstance:
    __instance = None 
    
    @staticmethod
    def getInstance():
        """ Static access method. """
        if DatabaseInstance.__instance == None:
            DatabaseInstance()
        return DatabaseInstance.__instance

    def __init__(self): 
        if DatabaseInstance.__instance != None:
            raise Exception("This class is a DatabaseInstance!")
        else:
            DatabaseInstance.__instance = self
            init_db()  
    
        
    def add_all_books(self,book_list): 
        for item in book_list: 
            book = Book(**item) 
            db_session.add(book)
        db_session.commit()
        return []
        
    def get_all_books(self):        
        booklist = db_session.query(Book).all()
        return booklist    
    
    def get_checked_books(self):
        baglist = db_session.query(Bag,Book,Member).join(Book,Book.bookID==Bag.bookID).join(Member,Member.id==Bag.memberID).order_by(Bag.bagId.desc()).all()
        return baglist   
    
    def get_books_inventory(self):
        inventory = db_session.query(Inventory,Book).join(Book,Book.bookID==Inventory.bookID).all()
        return inventory
    
    def add_book(self,book_item):
        db_session.add(Book(**book_item))
        db_session.commit()

    def delete_book(self,bookid):
        Book.query.filter_by(bookID=bookid).delete()
        Inventory.query.filter_by(bookID=bookid).delete()
        Bag.query.filter_by(bookID=bookid).delete()
        db_session.commit()
        return []
        
    def update_book_details(self,bookid,book_vals):
        db_session.query(Book).filter(Book.bookID == bookid).update(book_vals)
        db_session.commit() 
        return []

    def add_items_to_inventory(self,inventory_list ):  
        for item in inventory_list: 
            inventory = Inventory(**item) 
            db_session.add(inventory)
        db_session.commit()
        return []
        
    def add_item_to_inventory(self,inventory_item ):   
        db_session.add(Inventory(**inventory_item) )
        db_session.commit()
        return []
    
    def update_inventory_item(self,book_id,count):
        db_session.query(Inventory).filter(Inventory.bookID == book_id).update({'count':count})
        db_session.commit()
        return []
    
    def get_invetory_count(self,book_list):
        inventory_count_list = db_session.query(Inventory).filter(Inventory.bookID.in_(book_list)).all() 
        return inventory_count_list;
        
    def get_member(self,userid):
        member = db_session.query(Member).filter_by(user_id=userid).first()
        return member
        
    def add_member(self,user_id,psswd,f_name,l_name,dob,joindate):
        db_session.add(Member(user_id=user_id,psswd=psswd,first_name = f_name,last_name= l_name,dob= dob,join_date= joindate))
        db_session.commit()
        return ""
        
    def get_member_list(self):
        member_list = db_session.query(Member).filter(Member.role == "member").all() 
        return member_list        
    
    def update_member_details(self,memberid,member_vals):
        db_session.query(Member).filter(Member.id == memberid).update(member_vals)
        db_session.commit() 
        return []

    def delete_member(self,memberid):
        Member.query.filter_by(id=memberid).delete() 
        Bag.query.filter_by(memberID=memberid).delete()
        db_session.commit()
        return []

    def book_checkout(self,member_id,book_id,date,amount): 
        inventory_item = db_session.query(Inventory).filter_by(bookID=int(book_id)).first() 
        member = db_session.query(Member).filter_by(id=member_id).first() 
        if member.debt >=500:
            return {"status":"fail","msg":"Memebr Debt 500"}
        if inventory_item.checkout_count < inventory_item.count:
            inventory_item.checkout_count = inventory_item.checkout_count+1
            db_session.add(Bag(bookID = book_id,memberID=member_id,status = 1,checkout_date=date))
            member.debt = member.debt +amount;
            db_session.commit()
            return {"status":"success"}
        else :
            return {"status":"fail","msg":"Insufficient stock"}

    def book_checkin(self,member_id,book_id,bagId,date,amount):
        inventory_item = db_session.query(Inventory).filter_by(bookID=int(book_id)).first() 
        member = db_session.query(Member).filter_by(id=member_id).first()     
        if member.debt >100:
            member.debt = member.debt - amount;
            db_session.add(Transactions(m_id=member_id,book = book_id,amount=amount,date= date))            
        inventory_item.checkout_count = inventory_item.checkout_count-1
        db_session.query(Bag).filter(Bag.memberID == member_id , Bag.bookID == book_id,Bag.bagId==bagId ).update({'checkin_date':date,'status':0}) 
        db_session.commit()
        return []

    def get_top_books(self): 
        result = db_session.query(func.count(Bag.bookID).label("rank_count"),Book,Inventory.count,Inventory.checkout_count).group_by(Bag.bookID).join(Book,Book.bookID==Bag.bookID).join(Inventory,Inventory.bookID==Bag.bookID).order_by("rank_count").all()
        return result

    def get_top_spenders(self): 
        result = db_session.query(func.sum(Transactions.amount).label("spend_amount"),Member).group_by(Member.id).join(Member,Member.id==Transactions.m_id).order_by("spend_amount").all() 
        return result
		
    def get_all_transactions(self): 	
        transactions = db_session.query(Transactions,Member).join(Member,Member.id==Transactions.m_id).all() 
        return transactions

    def remove(self):
        shutdown_session()