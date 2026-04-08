import unittest

from flask import json

from openapi_server.models.book_create_request import BookCreateRequest  # noqa: E501
from openapi_server.models.book_update_request import BookUpdateRequest  # noqa: E501
from openapi_server.models.error_response import ErrorResponse  # noqa: E501
from openapi_server.models.success_response import SuccessResponse  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_d_elete_books_book_id(self):
        """Test case for d_elete_books_book_id

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books/{book_id}'.format(book_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_g_et_books(self):
        """Test case for g_et_books

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_g_et_books_book_id(self):
        """Test case for g_et_books_book_id

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books/{book_id}'.format(book_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_g_et_health(self):
        """Test case for g_et_health

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/health',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_p_ost_books(self):
        """Test case for p_ost_books

        
        """
        book_create_request = {"author":"author","title":"title"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='POST',
            headers=headers,
            data=json.dumps(book_create_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_p_ut_books_book_id(self):
        """Test case for p_ut_books_book_id

        
        """
        book_update_request = {"author":"author","title":"title"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/books/{book_id}'.format(book_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(book_update_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
