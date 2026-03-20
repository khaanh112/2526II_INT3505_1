# openapi_client.HealthApi

All URIs are relative to *http://localhost:5000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**health_get**](HealthApi.md#health_get) | **GET** /health | Kiểm tra trạng thái dịch vụ


# **health_get**
> SuccessResponse health_get()

Kiểm tra trạng thái dịch vụ

### Example


```python
import openapi_client
from openapi_client.models.success_response import SuccessResponse
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
    api_instance = openapi_client.HealthApi(api_client)

    try:
        # Kiểm tra trạng thái dịch vụ
        api_response = api_instance.health_get()
        print("The response of HealthApi->health_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling HealthApi->health_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Service healthy |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

