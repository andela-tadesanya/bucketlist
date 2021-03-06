![bucketlist logo](http://s27.postimg.org/fdhwsdoqr/Bucket_List_logo.png) 

[![Coverage Status](https://coveralls.io/repos/andela-tadesanya/bucketlist/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-tadesanya/bucketlist?branch=master) [![Build Status](https://travis-ci.org/andela-tadesanya/bucketlist.svg?branch=master)](https://travis-ci.org/andela-tadesanya/bucketlist)
# INTRODUCTION
Bucketlist is an API built using flask, where users can create and manage their bucketlists.

# FEATURES
- Supports multiple users
- Token based authentication
- Users can create multiple bucket lists and bucketlist items
- Users can delete bucket lists and items in them

# INSTALLATION
- Download the repo
- cd into the project root in your favorite commandline tool
- Run `pip install -r requirements.txt` to install all dependencies
- Run `python runserver.py` to start the server
- You can use [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en) to send request to the server

# VERSION
version: 1.0.0

# User Guide
### Create A User
```bash
POST http://127.0.0.1:5000/api/v1.0/users

Request Body:
{
    'username': 'kitty',
    'password': 'wildcat',
}

Response:
{
  "app_bucket_listing": [],
  "id": 1,
  "username": "kitty"
}
```

![create a user with Postman](https://gyazo.com/048a496936c0da43e46543ff85d43dba.gif)

### Create A Token
```bash
POST http://127.0.0.1:5000/api/v1.0/auth/login

Request Body:
{
    'username': 'kitty',
    'password': 'wildcat',
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0NjczMzkzMSwiaWF0IjoxNDQ2NzMyNzMxfQ.eyJpZCI6MX0.V-e2exs8HOmM_qr8y5w7FgzUaRhlq1GVPZzHtJ0BWQs"
}
```
![get a token with Postman](https://gyazo.com/d23c8293f95e2207a870cd6405012cf5.gif)

### Create A Bucketlist
```bash
POST http://127.0.0.1:5000/api/v1.0/bucketlists

Request Header:
{
    'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0NjcyNjc3NiwiaWF0IjoxNDQ2NzI1NTc2fQ.eyJpZCI6MX0.uN8pUuUAhixYkmbNISsk5ruBZf6N6oSPd66K_c8dSvo'
}

Request Body:
{
    'name': 'Before I die',
}

Response:
{
  "app_bucketlist_items": [],
  "created_by": 1,
  "date_created": "2015-11-05T15:14:14.851000+00:00",
  "date_modified": "2015-11-05T15:14:14.851000+00:00",
  "id": 1,
  "name": "Before I die"
}
```

![create a bucketlist with Postman](https://gyazo.com/fe71f081a020a9f8cd222e0242a7848c.gif)

### Display All Bucketlists
```bash
GET http://127.0.0.1:5000/api/v1.0/bucketlists

Request Header:
{
    'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0NjcyNjc3NiwiaWF0IjoxNDQ2NzI1NTc2fQ.eyJpZCI6MX0.uN8pUuUAhixYkmbNISsk5ruBZf6N6oSPd66K_c8dSvo'
}

Response:
{
  "bucketlists": [
    {
      "app_bucketlist_items": [],
      "created_by": 1,
      "date_created": "2015-11-05T15:14:14.851000+00:00",
      "date_modified": "2015-11-05T15:14:14.851000+00:00",
      "id": 1,
      "name": "Before I die"
    }
  ],
  "current_page": 1,
  "has_next_page": false,
  "has_previous_page": false,
  "total_objects": 1,
  "total_pages": 1
}
```

![get all bucketlists with Postman](https://gyazo.com/342f0f3e927e3926e5675f2a533f6458.gif)

### Display All Bucketlists With Query, Limit and Page
```bash
GET http://127.0.0.1:5000/api/v1.0/bucketlists?q=before%i%die&limit=20&page=1

Request Header:
{
    'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0NjcyNjc3NiwiaWF0IjoxNDQ2NzI1NTc2fQ.eyJpZCI6MX0.uN8pUuUAhixYkmbNISsk5ruBZf6N6oSPd66K_c8dSvo'
}

Response:
{
  "bucketlists": [
    {
      "app_bucketlist_items": [],
      "created_by": 1,
      "date_created": "2015-11-05T15:45:30.576000+00:00",
      "date_modified": "2015-11-05T15:45:30.576000+00:00",
      "id": 1,
      "name": "Before I die"
    }
  ],
  "current_page": 1,
  "has_next_page": false,
  "has_previous_page": false,
  "total_objects": 1,
  "total_pages": 1
}
```

![get all bucketlists with query, limit and page with Postman](https://gyazo.com/61538d748a199bd7b409f881e34451b2.gif)
### Display Single Bucket List
```bash
GET http://127.0.0.1:5000/api/v1.0/bucketlists/<int:id>

Request Header:
{
    'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0NjcyNjc3NiwiaWF0IjoxNDQ2NzI1NTc2fQ.eyJpZCI6MX0.uN8pUuUAhixYkmbNISsk5ruBZf6N6oSPd66K_c8dSvo'
}

Response:
{
  "app_bucketlist_items": [],
  "created_by": 1,
  "date_created": "2015-11-05T15:14:14.851000+00:00",
  "date_modified": "2015-11-05T15:14:14.851000+00:00",
  "id": 1,
  "name": "Before I die"
}
```

![get a single bucketlist with Postman](https://gyazo.com/64dc9747140723a72577656e87b14c9d.gif)

### Update A Bucketlist
```bash
PUT http://127.0.0.1:5000/api/v1.0/bucketlists/`<bucketlist_id>`

Request Header:
{
    'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0NjcyNjc3NiwiaWF0IjoxNDQ2NzI1NTc2fQ.eyJpZCI6MX0.uN8pUuUAhixYkmbNISsk5ruBZf6N6oSPd66K_c8dSvo'
}

Request Body:
{
    'name': 'Before I live',
}

Response:
{
  "app_bucketlist_items": [],
  "created_by": 1,
  "date_created": "2015-11-05T15:14:14.851000+00:00",
  "date_modified": "2015-11-05T15:19:05.340000+00:00",
  "id": 1,
  "name": "Before I live"
}
```

![update a bucketlist with Postman](https://gyazo.com/b07ef55c62e2dd79e3ede469c7529ae4.gif)

### Create A Bucketlist Item
```bash
POST http://127.0.0.1:5000/api/v1.0/bucketlists/`<bucketlist_id>`/items

Request Header:
{
    'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0NjcyNjc3NiwiaWF0IjoxNDQ2NzI1NTc2fQ.eyJpZCI6MX0.uN8pUuUAhixYkmbNISsk5ruBZf6N6oSPd66K_c8dSvo'
}

Request Body:
{
    'name': 'learn to program',
}

Response:
{
  "date_created": "2015-11-05T15:20:57.454000+00:00",
  "date_modified": "2015-11-05T15:20:57.454000+00:00",
  "done": false,
  "id": 1,
  "name": "learn to program"
}
```

![create a bucketlist item with Postman](https://gyazo.com/009343bfa16ff9ce72b4e08d51b732e9.gif)

### Update A Bucketlist Item
```bash
PUT http://127.0.0.1:5000/api/v1.0/bucketlists/`<bucketlist_id>`/items/`<bucketlist_item_id>`

Request Header:
{
    'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0NjcyNjc3NiwiaWF0IjoxNDQ2NzI1NTc2fQ.eyJpZCI6MX0.uN8pUuUAhixYkmbNISsk5ruBZf6N6oSPd66K_c8dSvo'
}

Request Body:
{
    'name': 'learn to dance',
    'done': 'true'
}

Response:
{
  "date_created": "2015-11-05T15:20:57.454000+00:00",
  "date_modified": "2015-11-05T15:23:21.516000+00:00",
  "done": true,
  "id": 1,
  "name": "learn to dance"
}
```

![update a bucketlist item with Postman](https://gyazo.com/71967a8ba3827113b10309f1e64a5db1.gif)

### Delete A Bucketlist item
```bash
DELETE http://127.0.0.1:5000/api/v1.0/bucketlists/`<bucketlist_id>`/items/`<bucketlist_item_id>`

Request Header:
{
    'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0NjcyNjc3NiwiaWF0IjoxNDQ2NzI1NTc2fQ.eyJpZCI6MX0.uN8pUuUAhixYkmbNISsk5ruBZf6N6oSPd66K_c8dSvo'
}

Response:
{
  "message": "bucketlist item deleted"
}
```

![delete a bucketlist item with Postman](https://gyazo.com/703bdf0856a763cff16448a43306b1a7.gif)

### Delete A Bucketlist
```bash
DELETE http://127.0.0.1:5000/api/v1.0/bucketlists/`<bucketlist_id>`

Request Header:
{
    'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0NjcyNjc3NiwiaWF0IjoxNDQ2NzI1NTc2fQ.eyJpZCI6MX0.uN8pUuUAhixYkmbNISsk5ruBZf6N6oSPd66K_c8dSvo'
}

Response:
{
  "message": "bucketlist deleted"
}
```

![delete a bucketlist with Postman](https://gyazo.com/eae1197f708243dcc01b7036f9e90be3.gif)


# IMPLEMENTATION

### Config File
Two config files are used, 'test_config.py' and 'development_config.py' for testing and development/production environment respectively.

### Authentication
Tokens are used for authentication. You first create a user and create a token with the username and password. **Tokens expire after every 20mins.** Remember to always include a token variable in the header when making requests, except when creating a user.


# TESTS
Run `coverage run test_bucketlist.py`. 


# CREDITS
God and my two guardian angels(:angel: Google and Stackoverflow:angel:).
Also got some great insights from the following links:

- [http://flask.pocoo.org/snippets/22/](http://flask.pocoo.org/snippets/22/)
- [http://docs.sqlalchemy.org/en/rel_0_5/index.html](http://docs.sqlalchemy.org/en/rel_0_5/index.html)

# LICENSE
Free
