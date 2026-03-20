# BookCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**author** | **str** |  | 

## Example

```python
from openapi_client.models.book_create_request import BookCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BookCreateRequest from a JSON string
book_create_request_instance = BookCreateRequest.from_json(json)
# print the JSON string representation of the object
print(BookCreateRequest.to_json())

# convert the object into a dict
book_create_request_dict = book_create_request_instance.to_dict()
# create an instance of BookCreateRequest from a dict
book_create_request_from_dict = BookCreateRequest.from_dict(book_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


