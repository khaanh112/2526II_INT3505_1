# StudentSingleResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** |  | 
**data** | [**Student**](Student.md) |  | 
**message** | **str** |  | 

## Example

```python
from openapi_client.models.student_single_response import StudentSingleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StudentSingleResponse from a JSON string
student_single_response_instance = StudentSingleResponse.from_json(json)
# print the JSON string representation of the object
print(StudentSingleResponse.to_json())

# convert the object into a dict
student_single_response_dict = student_single_response_instance.to_dict()
# create an instance of StudentSingleResponse from a dict
student_single_response_from_dict = StudentSingleResponse.from_dict(student_single_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


