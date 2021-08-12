from flask import Flask, request ,jsonify, send_file, Response,send_from_directory
from flask_script import Manager, Server
from DatabaseInstance import DatabaseInstance 
from datetime import datetime
from time import sleep
import sqlite3
import os 
import pandas as pd
import numpy as np
from flask_cors import CORS
import requests   


app = Flask(__name__)   
CORS(app)

"""   
https://stream-canvas-va1.herokuapp.com/ | https://git.heroku.com/stream-canvas-va1.git
"""
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])


@app.route("/test")
def hello():
	DatabaseInstance.getInstance().testDb()
	return "hello"

@app.route('/getApiBookList')
def get_api_book_list():
	json_arr = requests.get('https://frappe.io/api/method/frappe-library')
	book_list=pd.DataFrame(json_arr.json()["message"])
	book_list.rename(columns={'  num_pages': 'num_pages'},inplace =True) 
	DatabaseInstance.getInstance().add_all_books(book_list.to_dict('records'))
	book_list=book_list.assign(count=1)
	print(book_list) 
	DatabaseInstance.getInstance().add_items_to_inventory(book_list.filter(['bookID', 'count']).to_dict('records'))
	return book_list.to_json(orient="records")
	
@app.route('/addBooksToSystem')
def add_books_to_system():	  
    book_list= pd.DataFrame(json_arr.json()["book_list"]) 
    return book_list.json()
	
@app.route('/updateBookCount')
def update_book_count(): 
    DatabaseInstance.getInstance().update_inventory_item(request.args["bookId"],request.args["count"])
    return ""
    
@app.route("/getAllNotes")
def get_all_notes():
	cur = DatabaseInstance.getInstance().get_all_notes()
	return jsonify(cur)
	
@app.route("/getAllNotesList")
def get_all_notes_list():
	cur = DatabaseInstance.getInstance().get_all_notes_list()
	return jsonify(cur)

@app.route("/addNewNote")
def add_new_note():
	print(request.args)
	cur = DatabaseInstance.getInstance().add_new_note(request.args['name'],request.args['date'],request.args['priority'],request.args['body'])
	return jsonify(cur)
	
@app.route("/updateNote")
def update_note():
	print(request.args)
	cur = DatabaseInstance.getInstance().update_note(request.args['id'],request.args['name'],request.args['body'])
	return jsonify(cur)

@app.route("/updateNotePriority")
def update_note_priority():
	print(request.args)
	cur = DatabaseInstance.getInstance().update_note_priority(request.args['id'],request.args['priority'])
	return jsonify(cur)

@app.route("/deleteNote")
def delete_note():
	print(request.args)
	cur = DatabaseInstance.getInstance().delete_note(request.args['id'])
	return jsonify(cur)
	
@app.route("/getNoteArchive")
def get_note_archive():
	cur = DatabaseInstance.getInstance().get_note_archive()
	return jsonify(cur)
	
@app.teardown_appcontext
def shutdown_session(exception=None):
    DatabaseInstance.getInstance().remove()

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 8080))
	app.run(host='0.0.0.0', port=port,debug=True) 
