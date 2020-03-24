# Cyber API

Models docs are available at http://127.0.0.1:8000/ru/admin/doc/models/

## Requests list for Cyber API

## Error handling
If your request start causing error, you will get error status with json. Look always into `detail` field of json to see your error
<br/>
**Example**
```json
{
    "detail": "Not found."
}
```

## Authorization
All requests to API are made through API Token Authorization. To get token send following request
<br />
Method: **POST**
<br />
http://127.0.0.1:8000/api-token-auth/
<br />
**Body**
<br />
username = {_username: example lbadmin_}
<br />
password = {_password: example z709pa354rda_}
<br />
**Return**
<br />
```json
{
    "token": "3a46db5b038da1a7cc38e3c9332c2e6b00456128"
}
```
<br />
**All other requests require Authorization Token, do not forget to specify token in each request**
<br />

## Create User
Create new User instance, makes sure that user does not exist already in database
<br />
http://127.0.0.1:8000/api/auth/
<br />
Method: **POST**
<br />
**Body**
<br />
username - 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters
<br />
first_name (optional)
<br />
last_name (optional)
<br />
email
<br />
password
<br />
**Return**
<br />
```json
{
    "user": {
        "id": 21,
        "username": "Superman",
        "email": "sher.sadriddinov@gmail.com"
    },
    "token": {
        "key": "200a8007e8a9567cd3c37f16881021ebbe148ece"
    }
}
```

## User Info, Edit, Delete
Get, update, delete user information, depending on requests's method used. User is identified by user id passed.
You cannot update user's token, balance, donate & karma with this request!
<br />
use **GET** - to get info about user
<br />
use **PUT** - to update one or more fields by passing params to update in json
<br />
use **DELETE** - to delete user
<br />
http://127.0.0.1:8000/api/user/21/
<br />
Method: **GET**, **PUT**, **DELETE**
<br />
**Body**
<br />
username - 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters
<br />
first_name (optional)
<br />
last_name (optional)
<br />
email
<br />
password
<br />
**Return**
<br />
```json
{
    "id": 21,
    "username": "Superman",
    "email": "sher.sadriddinov@gmail.com"
}
```
<br />


## User List
Returns a list containing all active user's, count represents number of overall elements found. You can use `next` & `previous` if you add Authorization Token
<br />
http://127.0.0.1:8000/api/user/list/
<br />
Method: **GET**
<br />
**PARAMS**
<br />
_order_ - order of returned list, you can use `date_joined`, `username`, `last_login` or any other param. Use `-` before param (`-date_joined`) to get DESC order
<br />
_limit_ - limit list results to certain number (optional) if not used whole list will be returned
<br />
_offset_ - you can use it skip some number of results you already used. (optional)
<br />
**Return**
<br />
```json
{
    "count": 18,
    "next": "http://127.0.0.1:8000/api/user/list/?limit=2&offset=2",
    "previous": null,
    "results": [
        {
            "id": 21,
            "username": "Superman",
            "email": "sher.sadriddinov@gmail.com"
        },
        {
            "id": 20,
            "username": "Batman",
            "email": "sher.sadriddinov@gmail.com"
        }
    ]
}
```