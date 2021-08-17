from models.DBConnect import init_db,shutdown_session,db_session,Base 
from models.Book import Book 
from models.Inventory import Inventory
from models.Member import Member
from models.Bag import Bag
 
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
        booklist = db_session.query(Bag).outerjoin(Book,Book.bookID==Bag.bookID).all()
        return booklist    
    
    def add_items_to_inventory(self,inventory_list ):  
        for item in inventory_list: 
            inventory = Inventory(**item) 
            db_session.add(inventory)
        db_session.commit()
        return []
    
    def update_inventory_item(self,book_id,count):
        db_session.query(Inventory).filter(Inventory.bookID == book_id).update({'count':count})
        db_session.commit()
        return []
    
    def get_member(self,userid):
        member = db_session.query(Member).filter_by(user_id=userid).first()
        return member
        
    def add_member(self,user_id,psswd,f_name,l_name,dob,joindate):
        db_session.add(Member(user_id=user_id,psswd=psswd,first_name = f_name,last_name= l_name,dob= dob,join_date= joindate))
        db_session.commit()
        return ""
        
    def book_checkout(self,member_id,book_id,date):
        #check debt         
        inventory_item = db_session.query(Inventory).filter_by(bookID=int(book_id)).first()
        print(inventory_item.checkout_count < inventory_item.count)
        if inventory_item.checkout_count < inventory_item.count:
            inventory_item.checkout_count = inventory_item.checkout_count+1
            db_session.add(Bag(bookID = book_id,memberID=member_id,status = 1,checkout_date=date))
            db_session.commit()
        return []

    def book_checkin(self,book_id,member_id,date):
        inventory_item = db_session.query(Inventory).filter_by(bookID=int(book_id)).first()  
        inventory_item.checkout_count = inventory_item.checkout_count-1
        db_session.query(Bag).filter(Bag.memberID == member_id , Bag.bookID == book_id ).update({'checkin_date':date,'status':0}) 
        db_session.commit()
        return []
        
    def remove(self):
        shutdown_session()
