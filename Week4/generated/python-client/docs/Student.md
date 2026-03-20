# Student


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**full_name** | **str** |  | 
**email** | **str** |  | 
**year** | **int** |  | 

## Example

```python
from openapi_client.models.student import Student

# TODO update the JSON string below
json = "{}"
# create an instance of Student from a JSON string
student_instance = Student.from_json(json)
# print the JSON string representation of the object
print(Student.to_json())

# convert the object into a dict
student_dict = student_instance.to_dict()
# create an instance of Student from a dict
student_from_dict = Student.from_dict(student_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


