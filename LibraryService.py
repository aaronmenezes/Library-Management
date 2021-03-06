from flask import Flask, request ,jsonify, send_file, Response,send_from_directory
from flask_script import Manager, Server
from DatabaseInstance import DatabaseInstance 
from datetime import datetime
from time import sleep
from flask_cors import CORS
from models.Member import Member
from models.Inventory import Inventory
from models.TransactionView import TransactionView
from models.CheckedBooks import CheckedBooks
from models.InventoryView import InventoryView
from models.BookRankingView import BookRankingView
from models.SchemaMapping import Book as BookSchema
from models.SchemaMapping import Bag as BagSchema
from models.SchemaMapping import Member as MemberSchema
from models.SchemaMapping import CheckedBooks as CheckedBooksSchema 
from models.SchemaMapping import Inventory as InventorySchema 
from models.SchemaMapping import InventoryView as InventoryViewSchema
from models.SchemaMapping import MemberRankingView as MemberRankingViewSchema
from models.SchemaMapping import BookRanking as BookRankingViewSchema 
import os 
import pandas as pd 
import requests    
import hashlib 

app = Flask(__name__)   
CORS(app)

@app.route("/test")
def hello():
    DatabaseInstance.getInstance().testDb()
    return "hello"

@app.route('/getApiBookList')
def get_api_book_list():
    arg_string = ""
    for key in request.args:
        if  request.args[key] !="":
            arg_string+='{}={}&&'.format(key, request.args[key]) 
    print('https://frappe.io/api/method/frappe-library'+"?"+arg_string)
    json_arr = requests.get('https://frappe.io/api/method/frappe-library'+"?"+arg_string)
    if len(json_arr.json()["message"]) ==0 :
        return jsonify([])
    book_list=pd.DataFrame(json_arr.json()["message"])
    book_list.rename(columns={'  num_pages': 'num_pages'},inplace =True) 
    book_list = book_list.assign(count=1)
    book_list = book_list.assign(inventory_count=0)
    inventory_count_list = DatabaseInstance.getInstance().get_invetory_count(book_list['bookID'].tolist())  
    for item in inventory_count_list:  
        book_list.loc[book_list.bookID == str(item.bookID), 'inventory_count'] = item.count 
    return book_list.to_json(orient="records")
    
@app.route('/getAllBooks')
def get_all_book_list():  
    book_list = DatabaseInstance.getInstance().get_all_books()
    schema = BookSchema()
    result = BookSchema().dump(book_list, many=True) 
    return jsonify({"booklist":result})
    
@app.route('/quickBookSearch')
def quick_book_search():  
    book_param = request.args["book_q"]
    author_param = request.args["auth_q"] 
    book_list = DatabaseInstance.getInstance().search_books(book_param,author_param) 
    inventory=[]
    for in_item, bk_item in book_list:
        inventory.append(InventoryView(inventory_item= in_item,book_item =bk_item))
    schema = InventoryViewSchema()
    result = schema.dump(inventory,many=True) 
    return jsonify({"booklist":result})

@app.route('/addBooksToSystem', methods=['POST'])
def add_books_to_system():      
    book_to_import = request.json["import_book"]
    inventory_count = book_to_import.pop('inventory_count', 0)
    import_count = book_to_import.pop('import_count', 0)
    book_to_import.pop('count', None)
    if inventory_count ==0: 
        DatabaseInstance.getInstance().add_book(book_to_import)
        DatabaseInstance.getInstance().add_item_to_inventory({"bookID":book_to_import["bookID"],"count":import_count})
    else :     
        DatabaseInstance.getInstance().update_inventory_item(book_to_import["bookID"], int(inventory_count)+int(import_count))
    return jsonify({"status":"success"})
    
@app.route('/updateBookCount')
def update_book_count(): 
    DatabaseInstance.getInstance().update_inventory_item(request.args["bookId"],request.args["count"])
    return ""

@app.route('/deleteBook')
def delete_book(): 
    DatabaseInstance.getInstance().delete_book(request.args["bookId"])
    return jsonify({"status":"success"})

@app.route('/updateBookDetails', methods=['POST'])
def update_book_details():   
    DatabaseInstance.getInstance().update_book_details(request.json["bookId"],request.json["bookDetails"])
    return jsonify({"status":"success"})

@app.route('/signin', methods=['POST'])
def sign_in(): 
    print(request.json)
    user_id = request.json['userId']
    psswd = request.json['psswd']
    member_details = DatabaseInstance.getInstance().get_member(user_id);
    
    if isinstance(member_details,Member) and check_password(user_id,psswd,member_details.psswd):  
        schema =MemberSchema(exclude={"psswd"})
        result = schema.dump(member_details)     
        return jsonify(
        {
        "login":"success", 
        "user_details":result
        }
        )
    else:
        return jsonify( { "login":"fail"})

@app.route('/signup' , methods=['POST'])
def sign_up():
    user_id = request.json['user_id']
    psswd = hashPass(user_id,request.json['psswd'])  
    DatabaseInstance.getInstance().add_member(user_id,psswd,request.json['first_name'],request.json['last_name'],request.json['dob'],datetime.today().strftime('%d-%m-%Y'));
    return get_member_list()

@app.route('/checkout' , methods=['POST'])
def checkout():
    user_id = request.json['userId']
    book_id = request.json['bookId'] 
    result = DatabaseInstance.getInstance().book_checkout(user_id,book_id,datetime.today().strftime('%d-%m-%Y'),100);
    return jsonify(result)

