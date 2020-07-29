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
_user_only_ -  boolean flag (1 - True, otherwise always False) to get list of friends of the User
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

## Search
Returns a list containing active non-staff user's matched given query
<br />
http://127.0.0.1:8000/api/user/search/
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
_user_only_ -  boolean flag (1 - True, otherwise always False) to search in list of friends of the User
<br />
_query_ - the string for searching in user names
**Return**
<br />
```json
{
    "users": [
        {
            "id": 49,
            "username": "user2",
            "first_name": "",
            "client_settings_json": null
        },
        {
            "id": 48,
            "username": "user1",
            "first_name": "",
            "client_settings_json": null
        },
        {
            "id": 5,
            "username": "default_user",
            "first_name": "",
            "client_settings_json": null
        }
    ]
}
```

## Character List
Returns list containing information about all current available character, id `user_only` parameter passed, returns the
list of character belonging to user, whose token used
<br />
Method: **GET**
<br />
http://127.0.0.1:8000/api/character/list/
<br />
**PARAMS**
<br />
_user_only_ - if set to 1, returns a list containing only user (whose token used) characters
<br />
_order_ - order of returned list, you can use `date_created`, `tech_name` or any other param. Use `-` before param (`-date_joined`) to get DESC order
<br />
_limit_ - limit list results to certain number (optional) if not used whole list will be returned
<br />
_offset_ - you can use it skip some number of results you already used. (optional)
<br />
**Return**
<br />
```json
{
    "count": 5,
    "next": "http://127.0.0.1:8000/api/character/list/?limit=2&offset=2",
    "previous": null,
    "results": [
        {
            "id": 8,
            "tech_name": "Soldier",
            "default": true
        },
        {
            "id": 6,
            "tech_name": "Pyro",
            "default": true
        }
    ]
}
```


## Character
Returns info about single character by character id
<br />
Method: **GET**
<br />
http://127.0.0.1:8000/api/character/{id}/
<br />
**Return**
<br />
```json
{
    "id": 4,
    "tech_name": "Heavy",
    "default": true
}
```


## Add Character to User (ONLY FOR DEV PURPOSE, REMOVE BEFORE RELEASE)
Adds given character by id to user (whose token used) characters
<br />
Method: **PUT**
<br />
http://127.0.0.1:8000/api/character/{id}/add
<br />
**Return**
<br />
```json
{
    "detail": "Successfully added to user characters"
}
```


## Remove Character from User
Removes character from user (whose token used) characters
<br />
Method: **DELETE**
<br />
http://127.0.0.1:8000/api/character/{id}/
<br />
**Return**
<br />
```json
{
    "detail": "Successfully removed from user characters"
}
```


## Weapon List
Returns list containing information about all current available weapons, id `user_only` parameter passed, returns the
list of weapons belonging to user, whose token used
<br />
Method: **GET**
<br />
http://127.0.0.1:8000/api/weapon/list/
<br />
**PARAMS**
<br />
_user_only_ - if set to 1, returns a list containing only user (whose token used) weapons
<br />
_order_ - order of returned list, you can use `date_created`, `tech_name` or any other param. Use `-` before param (`-date_joined`) to get DESC order
<br />
_limit_ - limit list results to certain number (optional) if not used whole list will be returned
<br />
_offset_ - you can use it skip some number of results you already used. (optional)
<br />
**Return**
<br />
```json
{
    "count": 53,
    "next": "http://127.0.0.1:8000/api/weapon/list/?limit=2&offset=2",
    "previous": null,
    "results": [
        {
            "id": 53,
            "tech_name": "MP5-SD",
            "default": false
        },
        {
            "id": 52,
            "tech_name": "P90",
            "default": false
        }
    ]
}
```


