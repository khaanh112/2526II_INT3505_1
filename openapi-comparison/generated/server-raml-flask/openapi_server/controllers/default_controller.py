import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book_create_request import BookCreateRequest  # noqa: E501
from openapi_server.models.book_update_request import BookUpdateRequest  # noqa: E501
from openapi_server.models.error_response import ErrorResponse  # noqa: E501
from openapi_server.models.success_response import SuccessResponse  # noqa: E501
from openapi_server import util


def d_elete_books_book_id(book_id):  # noqa: E501
    """d_elete_books_book_id

     # noqa: E501

    :param book_id: 
    :type book_id: int

    :rtype: Union[SuccessResponse, Tuple[SuccessResponse, int], Tuple[SuccessResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def g_et_books():  # noqa: E501
    """g_et_books

     # noqa: E501


    :rtype: Union[SuccessResponse, Tuple[SuccessResponse, int], Tuple[SuccessResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def g_et_books_book_id(book_id):  # noqa: E501
    """g_et_books_book_id

     # noqa: E501

    :param book_id: 
    :type book_id: int

    :rtype: Union[SuccessResponse, Tuple[SuccessResponse, int], Tuple[SuccessResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def g_et_health():  # noqa: E501
    """g_et_health

     # noqa: E501


    :rtype: Union[SuccessResponse, Tuple[SuccessResponse, int], Tuple[SuccessResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def p_ost_books(body):  # noqa: E501
    """p_ost_books

     # noqa: E501

    :param book_create_request: 
    :type book_create_request: dict | bytes

    :rtype: Union[SuccessResponse, Tuple[SuccessResponse, int], Tuple[SuccessResponse, int, Dict[str, str]]
    """
    book_create_request = body
    if connexion.request.is_json:
        book_create_request = BookCreateRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def p_ut_books_book_id(book_id, body):  # noqa: E501
    """p_ut_books_book_id

     # noqa: E501

    :param book_id: 
    :type book_id: int
    :param book_update_request: 
    :type book_update_request: dict | bytes

    :rtype: Union[SuccessResponse, Tuple[SuccessResponse, int], Tuple[SuccessResponse, int, Dict[str, str]]
    """
    book_update_request = body
    if connexion.request.is_json:
        book_update_request = BookUpdateRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
