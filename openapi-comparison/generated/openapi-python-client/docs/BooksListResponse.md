# BooksListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** |  | 
**message** | **str** |  | 
**data** | [**List[Book]**](Book.md) |  | 

## Example

```python
from openapi_client.models.books_list_response import BooksListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BooksListResponse from a JSON string
books_list_response_instance = BooksListResponse.from_json(json)
# print the JSON string representation of the object
print(BooksListResponse.to_json())

# convert the object into a dict
books_list_response_dict = books_list_response_instance.to_dict()
# create an instance of BooksListResponse from a dict
books_list_response_from_dict = BooksListResponse.from_dict(books_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


