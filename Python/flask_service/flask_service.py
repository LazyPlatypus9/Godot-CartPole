from flask import Flask, request, jsonify
from pymongo import MongoClient, DESCENDING
  
app = Flask(__name__) 

CLIENT = MongoClient('mongodb://localhost:27017/')
DB = CLIENT['godot-cartpole']
  
@app.route('/') 
def ping(): 
    return 'MongoDB is running'

@app.route('/<collection>/get_last_row', methods=['GET'])
def get_last_row(collection):
    last_row = DB[collection].find_one(sort=[('_id', DESCENDING)])

    if last_row and "_id" in last_row:
        last_row["_id"] = str(last_row["_id"])

    return last_row

@app.route('/<collection>/add', methods=['POST'])
def add(collection):
    data = request.json

    DB[collection].insert_one(data)

    return 'Data added to MongoDB'
  
if __name__ == '__main__': 
    app.run() 
