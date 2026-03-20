# StudentListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** |  | 
**data** | [**List[Student]**](Student.md) |  | 
**message** | **str** |  | 

## Example

```python
from openapi_client.models.student_list_response import StudentListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StudentListResponse from a JSON string
student_list_response_instance = StudentListResponse.from_json(json)
# print the JSON string representation of the object
print(StudentListResponse.to_json())

# convert the object into a dict
student_list_response_dict = student_list_response_instance.to_dict()
# create an instance of StudentListResponse from a dict
student_list_response_from_dict = StudentListResponse.from_dict(student_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


