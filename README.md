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

## Login
All requests to API are made through API Token Authorization. On each successful login new Token for user generated, old deprecated. Only one device of user at a time is allowed. To get token send following request
<br />
Method: **POST**
<br />
http://127.0.0.1:8000/api/login
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
    "id": 30,
    "token": "c1f2dfdbd89d892b7f16d9ce264bf500d72c01e0"
}
```
<br />
**All other requests require Authorization Token, do not forget to specify token in each request**
<br />


## Logout
You can fully log out from game, your Token will be deleted and not replaced until you log in using default login or create a new account.
<br />
Method: **GET**
<br />
http://127.0.0.1:8000/api/logout
<br />
**Params**
<br />
user = {_user_id_}
<br />
**Return**
<br />
```json
{
    "detail": "You are logged out successfully"
}
```


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
        "id": 30,
        "username": "lbadmin",
        "first_name": "",
        "email": "sher.sadriddinov@gmail.com",
        "balance": 0,
        "donate": 0,
        "karma": 0,
        "client_settings_json": null
    },
    "token": {
        "key": "200a8007e8a9567cd3c37f16881021ebbe148ece"
    }
}
```

## User Info, Edit, Delete
Get, update, delete user information, depending on requests's method used. User is identified by user id passed.
You cannot update user's token, balance, donate & karma with this request
<br />
use **GET** - to get info about user
<br />
use **PUT** - to update one or more fields by passing params to update in json
<br />
use **DELETE** - to delete user
<br />
http://127.0.0.1:8000/api/user/{user id}/
<br />
Methods:
<br />
On **GET** you get user info
<br />
On **PUT** you can update user field all at once or one by one. All user info including passwords can be updated, except balance, donate, karma
<br />
On **DELETE** user profile moved to inactive state, data could be restored after relogin
<br />
**Return**
<br />
```json
{
    "id": 30,
    "username": "lbadmin",
    "first_name": "",
    "email": "sher.sadriddinov@gmail.com",
    "balance": 0,
    "donate": 0,
    "karma": 0,
    "client_settings_json": null
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

## Authorization - `unnecessary`
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