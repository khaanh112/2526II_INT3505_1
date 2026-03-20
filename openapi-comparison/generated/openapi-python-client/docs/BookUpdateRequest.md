# BookUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**author** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.book_update_request import BookUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BookUpdateRequest from a JSON string
book_update_request_instance = BookUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(BookUpdateRequest.to_json())

# convert the object into a dict
book_update_request_dict = book_update_request_instance.to_dict()
# create an instance of BookUpdateRequest from a dict
book_update_request_from_dict = BookUpdateRequest.from_dict(book_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


