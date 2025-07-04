
# @given('I set the API endpoint to "{url}"')
# def step_given_set_url(context, url):
#     context.url = url
#
# @given('I set the request body to "{url}"')
# def step_given_request_body(context):
#     context.payload = json.loads(context.text)
#
# @when('I send a GET request')
# def step_when_get(context):
#     context.response = requests.get(context.url)
#
# @when('I send a POST request')
# def step_when_post(context):
#     headers = {"Content-type" : "application/json"}
#     context.response = requests.post(context.url, json=context.payload, headers=headers)
#
# @when('I send a DELETE request')
# def step_when_delete(context):
#     context.response = requests.delete(context.url)
#
# @when('I send a PUT request')
# def step_when_put(context):
#     headers = {"Content-type": "application/json"}
#     context.response = requests.put(context.url, json=context.payload, headers=headers)
#
# @then('the response status code should be {status_code:d}')
# def step_then_status_code(context, status_code):
#     allure.dynamic.title("Validate HTTP response status code")
#     allure.dynamic.description(f"Expected: {status_code}, Actual: {context.response.status_code}")
#     assert context.response.status_code == status_code
#
# @then('the response should contain the name "{name}"')
# def step_then_check_name(context, name):
#     json_response = context.response.json()
#     allure.dynamic.title("Validate name in API response")
#     assert json_response["name"] == name
#
# @then('the response should contain {count:d} users')
# def step_then_check_user_count(context, count):
#     json_response = context.response.json()
#     assert isinstance(json_response, list), "Response is not a list"
#     assert len(json_response) == count, f"Expected {count} users, got {len(json_response)}"
#
# @then('the response should contain a valid email')
# def step_then_valid_email(context):
#     json_response = context.response.json()
#     email = json_response.get("email", "")
#     assert "@" in email and "." in email, f"Invalid email format: {email}"
#
# @then('the response should contain posts for userID {user_id:d}')
# def step_then_posts_for_user(context, user_id):
#     json_response = context.response.json()
#     assert isinstance(json_response, list), "Expected a list of posts"
#     for post in json_response:
#         assert post.get("userId") == user_id

import requests
from behave import given, when, then
import json
import allure
from allure_commons.types import AttachmentType

@given('I set the API endpoint to "{url}"')
def step_given_set_url(context, url):
    context.url = url

@given('I set the request body to')
def step_given_request_body(context):
    try:
        context.payload = json.loads(context.text)
        allure.attach(context.text, name="Request Payload", attachment_type=AttachmentType.JSON)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON body: {e}")

@when('I send a GET request')
def step_when_get(context):
    context.response = requests.get(context.url)
    _attach_response(context)

@when('I send a POST request')
def step_when_post(context):
    headers = {"Content-Type": "application/json"}
    context.response = requests.post(context.url, json=context.payload, headers=headers)
    _attach_response(context)

@when('I send a PUT request')
def step_when_put(context):
    headers = {"Content-Type": "application/json"}
    context.response = requests.put(context.url, json=context.payload, headers=headers)
    _attach_response(context)

@when('I send a DELETE request')
def step_when_delete(context):
    context.response = requests.delete(context.url)
    _attach_response(context)

@then('the response status code should be {status_code:d}')
def step_then_status_code(context, status_code):
    actual = context.response.status_code
    allure.dynamic.title("Validate HTTP Status Code")
    allure.dynamic.description(f"Expected: {status_code}, Got: {actual}")
    assert actual == status_code, f"Expected {status_code}, but got {actual}"

@then('the response should contain the name "{name}"')
def step_then_check_name(context, name):
    json_response = context.response.json()
    actual_name = json_response.get("name", "")
    allure.dynamic.title("Validate Name in Response")
    allure.attach(json.dumps(json_response, indent=2), name="Response Body", attachment_type=AttachmentType.JSON)
    assert actual_name == name, f"Expected name '{name}', but got '{actual_name}'"

@then('the response should contain {count:d} users')
def step_then_check_user_count(context, count):
    json_response = context.response.json()
    assert isinstance(json_response, list), "Expected a list of users"
    actual_count = len(json_response)
    assert actual_count == count, f"Expected {count} users, but got {actual_count}"

@then('the response should contain a valid email')
def step_then_valid_email(context):
    json_response = context.response.json()
    email = json_response.get("email", "")
    assert "@" in email and "." in email, f"Invalid email format: {email}"

@then('the response should contain posts for userID {user_id:d}')
def step_then_posts_for_user(context, user_id):
    json_response = context.response.json()
    assert isinstance(json_response, list), "Expected a list of posts"
    for post in json_response:
        assert post.get("userId") == user_id, f"Post {post.get('id')} has userId {post.get('userId')} instead of {user_id}"

def _attach_response(context):
    try:
        content_type = context.response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            body = json.dumps(context.response.json(), indent=2)
            allure.attach(body, name="Response JSON", attachment_type=AttachmentType.JSON)
        else:
            allure.attach(context.response.text, name="Response Body", attachment_type=AttachmentType.TEXT)
    except Exception as e:
        allure.attach(f"Failed to attach response: {e}", name="Attachment Error", attachment_type=AttachmentType.TEXT)
