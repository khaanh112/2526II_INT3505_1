from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client.get_database("week8_db")
users_collection = db.get_collection("users")

@app.route('/v1/users', methods=['GET'])
def get_users():
    users = []
    for doc in users_collection.find():
        doc['id'] = str(doc.pop('_id'))
        users.append(doc)
    return jsonify(users), 200

@app.route('/v1/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    result = users_collection.insert_one({
        "name": data['name'],
        "email": data['email']
    })
    
    return jsonify({
        "message": "User created successfully",
        "id": str(result.inserted_id)
    }), 201

if __name__ == '__main__':
    app.run(port=8080, debug=True)
