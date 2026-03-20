# openapi_client.BooksApi

All URIs are relative to *http://localhost:5000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**books_book_id_delete**](BooksApi.md#books_book_id_delete) | **DELETE** /books/{bookId} | Xóa sách
[**books_book_id_get**](BooksApi.md#books_book_id_get) | **GET** /books/{bookId} | Lấy chi tiết sách
[**books_book_id_put**](BooksApi.md#books_book_id_put) | **PUT** /books/{bookId} | Cập nhật sách
[**books_get**](BooksApi.md#books_get) | **GET** /books | Lấy danh sách sách
[**books_post**](BooksApi.md#books_post) | **POST** /books | Thêm sách mới


# **books_book_id_delete**
> DeleteResponse books_book_id_delete(book_id)

Xóa sách

### Example


```python
import openapi_client
from openapi_client.models.delete_response import DeleteResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    book_id = 56 # int | 

    try:
        # Xóa sách
        api_response = api_instance.books_book_id_delete(book_id)
        print("The response of BooksApi->books_book_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BooksApi->books_book_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **book_id** | **int**|  | 

### Return type

[**DeleteResponse**](DeleteResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Xóa thành công |  -  |
**404** | Không tìm thấy sách |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_book_id_get**
> BookResponse books_book_id_get(book_id)

Lấy chi tiết sách

### Example


```python
import openapi_client
from openapi_client.models.book_response import BookResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    book_id = 56 # int | 

    try:
        # Lấy chi tiết sách
        api_response = api_instance.books_book_id_get(book_id)
        print("The response of BooksApi->books_book_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BooksApi->books_book_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **book_id** | **int**|  | 

### Return type

[**BookResponse**](BookResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Chi tiết sách |  -  |
**404** | Không tìm thấy sách |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_book_id_put**
> BookResponse books_book_id_put(book_id, book_update_request)

Cập nhật sách

### Example


```python
import openapi_client
from openapi_client.models.book_response import BookResponse
from openapi_client.models.book_update_request import BookUpdateRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    book_id = 56 # int | 
    book_update_request = openapi_client.BookUpdateRequest() # BookUpdateRequest | 

    try:
        # Cập nhật sách
        api_response = api_instance.books_book_id_put(book_id, book_update_request)
        print("The response of BooksApi->books_book_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BooksApi->books_book_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **book_id** | **int**|  | 
 **book_update_request** | [**BookUpdateRequest**](BookUpdateRequest.md)|  | 

### Return type

[**BookResponse**](BookResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cập nhật thành công |  -  |
**404** | Không tìm thấy sách |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_get**
> BooksListResponse books_get()

Lấy danh sách sách

### Example


```python
import openapi_client
from openapi_client.models.books_list_response import BooksListResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)

    try:
        # Lấy danh sách sách
        api_response = api_instance.books_get()
        print("The response of BooksApi->books_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BooksApi->books_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**BooksListResponse**](BooksListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Danh sách sách |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_post**
> BookResponse books_post(book_create_request)

Thêm sách mới

### Example


```python
import openapi_client
from openapi_client.models.book_create_request import BookCreateRequest
from openapi_client.models.book_response import BookResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    book_create_request = openapi_client.BookCreateRequest() # BookCreateRequest | 

    try:
        # Thêm sách mới
        api_response = api_instance.books_post(book_create_request)
        print("The response of BooksApi->books_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BooksApi->books_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **book_create_request** | [**BookCreateRequest**](BookCreateRequest.md)|  | 

### Return type

[**BookResponse**](BookResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Tạo thành công |  -  |
**400** | Dữ liệu không hợp lệ |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