## Weapon
Returns info about single weapon with its addons available for this weapon by its id
<br />
Method: **GET**
<br />
http://127.0.0.1:8000/api/weapon/{id}/
<br />
**PARAM**
_user_only_ - if set to 1, returns weapon with addons purchased by user
<br />
**Return**
<br />
```json
{
    "weapon": {
        "id": 52,
        "tech_name": "P90",
        "default": false
    },
    "stock": [
        {
            "id": 5,
            "tech_name": "Compact 722",
            "default": true
        }
    ],
    "barrel": [],
    "muzzle": [],
    "mag": [],
    "scope": [],
    "grip": []
}
```
user_only = 1
```json
{
    "id": 19,
    "profile": 29,
    "weapon_with_addons": 4,
    "user_addon_stock": [
        5,
        4,
        3,
        2,
        1
    ],
    "user_addon_barrel": [],
    "user_addon_muzzle": [],
    "user_addon_mag": [],
    "user_addon_scope": [],
    "user_addon_grip": []
}
```

## Add Weapon to User (ONLY FOR DEV PURPOSE, REMOVE BEFORE RELEASE)
Adds given weapon by id to user (whose token used) weapons
<br />
Method: **PUT**
<br />
http://127.0.0.1:8000/api/weapon/{id}/add
<br />
**Return**
<br />
```json
{
    "detail": "Successfully added to user weapons"
}
```

## Remove Weapon from User
Removes weapon from user (whose token used) weapons
<br />
Method: **DELETE**
<br />
http://127.0.0.1:8000/api/weapon/{id}/
<br />
**Return**
<br />

```json
{
    "detail": "Successfully removed from user weapons"
}
```

## Notifications List
Returns a list containing all active notifications. Use it after every connection to web socket, and each time socket sends notification
<br />
```json
{
	"action": "notification"
}
```
Method: **GET**
<br />
http://127.0.0.1:8000/api/socket/connect/
<br />
**Return**
<br />
```json
{
    "id": 3,
    "date_created": "2020-07-20T21:49:28.882307+05:00",
    "notif_type": 1,
    "message": null,
    "status": true,
    "user": 49,
    "friend_id": 48
}
```

## Notification Info, Edit, Delete
Get, update, delete user notification, depending on requests's method used. Notification is identified by notification
id passed.
<br />
use **GET** - to get info about notif
<br />
use **PUT** - to update notif status. Boolean (True or False)
<br />
use **DELETE** - to delete notif
<br />
http://127.0.0.1:8000/socket/notif/{notif id}/
<br />
Methods:
<br />
On **GET** you get notif info
<br />
On **PUT** you can update notif status by sending "status": False
<br />
On **DELETE** delete notif
<br />
**Return**
<br />
```json
{
    "id": 3,
    "user": {
        "id": 49,
        "first_name": ""
    },
    "friend_id": {
        "id": 48,
        "first_name": ""
    },
    "date_created": "2020-07-20T21:49:28.882307+05:00",
    "notif_type": 1,
    "message": null,
    "status": true
}
```
<br />

## Friend Requests
Get list of your friend requests or make friend request
<br/>
Methods:
<br/>
On **GET** you will receive list of friend requests
<br/>
On **POST** you will create a friend request
<br/>
```json
{
	"friend": 48
}
```
http://127.0.0.1:8000/api/socket/friend/request/
<br />
**Return**
<br />
```json
{
	"id": 3,
	"date_created": "2020-07-20T21:49:28.882307+05:00",
	"notif_type": 1,
	"message": null,
	"status": true,
	"user": 49,
	"friend_id": 48
}
```

## Add Friend
Function to confirm friend request
<br />
Method: **PUT**
<br />
http://127.0.0.1:8000/api/friend/add/{user_id}/
<br />
**PARAM**
<br />
confirm - boolean (1 - True, 0 -False) to add frien or ignore
<br />
**Return**
<br />
```json
{
	"detail": "User added to friends list"
}
```

## Remove Friend
Function to remove someone from your friend list
<br />
Method: **PUT**
<br />
http://127.0.0.1:8000/api/friend/remove/{user_id}/
<br />
**Return**
<br />
```json
{
	"detail": "User removed from friends list"
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