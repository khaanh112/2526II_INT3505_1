import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util

from pymongo import MongoClient
import os

# Setup MongoDB connection
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
# Add a 3-second timeout so the API returns 500 error instead of hanging when DB is off
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client.get_database("week7_db")
users_collection = db.get_collection("users")


def create_user(body):  # noqa: E501
    """Create a user

     # noqa: E501

    :param body: User object to add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        data = connexion.request.get_json()
        result = users_collection.insert_one(data)
        return {"message": "User created successfully", "id": str(result.inserted_id)}, 201
    return "Invalid input", 400


def get_users():  # noqa: E501
    """Retrieve all users

     # noqa: E501

    :rtype: List[User]
    """
    # Fetch from MongoDB and map _id object to string for the API
    users = []
    for doc in users_collection.find():
        doc['id'] = str(doc.pop('_id'))
        users.append(doc)
    return users, 200
