![bucketlist logo](http://s27.postimg.org/fdhwsdoqr/Bucket_List_logo.png)

[![Coverage Status](https://coveralls.io/repos/andela-tadesanya/bucketlist/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-tadesanya/bucketlist?branch=master)

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
URL                 |       HTTP METHOD        |    FORM DATA     |     HEADER DATA    
--------------------|--------------------------|------------------|----------------
http://127.0.0.1:5000/api/v1.0/users | POST |   username, password | 



![create a user with Postman](https://gyazo.com/048a496936c0da43e46543ff85d43dba.gif)

### Create A Token
URL                 |       HTTP METHOD        |    FORM DATA     |     HEADER DATA    
--------------------|--------------------------|------------------|----------------
http://127.0.0.1:5000/api/v1.0/auth/login | POST |   username, password | 

![get a token with Postman](https://gyazo.com/d23c8293f95e2207a870cd6405012cf5.gif)

### Create A Bucketlist
URL                 |       HTTP METHOD        |    FORM DATA     |     HEADER DATA    
--------------------|--------------------------|------------------|----------------
http://127.0.0.1:5000/api/v1.0/bucketlists | POST |   name | token

![get a token with Postman](https://gyazo.com/fe71f081a020a9f8cd222e0242a7848c.gif)

### Display All Bucketlists
URL                 |       HTTP METHOD        |    FORM DATA     |     HEADER DATA    
--------------------|--------------------------|------------------|----------------
http://127.0.0.1:5000/api/v1.0/bucketlists | GET |    | token

![get a all bucketlists with Postman](https://gyazo.com/342f0f3e927e3926e5675f2a533f6458.gif)

### Display Single Bucket List
URL                 |       HTTP METHOD        |    FORM DATA     |     HEADER DATA    
--------------------|--------------------------|------------------|----------------
http://127.0.0.1:5000/api/v1.0/bucketlists/<int:id> | GET |    | token

![get a single bucketlist with Postman](https://gyazo.com/64dc9747140723a72577656e87b14c9d.gif)

### Update A Bucketlist
URL                 |       HTTP METHOD        |    FORM DATA     |     HEADER DATA    
--------------------|--------------------------|------------------|----------------
http://127.0.0.1:5000/api/v1.0/bucketlists/`<bucketlist_id>` | PUT | name  | token

![update a bucketlist with Postman](https://gyazo.com/b07ef55c62e2dd79e3ede469c7529ae4.gif)

### Create A Bucketlist Item
URL                 |       HTTP METHOD        |    FORM DATA     |     HEADER DATA    
--------------------|--------------------------|------------------|----------------
http://127.0.0.1:5000/api/v1.0/bucketlists/`<bucketlist_id>`/items | POST | name  | token

![create a bucketlist item with Postman](https://gyazo.com/009343bfa16ff9ce72b4e08d51b732e9.gif)

### Update A Bucketlist Item
URL                 |       HTTP METHOD        |    FORM DATA     |     HEADER DATA    
--------------------|--------------------------|------------------|----------------
http://127.0.0.1:5000/api/v1.0/bucketlists/`<bucketlist_id>`/items/`<bucketlist_item_id>` | PUT | name, done=`<true|false>`  | token

![update a bucketlist item with Postman](https://gyazo.com/71967a8ba3827113b10309f1e64a5db1.gif)

### Delete A Bucketlist item
URL                 |       HTTP METHOD        |    FORM DATA     |     HEADER DATA    
--------------------|--------------------------|------------------|----------------
http://127.0.0.1:5000/api/v1.0/bucketlists/`<bucketlist_id>`/items/`<bucketlist_item_id>` | DELETE |   | token

![delete a bucketlist item with Postman](https://gyazo.com/703bdf0856a763cff16448a43306b1a7.gif)

### Delete A Bucketlist
URL                 |       HTTP METHOD        |    FORM DATA     |     HEADER DATA    
--------------------|--------------------------|------------------|----------------
http://127.0.0.1:5000/api/v1.0/bucketlists/`<bucketlist_id>`/items/`<bucketlist_item_id>` | DELETE |   | token

![delete a bucketlist with Postman](https://gyazo.com/eae1197f708243dcc01b7036f9e90be3.gif)


# IMPLEMENTATION

### Config File
Two config files are used, 'test_config.py' and 'development_config.py' for testing and development/production environment respectively.

### Authentication
Tokens are used for authentication. You first create a user and create a token with the username and password. **Tokens expire after every 20mins.** Remember to always include a token variable in the header when making requests, except when creating a user.


# TESTS
Run `coverage run test_bucketlist.py`

# CREDITS
God and my two guardian angels(:angel: Google and Stackoverflow:angel:).
Also got some great insights from the following links:

- [http://flask.pocoo.org/snippets/22/](http://flask.pocoo.org/snippets/22/)
- [http://docs.sqlalchemy.org/en/rel_0_5/index.html](http://docs.sqlalchemy.org/en/rel_0_5/index.html)

# LICENSE
Free
