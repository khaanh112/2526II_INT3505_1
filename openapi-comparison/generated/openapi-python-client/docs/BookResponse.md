# BookResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** |  | 
**message** | **str** |  | 
**data** | [**Book**](Book.md) |  | 

## Example

```python
from openapi_client.models.book_response import BookResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BookResponse from a JSON string
book_response_instance = BookResponse.from_json(json)
# print the JSON string representation of the object
print(BookResponse.to_json())

# convert the object into a dict
book_response_dict = book_response_instance.to_dict()
# create an instance of BookResponse from a dict
book_response_from_dict = BookResponse.from_dict(book_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


