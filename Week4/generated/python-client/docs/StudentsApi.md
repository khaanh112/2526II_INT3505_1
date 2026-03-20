# openapi_client.StudentsApi

All URIs are relative to *http://127.0.0.1:5000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_student**](StudentsApi.md#create_student) | **POST** /students | Tạo mới sinh viên
[**delete_student**](StudentsApi.md#delete_student) | **DELETE** /students/{student_id} | Xoá một sinh viên
[**get_student_by_id**](StudentsApi.md#get_student_by_id) | **GET** /students/{student_id} | Lấy chi tiết một sinh viên
[**get_students**](StudentsApi.md#get_students) | **GET** /students | Lấy danh sách sinh viên
[**update_student**](StudentsApi.md#update_student) | **PUT** /students/{student_id} | Cập nhật thông tin một sinh viên


# **create_student**
> StudentSingleResponse create_student(create_student_request)

Tạo mới sinh viên

### Example


```python
import openapi_client
from openapi_client.models.create_student_request import CreateStudentRequest
from openapi_client.models.student_single_response import StudentSingleResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://127.0.0.1:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://127.0.0.1:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.StudentsApi(api_client)
    create_student_request = {"full_name":"Le Van C","email":"c.le@example.com","year":3} # CreateStudentRequest | 

    try:
        # Tạo mới sinh viên
        api_response = api_instance.create_student(create_student_request)
        print("The response of StudentsApi->create_student:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StudentsApi->create_student: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_student_request** | [**CreateStudentRequest**](CreateStudentRequest.md)|  | 

### Return type

[**StudentSingleResponse**](StudentSingleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Tạo sinh viên thành công |  -  |
**400** | Dữ liệu đầu vào không hợp lệ |  -  |
**409** | Trùng email sinh viên |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_student**
> DeleteResponse delete_student(student_id)

Xoá một sinh viên

### Example


```python
import openapi_client
from openapi_client.models.delete_response import DeleteResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://127.0.0.1:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://127.0.0.1:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.StudentsApi(api_client)
    student_id = 56 # int | Định danh duy nhất của sinh viên

    try:
        # Xoá một sinh viên
        api_response = api_instance.delete_student(student_id)
        print("The response of StudentsApi->delete_student:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StudentsApi->delete_student: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **student_id** | **int**| Định danh duy nhất của sinh viên | 

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
**200** | Xoá thành công |  -  |
**404** | Không tìm thấy sinh viên |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_student_by_id**
> StudentSingleResponse get_student_by_id(student_id)

Lấy chi tiết một sinh viên

### Example


```python
import openapi_client
from openapi_client.models.student_single_response import StudentSingleResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://127.0.0.1:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://127.0.0.1:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.StudentsApi(api_client)
    student_id = 56 # int | Định danh duy nhất của sinh viên

    try:
        # Lấy chi tiết một sinh viên
        api_response = api_instance.get_student_by_id(student_id)
        print("The response of StudentsApi->get_student_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StudentsApi->get_student_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **student_id** | **int**| Định danh duy nhất của sinh viên | 

### Return type

[**StudentSingleResponse**](StudentSingleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Thông tin sinh viên |  -  |
**404** | Không tìm thấy sinh viên |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_students**
> StudentListResponse get_students(year=year)

Lấy danh sách sinh viên

Trả về toàn bộ sinh viên hoặc lọc theo năm học (`year`).

### Example


```python
import openapi_client
from openapi_client.models.student_list_response import StudentListResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://127.0.0.1:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://127.0.0.1:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.StudentsApi(api_client)
    year = 56 # int | Lọc danh sách theo năm học (1-4) (optional)

    try:
        # Lấy danh sách sinh viên
        api_response = api_instance.get_students(year=year)
        print("The response of StudentsApi->get_students:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StudentsApi->get_students: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **year** | **int**| Lọc danh sách theo năm học (1-4) | [optional] 

### Return type

[**StudentListResponse**](StudentListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Danh sách sinh viên |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_student**
> StudentSingleResponse update_student(student_id, create_student_request)

Cập nhật thông tin một sinh viên

### Example


```python
import openapi_client
from openapi_client.models.create_student_request import CreateStudentRequest
from openapi_client.models.student_single_response import StudentSingleResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://127.0.0.1:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://127.0.0.1:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.StudentsApi(api_client)
    student_id = 56 # int | Định danh duy nhất của sinh viên
    create_student_request = {"full_name":"Le Van C Updated","email":"c.updated@example.com","year":4} # CreateStudentRequest | 

    try:
        # Cập nhật thông tin một sinh viên
        api_response = api_instance.update_student(student_id, create_student_request)
        print("The response of StudentsApi->update_student:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StudentsApi->update_student: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **student_id** | **int**| Định danh duy nhất của sinh viên | 
 **create_student_request** | [**CreateStudentRequest**](CreateStudentRequest.md)|  | 

### Return type

[**StudentSingleResponse**](StudentSingleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cập nhật sinh viên thành công |  -  |
**400** | Dữ liệu đầu vào không hợp lệ |  -  |
**404** | Không tìm thấy sinh viên |  -  |
**409** | Trùng email sinh viên |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

