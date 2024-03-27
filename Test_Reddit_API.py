import requests
import json

base_url = 'http://localhost:5000'



# Define a list of test cases for each endpoint

#positive test cases
positive_test_cases = [

    ('POST','/login',{'username': 'test_user', 'password': 'password'},200, 'success'),
    ('POST', '/post', {'title': 'Test Post', 'content': 'This is a test post', 'author': 'test_user'}, 200, 'success'),
    ('PUT', '/post/1', {'title': 'Updated Post', 'content': 'This post has been updated'}, 200, 'success'),
    ('POST', '/post/1/vote', {'vote': 'up'}, 200, 'success'),
    ('POST', '/post/1/comment', {'author': 'test_user', 'content': 'This is a test comment'}, 200, 'success'),
    ('POST', '/comment/1/vote=[]', {'vote': 'up'}, 200, 'success'),
    ('GET','/post/1/postview',None,200,'''{
  "comments": [
    {
      "author": "test_user",
      "content": "This is a test comment",
      "downvotes": 0,
      "id": 1,
      "upvotes": 1
    }
  ],
  "downvotes": 0,
  "post": {
    "author": "test_user",
    "comments": [
      {
        "author": "test_user",
        "content": "This is a test comment",
        "downvotes": 0,
        "id": 1,
        "upvotes": 1
      }
    ],
    "content": "This post has been updated",
    "downvotes": 0,
    "id": 1,
    "title": "Updated Post",
    "upvotes": 1
  },
  "upvotes": 1
}
'''),
    ('GET', '/user/test_user/posts', None, 200,'''[
  {
    "author": "test_user",
    "comments": [
      {
        "author": "test_user",
        "content": "This is a test comment",
        "downvotes": 0,
        "id": 1,
        "upvotes": 1
      }
    ],
    "content": "This post has been updated",
    "downvotes": 0,
    "id": 1,
    "title": "Updated Post",
    "upvotes": 1
  }
]
'''),
    ('GET', '/user/test_user/votes', None, 200, '''[
  {
    "author": "test_user",
    "comments": [
      {
        "author": "test_user",
        "content": "This is a test comment",
        "downvotes": 0,
        "id": 1,
        "upvotes": 1
      }
    ],
    "content": "This post has been updated",
    "downvotes": 0,
    "id": 1,
    "title": "Updated Post",
    "upvotes": 1
  }
]
'''),
    ('GET', '/post/1/comments', None, 200, '''[
  {
    "author": "test_user",
    "content": "This is a test comment",
    "downvotes": 0,
    "id": 1,
    "upvotes": 1
  }
]
'''
 ),
    ('POST', '/comment/1/vote=[]', {'vote': 'down'}, 200, 'success'),
    ('DELETE', '/post/1', None, 200, 'success'),
]

# negetive test cases
negetive_test_cases = [
    ('POST','/login',{'username': 'invalid_user', 'password': 'invalid_password'},404, 'Invalid username or password'),
    ('PUT', '/post/100', {'title': 'Updated Post', 'content': 'This post has been updated'}, 404, 'not found'),
    ('POST', '/post/100/vote', {'vote': 'up'}, 404, 'not found'),
    ('POST', '/post/100/comment', {'author': 'test_user', 'content': 'This is a test comment'}, 404, 'not found'),
    ('POST', '/comment/100/vote=[]', {'vote': 'up'}, 404, 'not found'),
    ('GET','/post/1/postview',None,404, 'not found'),
    ('GET', '/user/non_user/posts', None, 404, 'not found'),
    ('GET', '/user/non_user/votes', None, 404, 'not found'),
    ('GET', '/post/100/comments', None, 404, 'not found'),
    ('DELETE', '/post/1', None, 404, 'not found'),
]

# Iterate over each test case in positive test cases and make requests to the server
print("Positive test cases:")
for method, endpoint, data, expected_status, expected_response in positive_test_cases:
    url = base_url + endpoint
    response = requests.request(method, url, json=data)
    actual_status = response.status_code
    actual_response = response.text
    
    if actual_status == expected_status and actual_response == expected_response:
        print(f"Test case for {method} {endpoint}: PASSED")
    else:
        print(f"Test case for {method} {endpoint}: FAILED. Expected status {expected_status}, response '{expected_response}', but got status {actual_status}, response '{actual_response}'") 
print("")
print("Negetive test cases:")

# Iterate over each test case in negetive test cases and make requests to the server
for method, endpoint, data, expected_status, expected_response in negetive_test_cases:
    url = base_url + endpoint
    response = requests.request(method, url, json=data)
    actual_status = response.status_code
    actual_response = response.text
    if actual_status == expected_status and actual_response == expected_response:
        print(f"Test case for {method} {endpoint}: PASSED")
    else:
        print(f"Test case for {method} {endpoint}: FAILED. Expected status {expected_status}, response '{expected_response}', but got status {actual_status}, response '{actual_response}'") 