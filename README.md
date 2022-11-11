# NARMA Documentation


This documentation contains information pertaining to the use of the backend API webserver for the Narma app. 

---

## What is Narma?

Narma is a one-way messaging application. Messages are sent by simulated users (currently run by company admins) to their followers (public users). 

Content within these messages is general in nature, but is intended to support people struggling with depression, anxiety and addiction. It ranges from comedic internet content, news and current affiars, movie and book reccomendations, dating advice, and mental health resources. Each Narma bot has a unique background and persona, which is translated into the content they message to their Followers. 

## How to install

Program files can be downloaded with the following curl command:

```bash

```

Open the program directory in a IDE of your chosing then proceed to create and initialise a realtaional database with (postgres prefered) on port 5432 of your local machine. 

Since the project is still in developement, the API ORM adaptor comes with the database name and password that was initially used when the API was built. For quick start, set up a database called narma_app with the password of medic2. 

To create a custom db, ensure you modify the database adaptor string within the program's .env file with your chosen database name and password:

```python
### .env file

DATABASE_URL=postgresql+psycopg2://postgres:<password>@127.0.0.1:5432/<database_name>

```

When initialising a non-postgres database with the Narma API, it is advised to consult the documentation on how best to connect your database with the flask app.

## Endpoint documentation
---

### Admin_only routes

<u>USER</u>

/users/

- Method: GET
- args: none
- Authentication: bearer{token}
- Authorisation: admin (bool)
- Description: returns
- request body: none
- response body:

```json
{
    "id"
    "name"
    "email"
    "gender"
    "age"
    "connections(FK):
} 
```

/users/\<int:id>/delete/

- Method: DELETE
- Args: user_id
- Description: deletes a user 
- Authentication: bearer(Token)
- Authorisation: admin (bool)
- request body: none
- resquest response: 

```json
{"message" : "User has been successfully deleted"}
```

<u>MESSAGES</u>

/messages/\<int:id>/send/

- Method: POST
- Args: bot_id
- Description: sends a message to a bots followers
- Authentication: bearer(token)
- Authorisation: admin (bool)
- Request body:

```json
{
    "content_id"
} 
```

- Response body:

```json
{
    "success" : "Messages have been sent"
}
```

/messages/<int:id>/all/

- Method: GET
- Args: bot_idbot_id
- Description: returns all messages from a  specific bot
- Request body: none
- Response body:

```json
{
    "id"
    "connection_id"
    "content"
    "datetime"
}
```

/messages/\<int:id>/delete/

- Method: DELETE
- Args: bot_id
- Authentication: bearer(token)
- Authorisation: admin (bool)
- Description: allows admins to delete a specific message
- Request Body: none
- Response body:

```json
{"success" : "message has been deleted"}
```

<u>CONNECTIONS</u>

/connections/all_connections/

- Method: GET
- Args: none
- Authentication: bearer(token)
- Authorisation: admin (bool)
- Description: Returns all connections to admin
- Request body: none
- Response body:

```json
[{
        "id":,
        "user": {
            "id"
            "name"
            "email"
            "gender"
            "age"
        },
        "bot": {
            "id"
            "name"
            "bio"
            "gender"
            "picture"
        }
    },
]
```

<u>BOTS</u>

/bots/add/

- Method: POST
- Args: none
- Authentication: bearer(token)
- Authorisation: admin (bool)
- Description: creates a new bot
- Request body:

```json
{
    "name"
    "bio"
    "gender"
    "picture"
}
```

- Response body:

```json
{
    "id"
    "name"
    "bio"
    "gender"
    "picture"
}
```

/bots/\<string:name>/edit/>

- Method: PATCH 
- Args: bot_name
- Authentication: bearer(token)
- Authorisation: admin (bool)
- Description: updates/edits an existing bot
- Request body:

```json
{
    "name"
    "bio"
    "gender"
    "picture"
}
```

- Response body:

```json
{
    "id"
    "name"
    "bio"
    "gender"
    "picture"
}
```

/bots/\<int:id>/delete/>

- Method: DELETE
- Args: id
- Authentication: bearer(token)
- Authorisation: admin (bool)
- Description: deletes an existing bot
- Request body: none
- Response body: 

```json
{
    "message" : "bot deleted successfully"
}
```

<u>CONTENT</u>

/content/\<string:name>/all/

- Method: GET
- Args: bot name
- Authentication: bearer(Token)
- Authorisation: admin (bool)
- Description: returns all content uploaded for the specified bot
- Request body: none
- Response body:

```json
[{
    "content", 
    "bot_id",
    "bot" {
        "name"
        "picture"
    },
    
}]
```

/content/<int:id>/

- Method: GET
- Args: content_id
- Authentication: bearer(Token)
- Authorisation: admin (bool)
- Description: returns a specific piece of content specified by id
- Request body: none
- Response body:

```json
{
    "content", 
    "bot_id",
    "bot" {
        "name"
        "picture"
    },
    
}
```

/content/<string:name>/add/

- Method: POST 
- Args: bot_name
- Authentication: bearer(Token)
- Authorisation: admin (bool)
- Description: returns a specific piece of content specified by id
- Request body: 

```json
{
    "bot_id"
    "content" (VARCHAR)

}
```

