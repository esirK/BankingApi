# BankingApi
[![Build Status](https://travis-ci.org/esirK/BankingApi.svg?branch=develop)](https://travis-ci.org/esirK/BankingApi)

Allows different users(Managers, Bank Tellers, and Customers) to perform different bank activities from an API

## API Spec
The preferred response format should be JSON.
The JSON object to be returned by the API should be structured as follows:

### Users (for authentication)
```source-json
{
  "user": {
    "email": "john@doe.jake",
    "username": "johndoe",
    "is_activated": True/False
    "token": "jwt.token.here",
  }
}
```
### Single Transaction
```source-json
{
    "transaction": {
        "type": [topup, transfer, withdraw],
        "performed_by": user: {
            "name": name,
            "id": user_id
         },
         "timestamp": "When the transaction happened",
         "status": "Success/Failure"
    }
}
```

### Multiple Transactions
```source-json
{
    "transactions":
        [{
            "id": 1,
            "type": [topup, transfer, withdraw],
            "performed_by": user: {
                "name": name,
                "id": user_id
             },
             "timestamp": "When the transaction happened",
             "status": "Success/Failure"
        }],
        "transactions_count": 1
}
```
### Errors and Status Codes
If a request fails any validations, errors should be expected in the following format:
```source-json
{
  "errors":{
    "email": [
      "User with this email already exists"
    ]
  }
}
```
### Other status codes:
401 for Unauthorized requests, when a request requires authentication but it isn't provided

403 for Forbidden requests, when a request may be valid but the user doesn't have permissions to perform the action

404 for Not found requests, when a resource can't be found to fulfill the request

Endpoints:
----------
### Registration:

`POST /api/register`

Example request body:

```source-json
{
    "username": "Jacob",
    "email": "jake@jake.jake",
    "confirm_email": "jake@jake.jake",
    "password": "jakejake"
}
```

Only a Manager or a Bank Teller can access this endpoint i.e
If the request is successful, the user details will be returned.

Required fields: `email`, `confirm_email`, `username`, `password`

##### Note
The registered user will have to change their accounts password once they are logged in the first time.

### Login:

`POST /api/login`

Example request body:

```source-json
{
    "email": "jake@jake.jake",
    "password": "jakejake"
}
```
No authentication required.
On successful login, a JWT will be returned that will be used to access other secure endpoints.

Required fields: `email`, `password`

### Perform a Transaction
`POST /api/transactions`

Example request body

```source-json
{
    "type": "withdraw/deposit/transfer",
    "amount": "20000",
    "timestamp": "11/30/2018 @ 11:09am (UTC)",
    "performed_by": {
        "user": {
            "name": "Kimotho",
            "account_type": "customer",
            "user_id": 10,
        }
    },
    "status": "Success/Failure"
}
```

### View all Managers
`GET /api/users/managers`

Authentication will be required for this endpoint.
Only Users with Manager permissions can access this endpoint.

Response should be a list of all available managers

Sample response
```source-json
{
    "managers":
        [
            {
                "username": "John",
                "email": "john.doe@company.com",
                "user_id": 10,
                "account_type": "manager"
            },
            {
                "username": "Mike",
                "email": "mike.tyson@company.com",
                "user_id": 20,
                "account_type": "manager"
            },
         ]
}
```

### View all Bank Tellers

`GET /api/users/tellers`

Authentication will be required for this endpoint. Only Users with manager and teller permissions can access this endpoint.
Response should be a list of all available tellers.

Sample response
```
{
    "tellers":
        [
            {
                "username": "John",
                "email": "john.doe@company.com",
                "user_id": 10,
                "account_type": "teller"
            },
            {
                "username": "Mike",
                "email": "mike.tyson@company.com",
                "user_id": 20,
                "account_type": "teller"
            },
         ]
}
```

### View all Bank Customers

`GET /api/users/customers`

Authentication will be required for this endpoint. Only Users with manager and teller permissions can access this endpoint.
Response should be a list of all available customers.

Sample response
```
{
    "customers":
        [
            {
                "username": "John",
                "email": "john.doe@company.com",
                "user_id": 10,
                "account_type": "customer"
            },
            {
                "username": "Mike",
                "email": "mike.tyson@company.com",
                "user_id": 20,
                "account_type": "customer"
            },
         ]
}
```

All users will have access to their accounts where they can perform updates on their accounts.
Managers can access all accounts belonging to tellers and customers.

They however can not update the users passwords.

Tellers can access all accounts belonging to customers but can not update their passwords.

Endpoint to access a user

###### Manager
`GET api/users/managers/username`

`PUT api/users/managers/username`


###### Tellers
`GET api/users/tellers/username`

`PUT api/users/tellers/username`


###### Customer
`GET api/users/customers/username`

`PUT api/users/customers/username`
