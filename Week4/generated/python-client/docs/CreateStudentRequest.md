# CreateStudentRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**full_name** | **str** |  | 
**email** | **str** |  | 
**year** | **int** |  | 

## Example

```python
from openapi_client.models.create_student_request import CreateStudentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateStudentRequest from a JSON string
create_student_request_instance = CreateStudentRequest.from_json(json)
# print the JSON string representation of the object
print(CreateStudentRequest.to_json())

# convert the object into a dict
create_student_request_dict = create_student_request_instance.to_dict()
# create an instance of CreateStudentRequest from a dict
create_student_request_from_dict = CreateStudentRequest.from_dict(create_student_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