- Response body:

```json
{"message" : "content uploaded successfully"},
    
}
```

/content/<int:id>/edit/

- Method: POST 
- Args: content_id
- Authentication: bearer(Token)
- Authorisation: admin (bool)
- Description: returns a specific piece of content specified by id
- Request body: 

```json
{
    "bot_id"
    "content" (VARCHAR)

}
```

- Response body:

```json
{"message" : "content updated successfully"},
    
}
```

---

### Authenticated User routes


<u>AUTHENTICATION</u>

/auth/register/

- Method: POST
- Args: None
- Authentication: none
- Authorisation: none
- Description: Create a user account 
- Request body:

```json
//  NOTE: age is type DATE, in format YYYY-MM-DD
{
    "name"
    "email"
    "password"
    "gender"
    "age"
}
```

```json

- Request body:

```json
{
    "name"
    "email"
    "password" (encrypted/salted)
    "gender"
    "age" (YYYY-MM-DD)
}
```

/auth/login/

- Method: POST
- Args: none
- Authentication: bearer(token)
- Authorisation: none
- Description: user is authenticated and provided a session token 
- Request body:

```json
{
    "email"
    "password"
}
```

- Request body:

```json
{
    "name"
    "token"
}
```


<u>USERS</u>

/users/profile/

- Method: GET
- Args: none
- Authentication: bearer(token)
- Authorisation: none
- Description: returns the logged in user's profile
- Request body: none
- Response body: 

```json
{
    "id"
    "name"
    "email"
    "gender"
    "age"
    "connections": (list)
}
```

/users/current/edit_profile/

- Method: PATCH
- Args: none
- Authentication: bearer(token)
- Authorisation: none
- Description: edits the logged in user's profile with request body data
- Request body:

```json
{
    "name"
    "gender"
    "age"
}
```

- Response body:

```json
{
    "id"
    "name"
    "email"
    "gender"
    "age"
    "connections" (list)
}
```

/users/current/delete_account/

- Method: DELETE
- Args: none
- Authentication: bearer(token)
- Authorisation: none
- Description: deletes a logged in user's account
- Request body: none
- Response body: 

```json
{
    "message" : "User has been successfully deleted"
}
```

<u>MESSAGES</u>

/messages/\<string:name>/

- Method: GET
- Args: bot_name 
- Authentication: bearer(token)
- Authorisation: none
- Description: returns messages sent to the logged in user from a specified bot
- Request body: none
- Response body:

```json
{
    "message" : "No messages yet"
}
```

<u>LIKES</u>

/likes/message/like/

- Method: POST
- Args: none 
- Authentication: bearer(token)
- Authorisation: none
- Description: Route for logged in user to 'like' a message
- Request body: 

```json
{
    "message_id"
}
```

- Response body:

```json
{
    "message" : "message {message_id} was liked by {logged in user}"
}
```

/likes/message/unlike/

- Methods: DELETE
- Args: none
- Authentication: bearer(token)
- Authorisation: none
- Description: Route for logged in user to 'unlike' a message
- Request body:


```json
{
    "message_id"
}
```

- Response body:

```json
{
    "message" : "message {message_id} was unliked by {logged in user}"
}
```

<u>CONNECTIONS</u>

/connections/following/

- Method: GET
- Args: none
- Authentication: bearer(token)
- Authorisation: none
- Description: Route for logged in user to show who they are connected with
- Request body: none
- Response body:

```json

    [
    {
        "id": 
        "user": {
            "id" 
            "name"
            "email"
            "gender"
            "age"
        },
        "bot": {
            "id"
            "name"
            "bio"
            "gender"
            "picture"
        }
    }
]
```

/connections/follow/

- Method: POST
- Args: none 
- Authentication: bearer(token)
- Authorisation: none
- Description: Route for logged in user to follow a bot
- Request body:

```json
{
    "bot_id"
}
```

- Response body:

```json
{
    "Success" : "user is now connected with bot {bot_id}"
}
```

/connections/unfollow/

- Method: DELETE
- Args: None
- Authentication: bearer(token)
- Authorisation: none
- Description: Route for logged in user to unfollow a bot (remove connection entry)
- Request body:

```json
{
    "bot_name"
}
```

- Response body:

```json
{
    "Success" : "user is no longer connected with bot {bot_id}"
}
```

<u>BOTS</u>

/bots/

- Method: GET
- Args: None
- Authentication: bearer(token)
- Authorisation: None
- Description: Return a list of all bots 
- Request body: None
- Response body: 

```json
[{
    "id"
    "name"
    "bio"
    "gender"
    "picture" 
},]
```

/bots/\<int:id>/

- Method: GET
- Args: bot_id
- Authentication: bearer(token)
- Authorisation: None
- Description: Return a single bot
- Request body: none
- Response body:

```json
{
    "id"
    "name"
    "bio"
    "gender"
    "picture" 
}
```

/bots/\<string:name/>

- Method: GET
- Args: bot_name
- Authentication: bearer(token)
- Authorisation: None
- Description: returns bot with specified name
- Request body: none
- Response body:

```json
{
    "id"
    "name"
    "bio"
    "gender"
    "picture" 
}
```


---

