
Narma - Stay connected off-grid with the Narma Network

---
## Purpose and Scope

Today, content on the internet is accessed by users visiting applications such as Instagram, TikTok and Youtube. This content is distributed via an algorithm that is trained by the user's activity on the application. This paradigm, enforced by companies to increase advertising revenue by maintaining a user's attention, can encourage addictive behaviours and lead to a unhealthy reliance on the technology. 

It is especially harmful for people with anxiety and depression, particularly in younger demographics, who are more succeptable to a lower self esteem and rumination. 

Narma aims to be a solution to this problem by providing users access to content they are interested in albiet in healthy doses throughout the day via text messages. 

At its core, Narma is a one-way messaging app between users and the application's simulated users - called the 'narma' network. It is designed to permit the consumption of content without demanding time spent searching for content. 

## Database 

Relational functionality 

Messaging applications rely heavily on the interaction between users. Often, in-app messages exhanged between a sender and receiver are stored as individual entries within a table that references the <em>user</em> entity. Given this, Narma required a relational database that can implement this table linking logic. Postgres was chosen as the database management systems for narma for its seamless compatibility with Flask and the python language. It is also in flexible in its ability to work with user-defined data types (including JSON) and custom functions.(PostgreSQL, N.d.). 


Postgres was suitable for the app for its simple implementation of cascading, which was central to the Narma app whereby if a user unfollowed a particular simulated_user, both the conversation and messages within the conversation needed to be deleted. An example of this implementation is presented below:

```python
## from the User Model

connection = db.relationship('Connections', back_populates='connections', cascade='all, delete')

## from the Connection Model

user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 

```

Given the potential high frequency of messaging within the app, and the extensive volume of data which is required to be stored for each message sent was an additional reason to implement Postgres as the apps database. Postgres is robust for 

When compared to other SQL-reliant database systems (such as MySQL), postgres suffers from lower speeds 


# Endpoint/route Documentation
---



## Authentication Endpoints
---



## User endpoints 
---




## Bot endpoints 
---







## R8 Describe models

The app has 5 models that represent 5 entities expressed in the database. Each model stores data that relate to either a type of user (e.g. a user or a bot) or type of app function (e.g. following a bot, liking a bot's message). 

1. Bots model: ID, name, gender, bio, and display picture fields

Bots are a 'simulated' user that is created, edited, actioned and deleted by admin users. They each have a unique background and are 'followed' by regular users. Admins upload messages on behalf of bots that get distributed to each of their followers. 

2. Users model: ID, name, gender, age, email and password, is_admin (bool)

The users model encapsulates information from public users of the app. It also grants admin roles to authourised company users. 

3. Connections: 

Connections is essentially a model that represents a linking table between users and bots (ID FKs) that symbolise users 'following' bots. Once a user follows a bot, a Connection instance is created with a unique ID and a user_id (follower) plus bot_id (followed). It is related to the bot and user models using the built-in sql alchemy function db.realtionship: 

```python
# this is the model
class Connections(db.Model):
    __tablename__ = 'connections'
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    user = db.relationship('User', back_populates = 'connections')
    bot_id = db.Column(db.Integer, db.ForeignKey("bots.id"), nullable = False)
    bot = db.relationship('Bot', back_populates = 'connections')


# this is the schema
class ConnectionsSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=['password', 'connections'])
    bot = fields.Nested('BotSchema')

    class Meta:
        model = Connections
        fields = ('id', 'user', 'bot')
        ordered = True 

```

SQL Alchemy also requires this relationship to be recorded in both (representing the one-to-many part of the realtionship).

4. Messages model: 

The messages model comprise individual entries (instances) inclusive of an ID, Content and a Connection ID foreign key that links the message to a connection - e.g. the bot sender and user reciever in the connections table

5. Likes model: 

## R9 describe db relations 



## R10 project managemnet with Trello

Tasks are allocated and tracked using the app Trello. The agile framework used was Kanban, which involves the open communication of tasks (broken down as checklists that follow user stories) and their delegation between future, current and completed statuses. 

My Kanban board included the following cards:

1. To-do: All tasks were initally posted here and one-by-one were advanced to the Doing board
2. Doing: Tasks here were in the middle of being compelted. There were times when multiple cards were      posted here depening on the complexity of the card or whether blockers were met. 
3. Testing: Testing came in the form of manually sending requests to built api routes using the Postman OS software
4. Done: This card holds tasks that have been built and tested and therefore completed.

There was no need for a backlog card as there was no client or manager that would initialise the review process that would otherwise warrant this card. Once tasks were completed and placed in 'done', the card was deemed acceptable and therefore was not able to be re-impleted in the kanban cycle. 

An example of the board can be seen bellow

![](/docs/trello%20in%20progress2.png)

An example of a task can be seen below

![](/docs/task_example_trello.png)

Trello link: https://trello.com/invite/b/vy1F5ABe/ATTI8da6eacdffe70c02c7465565d6423fbc3132416B/narma-backend

