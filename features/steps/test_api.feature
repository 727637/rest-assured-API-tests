Feature: Testing Public APIs

  Scenario: Get a user by ID from API
    Given I set the API endpoint to "https://jsonplaceholder.typicode.com/users/1"
    When I send a GET request
    Then the response status code should be 200
    And the response should contain the name "Leanne Graham"


  Scenario: Get all users and verify count is 10
    Given I set the API endpoint to "https://jsonplaceholder.typicode.com/users"
    When I send a GET request
    Then the response status code should be 200
    And the response should contain 10 users

  Scenario: Create a new user
    Given I set the API endpoint to "https://jsonplaceholder.typicode.com/users"
    And I set the request body to
    """
    {
      "name": "Neha abc",
      "username": "neha123",
      "email": "neha123@example.com"
     }
    """
    When I send a post request
    Then the response status code should be 201
    And the response should contain the name "Neha abc"

  Scenario: Delete a user
    Given I set the API endpoint to "https://jsonplaceholder.typicode.com/users/1"
    When I send a DELETE request
    Then the response status code should be 200

  Scenario: Get a non-existent user
    Given I set the API endpoint to "https://jsonplaceholder.typicode.com/users/9999"
    When I send a GET request
    Then the response status code should be 404

  Scenario:Update an existing user
    Given I set the API endpoint to "https://jsonplaceholder.typicode.com/users/1"
    And I set the request body to
      """
      {
        "name": "Updated User",
        "username" : "updateuser",
        "email" : "updated@example.com"
      }
      """
    When I send a PUT request
    Then the response status code should be 200
    And the response should contain the name "Updated User"

  Scenario: Create user with missing email
    Given I set the API endpoint to "https://jsonplaceholder.typicode.com/users"
    And I set the request body to
      """
      {
      "name": "Jane Doe",
      "username": "janed"
      }
      """
    When I send a POST request
    Then the response status code should be 201

  Scenario: Validate email format of a user
    Given I set the API endpoint to "https://jsonplaceholder.typicode.com/users/1"
    When I send a GET request
    Then the response status code should be 200
    And the response should contain a valid email

  Scenario: Get posts for a user
    Given I set the API endpoint to "https://jsonplaceholder.typicode.com/users/1/posts"
    When I send a GET request
    Then the response status code should be 200
    And the response should contain posts for userID 1

  Scenario: Get user with invalid ID format
    Given I set the API endpoint to "https://jsonplaceholder.typicode.com/users/abc"
    When I send a GET request
    Then the response status code should be 404


