# importing libraries
import bcrypt
import json
from bson import json_util, ObjectId
from flask import Flask, request , jsonify

import pymongo
from pymongo import errors

# defining the app
app = Flask(__name__)

# establishing connection with mongodb using pymongo
maxSevSelDelay = 1
try:
    client = pymongo.MongoClient("mongodb+srv://admin-arjyo:batulthegreat@cluster0.qwodm.mongodb.net/?retryWrites=true&w=majority",
                                     serverSelectionTimeoutMS=maxSevSelDelay)
    client.server_info()
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)
db = client.db

# helper function
def encrypt(password):
    # ecoding before hashing
    password = password.encode('utf-8')
    password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
    return password_hash

# default route
@app.route('/')
def index():
    return 'Home page'

# route without any argument passed
@app.route('/users', methods = ['GET', 'POST'])
def all_users():
    if request.method == 'GET':
        users = db.users
        output = []

        # find all queries in users collection
        for q in users.find():
            output.append({'id':q['_id'], 'name':q['name'], 'email':q['email'], 'password':q['password']})
        users_output = json.loads(json_util.dumps(output))

        return users_output

    if request.method == 'POST':
        try:
            input_json = request.get_json(force=True) 
            name = input_json['name']
            email = input_json['email']
            password = input_json['password']
            if not name or not email or not password:
                return jsonify({'error': 'Missing required fields'}), 400
        # encrypting password 
            encrypted_password = encrypt(password)

            obj = {'name':name, 'email':email, 'password':encrypted_password}
            result = db.users.insert_one(obj)
            return jsonify({'id': str(result.inserted_id), 'name': name, 'email': email})
        except Exception as e:
            return jsonify({'error': str(e)}), 500


# route with id passed as argument 
@app.route('/users/<user_id>', methods = ['GET', 'PUT', 'DELETE'])
def get_user(user_id):
    # returns data of particular user
    if request.method == 'GET':
        print(user_id)
        users = db.users

        # iterating through records in users collection
        for q in users.find():
            if q['_id'] == ObjectId(user_id):
                # jsonifies the data
                user_output = json.loads(json_util.dumps(q))
                return user_output

        return 'user not found'

    # updates data of particular user
    if request.method == 'PUT':
        print(user_id)
        input_json = request.get_json(force=True) 
        name = input_json['name']
        email = input_json['email']
        password = input_json['password']

        # encrypting password
        encrypted_password = encrypt(password)

        users = db.users
        # iterating through records of users collection
        for q in users.find():
            if q['_id'] == ObjectId(user_id):
                new_data = {'name':name, 'email':email, 'password':encrypted_password}
                # update statement
                db.users.replace_one(q, new_data, True)
                return 'user updated'
        return 'user not found'

    # deletes record of user from collection
    if request.method == 'DELETE':
        print(user_id)
        users = db.users

        # iterating though records of users collection
        for q in users.find():
            if q['_id'] == ObjectId(user_id):
                # delete statement
                db.users.delete_one(q)
                return 'deleted'

        return 'user not found'

# app run
if __name__ == "__main__":
    app.run(debug = True)