@app.route('/checkin' , methods=['POST'])
def checkin():
    user_id = request.json['userId']
    book_id = request.json['bookId'] 
    bagId = request.json['bagId'] 
    DatabaseInstance.getInstance().book_checkin(user_id,book_id,bagId,datetime.today().strftime('%d-%m-%Y'),100);
    return jsonify({"status":"success"})

@app.route('/getCheckedBooks')
def get_checked_books(): 
    baglist = DatabaseInstance.getInstance().get_checked_books();  
    checked_books = []
    for bgitem,bkitem,memitem  in baglist:
        checked_books.append(CheckedBooks(bag_item=bgitem , book_item=bkitem, member_item = memitem))
    schema = CheckedBooksSchema()
    result = schema.dump(checked_books,many=True) 
    return jsonify({"booklist":result}) 

@app.route('/getBooksInventory')
def get_books_inventory(): 
    inventory_list = DatabaseInstance.getInstance().get_books_inventory();   
    inventory=[]
    for in_item, bk_item in inventory_list:
        inventory.append(InventoryView(inventory_item= in_item,book_item =bk_item))
    schema = InventoryViewSchema()
    result = schema.dump(inventory,many=True) 
    return jsonify({"booklist":result}) 

@app.route('/getMemberList')
def get_member_list():
    member_list = DatabaseInstance.getInstance().get_member_list(); 
    schema = MemberSchema(exclude={"psswd"})
    result = schema.dump(member_list,many=True) 
    return jsonify({"memberlist":result})

@app.route('/deleteMember')
def delete_member(): 
    DatabaseInstance.getInstance().delete_member(request.args["memberId"])
    return get_member_list()

@app.route('/updateMemberDetails', methods=['POST'])
def update_member_details():
    DatabaseInstance.getInstance().update_member_details(request.json["memberId"],request.json["memberDetails"]);
    return get_member_list()

@app.route('/getCustomerRanking')
def get_customer_ranking():    
    transactions = DatabaseInstance.getInstance().get_top_spenders();  
    tmpView=[]
    for spend_amount, mb_item in transactions:
        tmpView.append(TransactionView(item_count= spend_amount,member_item = mb_item))
    schema = MemberRankingViewSchema()
    transactionView = schema.dump(tmpView,many=True)
    return jsonify({"rank_list":transactionView})     

@app.route('/getTopBooks')
def get_top_books():
    result = DatabaseInstance.getInstance().get_top_books()
    tmp_view = [] 
    for rank_count,bk_item, in_count, chk_count in result: 
        tmp_view.append(BookRankingView(item_count = rank_count,inventory_count= in_count,checkout_count=chk_count, book_item=bk_item))
    schema = BookRankingViewSchema()
    result_view = schema.dump(tmp_view,many=True)  
    return jsonify({"rank_list":result_view})

@app.route('/getTopBooksReport')
def get_top_books_report():
    result = DatabaseInstance.getInstance().get_top_books() 
    data_list = [to_dict(item) for item in result]
    data_list  = reversed(data_list) 
    df = pd.DataFrame(data_list)
    filename = "assets/TopBooksReport.xlsx"
    sheet_name = 'TopBooksReport'
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, sheet_name=sheet_name) 
    workbook = writer.book
    worksheet = writer.sheets[sheet_name] 
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({ 
        'values':     [sheet_name, 1, 1, len(df.index), 1], 
        'gap':        2,
    }) 
    chart.set_legend({'position': 'top'}) 
    chart.set_y_axis({'major_gridlines': {'visible': True}})   
    worksheet.insert_chart('R2', chart) 
    writer.save()
    return send_from_directory(directory='assets',filename= 'TopBooksReport.xlsx', as_attachment=True)

@app.route('/getCustomerRankingReport')
def get_top_spender_report():
    result = DatabaseInstance.getInstance().get_top_spenders() 
    data_list = [to_dict(item) for item in result]
    data_list  = reversed(data_list) 
    df = pd.DataFrame(data_list)
    filename = "assets/TopSpenderReport.xlsx"
    sheet_name = 'TopSpenderReport'
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, sheet_name=sheet_name)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name] 
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({	
        'values':     [sheet_name, 1, 1, len(df.index), 1], 
        'gap':        2,
    }) 
    chart.set_legend({'position': 'top'}) 
    chart.set_y_axis({'major_gridlines': {'visible': True}})   
    worksheet.insert_chart('R2', chart) 
    writer.save() 
    return send_from_directory(directory='assets',filename= 'TopSpenderReport.xlsx', as_attachment=True)
    
def to_dict(row): 
    if row is None:
        return None
    rtn_dict = dict()     
    keys =[a for a in dir( row[1]) if not (a.startswith('_') or a =='metadata' or a=='query')] 
    for ikeys in row:
        if row.index(ikeys) !=1:
            rtn_dict[row.keys()[row.index(ikeys)]] =ikeys
        for key in keys:
            rtn_dict[key] = getattr(row[1], key)
    return rtn_dict
    

def hashPass(user_id,psswd):
    result = hashlib.md5((user_id+psswd).encode())
    return  result.hexdigest()

def check_password(user_id,raw_password, enc_password):    
    return enc_password == hashPass(user_id,raw_password)
    
@app.teardown_appcontext
def shutdown_session(exception=None):
    DatabaseInstance.getInstance().remove()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port,debug=False) 