'''
    def get_all_notes(self):
        cur= self.get_db().cursor()
        cur.execute("SELECT * from NOTES_VIEW")
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return r
    
    def get_all_notes_list(self):
        cur= self.get_db().cursor()
        cur.execute("SELECT * from note_list")
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return r 
    
    def add_new_note(self,name,date,priority,body):
        cur= self.get_db().cursor()
        cur.execute("INSERT INTO note_list  (name, date, priority )  VALUES (?,?,?)",(name,date,priority))        
        r = cur.execute("SELECT MAX(id) FROM note_list")
        note_id =r.fetchone()[0] or 0
        cur.execute("INSERT INTO notes  (key, body )  VALUES (?,?)",(note_id,body))                
        self.get_db().commit()
        return []

    def update_note(self,id,name,body):
        cur= self.get_db().cursor()
        cur.execute("UPDATE note_list SET name = '"+name+"' WHERE id = "+id) 
        cur.execute("UPDATE notes SET body = ? WHERE key = ? ",(body,id))  
        self.get_db().commit()
        return []        

    def update_note_priority(self,id,priority):
        cur= self.get_db().cursor()
        cur.execute("UPDATE note_list SET priority = '"+priority+"' WHERE id = "+id) 
        self.get_db().commit()
        return []
        
    def delete_note(self,id):
        cur= self.get_db().cursor()
        cur.execute("""INSERT INTO note_archive (key, name,body,priority,date)
                        SELECT key, name,body,priority,date
                        FROM   NOTES_VIEW where key="""+id)    
        cur.execute("DELETE from note_list WHERE id = "+id)
        cur.execute("DELETE from notes WHERE key = "+id)
        self.get_db().commit()
        return []        
    
    def get_note_archive(self):
        cur= self.get_db().cursor()
        cur.execute("SELECT * from note_archive")
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return r
    
     
    
    def get_home_category(self):
        cur= self.get_db().cursor()
        cur.execute("SELECT cid as _id,cid, title,parentcid,category_attr_template_id, lid,category_synopsis_filename_21 as poster FROM v_categories where parentcid="+self.home_node+" and lid="+self.cur_lid)
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return r
        
    def get_featured_category(self):
        cur= self.get_db().cursor()
        cur.execute("SELECT mid as _id, mid,title,rating_name,genre,duration,media_synopsis_filename_21 as synopsisposter FROM v_categorymedia where cid in (SELECT cid FROM v_categories where category_attr_template_id='featured' and lid="+self.cur_lid+") and lid="+self.cur_lid)
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return r
        
    def get_device_list(self):
        cur= self.get_db().cursor()
        cur.execute("SELECT mid as _id, mid,title,description,cast_list,rating,genre,duration,media_poster_filename_21 as poster,media_poster_filename_11 as synopsisposter FROM v_categorymedia where cid=36 and lid=1 limit 10")
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return r
        
    def get_media_model(self,cid):
        cur= self.get_db().cursor()
        cur.execute("SELECT mid as _id, mid,title,description,cast_list,rating,genre,duration,media_poster_filename_21 as poster,media_poster_filename_11 as synopsisposter FROM v_categorymedia where cid in (SELECT cid FROM v_categories where cid="+cid+" and lid="+self.cur_lid+") and lid= "+self.cur_lid +" order by title")
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return r

    def get_video_model(self,cid):
        cur= self.get_db().cursor()
        cur.execute("SELECT cid as _id,cid, title,parentcid,category_attr_template_id, lid,category_synopsis_filename_21 as poster FROM v_categories where parentcid="+cid+" and lid="+self.cur_lid)
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return r

    def get_tracklist_model(self,aggMid):
        cur= self.get_db().cursor()
        cur.execute("select mid as _id, mid,title,duration,artist,media_type,rating,aggregate_parentmid from  v_media_aggs as v_ma where lid="+self.cur_lid+" and aggregate_parentmid="+aggMid+" order by aggregate_order")
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return r

    def get_synopsis_model(self , mid , cid , scid):
        self.log_user_selection(mid , cid , scid)
        cur= self.get_db().cursor()
        cur.execute("SELECT mid,title,description,cast_list,rating,genre,duration,media_poster_filename_21 as poster,media_poster_filename_11 as synopsisposter FROM v_categorymedia where mid="+mid+" and lid="+self.cur_lid + " limit 1")
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return r    
    
    def get_search_media(self,title):
        cur= self.get_db().cursor()
        cur.execute("SELECT  DISTINCT title ,mid,description,cast_list,rating,genre,duration,media_poster_filename_21 as poster,media_poster_filename_11 as synopsisposter FROM v_categorymedia where title LIKE '"+title+"%' and lid="+self.cur_lid )
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return r

    def update_poster_entry(self,mid,filename):
        cur= self.get_db().cursor()  
        cur.execute("UPDATE media SET media_poster_filename_21 = '"+filename+"' WHERE mid = "+mid)  
        cur.execute("DROP VIEW v_categorymedia")
        cur.execute('CREATE VIEW "v_categorymedia" AS  \
                    SELECT \
                    f.media_config_id, f.categorymedia_startdate, f.categorymedia_enddate, f.cid, f.categorymedia_order, f.categorymedia_purpose, f.categorymedia_accesstype, f.categorymedia_price, f.categorymedia_channel, f.categorymedia_channelnum,\
                    m.mid, m.media_type, m.contenttype, m.uniqueid, m.groupid, m.duration, m.aspect, m.filename, m.rating, m.rating_name, m.soundtrack_count, m.soundtrack_list, m.subtitle_count,\
                    m.subtitle_list, m.child_count, m.media_attr_associate_music, m.media_attr_channel, m.media_attr_contenttype, m.media_attr_mediatype, m.media_poster_filename_11,\
                    m.media_synopsis_filename_11, m.media_poster_filename_12, m.media_synopsis_filename_12, m.media_poster_filename_21, m.media_synopsis_filename_21, m.media_poster_filename_22, \
                    m.media_synopsis_filename_22, m.media_poster_filename_33, m.media_synopsis_filename_33, m.media_poster_filename_34, m.media_synopsis_filename_34, m.media_navthumb_filename_1,\
                    mll.lid,\
                    ml.media_label_id, ml.label_lid, ml.title, ml.short_title, ml.description, ml.short_description, ml.cast as cast_list, ml.director, ml.artist, ml.author, ml.publisher, ml.narrator, ml.year, ml.genre, ml.copyright, ml.review, ml.country, ml.numberofplayers, ml.datetext, ml.numberofpages, ml.language, ml.isbn, ml.launchlang, ml.resolution, ml.critic_score, ml.people_score, ml.trailer_mid, ml.trailer_duration, ml.trailer_soundtrack_count, ml.trailer_soundtrack_list, ml.search_title, ml.search_director, ml.search_cast, ml.search_artist \
                    FROM categorymedia f, media m, media_label_lookups mll, media_labels ml \
                    WHERE f.mid = m.mid AND m.mid = mll.mid AND mll.media_label_id = ml.media_label_id')
        self.get_db().commit()
    
    def log_user_selection(self,mid,cid,scid):
            cur= self.get_db().cursor()
            cur.execute("SELECT DISTINCT title from media_labels where mid = "+mid+" and label_lid = 1")
            title = cur.fetchone()[0]
            cur.execute("SELECT DISTINCT title from category_labels where cid = "+cid+" and lid = 1")
            cat = cur.fetchone()[0]
            cur.execute(" SELECT DISTINCT title from category_labels where cid = "+scid+" and lid = 1 ")
            subcat = cur.fetchone()[0]
            cur.execute("INSERT INTO selection_log  (media_title, media_category, media_subcategory )  VALUES (?,?,?)",(title,cat,subcat))            
            self.get_db().commit()

    def get_selection_history(self):
        cur= self.get_db().cursor()
        cur.execute("SELECT * from selection_log" )         
        return cur
    '''