import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import mongomock
from app import app, users_collection
import json

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        # Setup mock db
        self.mock_client = mongomock.MongoClient()
        self.mock_db = self.mock_client.week8_db
        self.mock_users = self.mock_db.users
        
        # Patch the global users_collection in app.py
        self.patcher = patch('app.users_collection', self.mock_users)
        self.patcher.start()
        
        self.client = app.test_client()

    def tearDown(self):
        self.patcher.stop()

    def test_create_user(self):
        """Test POST /v1/users"""
        payload = {"name": "Test User", "email": "test@domain.com"}
        response = self.client.post('/v1/users', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['message'], "User created successfully")

    def test_get_users(self):
        """Test GET /v1/users"""
        # Pre-insert data
        self.mock_users.insert_one({"name": "User A", "email": "a@test.com"})
        
        response = self.client.get('/v1/users')
        self.assertEqual(response.status_code, 200)
        users = response.get_json()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['name'], "User A")

    def test_create_user_invalid(self):
        """Test POST /v1/users with missing fields"""
        payload = {"name": "Incomplete"}
        response = self.client.post('/v1/users', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
