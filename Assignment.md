
# Narma - Stay connected off-grid with the Narma Network

---
## Purpose and Scope (R1&2)

Today, accessing content on the internet requires spending time on applications, such as YouTube, instagram, Twitter, TikTok. This content is largely distributed via an algorithm that is trained by the user's activity on the application. This paradigm, enforced by companies to increase advertising revenue by maintaining a user's attention, can encourage addictive behaviours and lead to an unhealthy reliance on the technology. 

It is especially harmful for people with anxiety and depression, particularly in younger demographics, who are more succeptable to a lower self esteem and rumination. 

Narma aims to be a solution to this problem by providing users access to content they are interested in, albiet in healthy doses throughout the day via direct messages. 

At its core, Narma is a one-way messaging app between users and the application's simulated users - called the 'narma' network. It is designed to permit the consumption of content without demanding time spent searching for content. 

Narma aims to:
 1. let users remain connected to the online world while unplugging from social media
 2. provide advice and resources to help with mental struggles or social interactions (e.g. conversation starters, date tips) 
 3. generate a sense of support during times of lonliness and isolation

## Why Postgres as a Database 

<u>Relational functionality</u>

Messaging applications rely heavily on the interaction between users. Often, in-app messages exhanged between a sender and receiver are stored as individual entries within a table that references the <em>user</em> entity. Given this, Narma required a relational database that can implement this table linking logic. Postgres was chosen as the database management systems for narma for its seamless compatibility with Flask and the python language. It is also in flexible in its ability to work with user-defined data types (including JSON) and custom functions.(PostgreSQL, N.d.). 


Postgres was suitable for the app for its simple implementation of cascading, which was central to the Narma app whereby if a user unfollowed a particular simulated_user, both the conversation and messages within the conversation needed to be deleted. An example of this implementation is presented below:

```python
## from the User Model

connection = db.relationship('Connections', back_populates='connections', cascade='all, delete')

## from the Connection Model

user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 

```

Given the potential high frequency of messaging within the app, and the extensive volume of data which is required to be stored for each message sent was an additional reason to implement Postgres as the apps database. Postgres is robust for a range of large file data types, and is measurably more effiecent in storing blobs and images comapred with MySQL (Kavin, 2022).

When compared to other SQL-reliant database systems (such as MySQL), postgres generally suffers from lower speeds and is particularly inefficient in establishing client connections which cost 10mb memory each (Hirstozov, 2019). To deal with this, connection pooling is often implemented between to handle high volumes of client connections. PgBouncer is a widely used postgresql connection pooler module. 

## R4 Functions and Benefits of ORM implementation

Storing, maniplating and retrieving data within an app's database is commonly implemented with an object-relational-mapper plugin. ORMs translate database tables to objects, meaning data handling within the app can follow the developers native Object-oriented-programming (OOP) paradigm. The main functions of an ORM is:

 1. Connecting to, then referencing a database using limited lines of code:

The fundamental functionality of an ORM is to connect a remote database to a backend application (e.g. API). A commonly used python ORM is SQL Alchemy, and the way it connects to a running db server is as simple as declaring the SQL Alchemy ORM as a variable in your backend app. To reference this connection (e.g. retieve and store data in the db), all that needs to be done is to call this variable. The connection is initialised using the relevant database URI:

```python

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db.init_app(<variable storing your app>)
```

 2. The ability to interact with the database infrastucture remotely (db/table creation, seeding)

When an ORM has connected with a remote database, it has the core functionality of setting up and modifying its infrastructure, that is, creating, deleting, modifying and seeding tables. SQL Alchemy can be connected to the terminal within a running program (e.g. flask app) with a cli python decorator. This provides the ability to complete these actions with as little as two words:

```python
    # delete all tables
    @app.cli.command('drop')
    def drop_db():
        db.drop_all()
        print('Tables dropped')
    #create all tables 
    @app.cli.command('create')
    def create_db():
        db.create_all()
        print('Tables created')
```
Can be activated in the terminal:

```bash
$ flask drop
>>> Tables dropped
$ flask create 
>>> Tables created
```

3. The ability to create classes which represent db tables (table fields become object attributes):

```python
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10), nullable = False)
    email = db.Column(db.String, nullable = False) 
    password = db.Column(db.String, nullable = False)
    gender = db.Column(db.String, nullable = False)
    age = db.Column(db.Date, nullable = False)
    connections = db.relationship('Connections', back_populates='user', cascade = "all, delete")
    likes = db.relationship('Likes', back_populates='user', cascade = "all, delete")
```

Working with classes instead of static tables is far more beneficial to the developer as it adds flexibility to CRUD operations, giving the developer seamless access to each class object anywhere in the program without having to reconnect and query the database with often convoluted SQL statements. It also promotes encapsulation and abstraction. 

 4. The ability to add instances of these classes with several lines of code and no SQL statements:

```python
# create a new entry in the 'users' table (by creating  new instance of the User class/model)
users = [
            User(
                name='Peter',
                email='peter@hotmail.com',
                password='password',
                gender='Male',
                age='25',
            )
            #use the ORM to commit the instance to the database as a new entry:
            db.session.add(users)
            db.session.commit()
```

 5. The ability to take a declared model instance and add it to a db table as a new entry. 

As seen above, adding a new entry (i.e. enacting a INSERT SQL command) to the database is completed in as little as 2 lines by first calling the connected db. Then adding and commiting it to the database session (built in ORM functionis with SQL alchemy). Data seeded above can also be dynamic, for example json data sent by a client program:

```python
def edit_user_profile():
    stmt = db.select(User).filter_by(id = get_jwt_identity())
    user = db.session.scalar(stmt)

    if user: 
        data = UserSchema().load(request.json, partial=True)
    
        user.name = data['name'],
        user.gender = data['gender'],
        user.age = data['age']
        #commit changes to the database 
        db.session.commit()
```

 5. The ability to query the database (translating SELECT statements with native languages):

Allowing developers to query the database without sending raw SQL is a key function of ORMs. Along with any dependancy plug ins required, an ORM can return raw data from a simplified db query and send it as json to a client program. Below is an example of this from a simple GET(READ) route:

```python
@app.route('/data/')
def select_rows():
  stmt = db.select(<tablename>).where(<condition>)
  selection = db.session.execute(stmt)

  #return as JSON with the Marshmallo plug-in
  return <tablename>Schema(many=True).dump(selection)
```


### Additional benefits

Not only does amalgamating SQL methods with OOP methods (seen above) simplifies apps and developer workflows, but sending SQL commands to the db under the hood also (1) simplifies syntax for the developer team [i.e. implementing one language vs multiple] and (2) secures the system against SQL injection attacks. 

By allowing developers to encact SQL commands (e.g. SELECT, INSERT, UPDATE, DELETE) with the apps native language, project management is streamlined as potentially less blockers exist to devs with less experience with SQL. 

Protecting against SQL injections with an ORMS inherent input sanitization is highly effective for endpoints that are protected with authorisation or not. 

By treating tables as python classes, table data can be used like ordinary python data types and structures. This allows devs to easily manipulate table data with standard python syntax and functions, such as data conversion and arithmatic (where needed).

## R5 

All endpoints are documented in the official documentation README of the app (located within the root folder). 

## R6 Narma ERD

The entity relationship diagram below details the proposed tables to be created for the Narma app. It involves 6 entities which represent people, objects and actions all of which are central to the apps operation.

![](/docs/NarmaERD.png)

Users and bots were inherently different entities and thus warranted having their own tables. These are the root tables, which help connect other entities and functions in the app. They are linked by a linking table called Connections which is an entity which represents a user 'following' a bot. Representing this as an entity was important, rather thna just bypassing it to link connections via messages that are sent (e.g. sender vs reciever) as it allowed easy cascade deletion - that is, once a connection is deleted (user ufollows a bot), the messages associated with that conversation is deleted with it. This I felt will increase efficiency in the apps backend greatly particularly later in the apps life.

Messages are the key entitiy in the app and give it purpose. Content within the message is taken from a 'content' entity/table and it is timestamped at time a message is sent. 

In a standard messaging app, the messages entity would usually include the message's content. This allows users to edit their OWN messages. However, since Narma is a one-way messaging app, where bot messages are written once and sent to potentially +million users, it was necessary to isolate the message 'content/body' into its own model/table. Having an isolated content table takes into consideration potential company workflows:  for example, company staff admins will be able to upload content at will before it is sent to users in order to be checked/evaluated by supervisors. 

Once messages are created (and accessible to users), they are permitted to be 'liked'. Although these messages are technically automated, messsage likes are designed to provide feedback to , and later down the track could be used to train an AI model that would help reccomend what content certain users are interested in. The likes table is to be related to the message via message_ID FK and to a user by user_id. A user can only like one message and this will be impletemtned with conditional python logic within a 'like' controller.

<em>Note: minor changes were eventually made to the ERD, such as the addition of fields within the Bot_profile table (profile picture, age).</em>

## R7 3rd party services and modules

<u>PsycoPg2</u>

PsycoPg2 is a database adaptor module which is used to connect the flask server with the database server.

<u>SQL Alchemy</u>

SQL Alchemy is an ORM plugin used to manage, query and manipulate the postgres database without SQL. Its role is to contextualise db tables as python classes so that data can be manipulated easily as python data types which allows seamless conversion and calculation (where needed). 

<u>Marshmallow</u>

Marshmallow is a json serializer frequently used in conjunction with SQL Alchemy. It is used in the Narma API to translate python data types rendered from ORM models into serialised json, or incoming client json into python-friendly data types. Built into marshmallow is data validation which was used to ensure data recieved from client requests is consistent with what is required for the database. E.g. permitted data sizes and consistent data types.

<u>Bcrypt</u>

Bcrypt is a flask plugin used to encrypt and salt user passwords. It was used on each password sent to the API via client response before it was stored in the database. It was also used to decypt in order to cross-check user password inputs during 'login':

```python
@auth_bp.route('/register/', methods=['POST'])
def auth_register():

    data = UserSchema().load(request.json, partial=True)
    user = User(
        name = data['name'],
        email = data['email'],
        password = bcrypt.generate_password_hash(data['password']).decode('utf8'),

@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    #Locate the user account
    stmt = db.select(User).filter_by(email=request.json.get('email'))
    #store the selected entry into a variable
    user = db.session.scalar(stmt)

    #if user exists and password is correct
    if bcrypt.check_password_hash(user.password, request.json.get('password')):
        #then provide them with a token
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))

```

<u>JWT Manager</u>

All users are authenticated with bearer tokens specifically, Json web tokens (JWT). The JWT manager from flask was used to generate tokens when a client json password matched the encrypted password stored in the database (see example above). This token is used to stake claims to resources behind secured enpoints. 

<u>Phone number validator 'phonenumbers'</u>

The <em>phonenumbers</em> package is the python port of Google's libphonenumber which uses a database of registered numbers from carriers all over the world. When used for validation (as seen in the example below) it not only checks for number syntax, but cross-references it with the built-in carrier database. Phonenumbers is an open source package and was used in the Narma API to detract and physically limit non-human (bot) user registeration. 

```python
    #3rd party phone number validator:
    @validates('phonenumber')
    def validate_phonenumber(self, phonenumber):
        check = carrier._is_mobile(number_type(phonenumbers.parse(phonenumber)))
        if check is False:
            raise ValidationError("Phone number is not valid")
```

## R8 Describe the Narma models

The app has 6 models that represent 6 entities expressed in the database. Each model stores data that relate to either a type of user (e.g. a user or a bot) or type of app function (e.g. following a bot, liking a bot's message). 

1. Bots model: ID, name, gender, bio, and display picture 

Bots are a 'simulated' user that is created, edited, actioned and deleted by admin users. They each have a unique background and are 'followed' by regular users. Admins upload messages on behalf of bots that get distributed to each of their followers. Bots are related to Users via the 'connections' linking model in a one-to-many relationship using  bot_id as a foreign key. This relationship essnetially represents a user following a bot. As a root model, the bot model is referenced many times in the app for instance when data is requested for user connections or when messages are sent or requested for rendering within a view.

2. Users model: ID, name, gender, age, email and password, is_admin (bool)

The users model encapsulates information from public users of the app. It also grants admin roles to authourised company users accessed by the <em>auth</em> controller. The Users schema is validated using 'Marshmallow.validate'. It not only makes all fields required, but enforces rules for user inputs for each field such as letter count for strings as well as valid input options for categorical gender data. An example of this validation is presented below:

```python 
#validation rules
    name = fields.String(required=True, validate=Length(min=2))
    email = fields.String(required=True, validate=Length(min=10))
    password = fields.String(required=True, validate=And(Length(min=8), Regexp('^[a-zA-Z0-9]')))
    gender = fields.String(required=True, validate= OneOf(VALID_GENDERS))
    age = fields.Integer(required=True, validate=Range(min=16, max=99))

```

The model schema also enforces that user email and password are unique within the database so that no duplicate passwords or emails can exist. This means that the PATCH route that edits user data only handles and returns data relating to name, gender and age:

```python
@users_bp.route('/edit_profile/', methods=['PATCH'])
@jwt_required()
def edit_user_profile():
    stmt = db.select(User).filter_by(id = get_jwt_identity())
    user = db.session.scalar(stmt)

    if user: 
        data = UserSchema().load(request.json, partial=True)

        #users can only edit their name, gender and age
        user.name = data['name'],
        user.gender = data['gender'],
        user.age = data['age']

        #add and commit to the database 
        db.session.add(user)
        db.session.commit()

        #respond to client with changed data
        return UserSchema().dump(user)

```

Like the bot model, the user model is considered a root model, and relates with Bot via the connections model in a many-to-one relationship using the user_id as a foreign key.

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

SQL Alchemy also requires this relationship to be recorded in both the Bot and User models (representing the one-to-many part of the realtionship). Bot and User data can be accessed by referencing this connections model as connections shares a one to many relationship with the Messages model, in that each message belongs to a single connection (i.e. has one user as the recipient and one bot as the sender) and each connection can have many messages.

4. Messages model: 

The messages model comprise individual entries (instances) inclusive of an ID, Content and a Connection ID foreign key that links the message to a connection. In other words each entry acts as 'message' and can be accesed/edited/deleted with the API either by its ID (sinlge message), Bot_id (all messages sent by a bot - admin only), all messages sent by a single bot to a logged in user, or user_id (which returns all messages sent to a particualar user from all the bots they follow). It shares a many-to-one relationship with the Connections Table, signalling that a message can only belong to one connection, yet each connection can have multiple messages associated with it. 

5. Likes model: ID, Connection ID (FK), user_id (FK)

The Likes model is used to represent the likes table within the database which is used to store each time a user 'likes' a message. In a front end program this may be represented as a 'thumbs-up' icon. The likes model shares a many-to-one relationship with the Messages model as each message may have multiple likes, but a user's like can only belong to a single message. Cascade deletion was implemented in the Messages model so that all Likes (which are back referenced to the Messages table) are also deleted with the deleted message:

```python
class Likes(db.Model):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    user = db.relationship('User', back_populates = 'likes')
    message_id = db.Column(db.Integer, db.ForeignKey("messages.id"), nullable = False)
    message = db.relationship('Messages', back_populates = 'likes', cascade = 'all, delete')
```

The above 5 models are sufficient for a standard messaging app, where users are all alike and can send and edit their OWN messages. However, since Narma is a one-way messaging app, where bot messages are written once and sent to potentially +million users, it was necessary to isolate the message 'content/body' into its own model/table. This is because with the original 5 model framwork, an admin editing a message would need to do so for however many messages it belonged to. It was decided late into planning that although this only affected message PATCH requests, it was best to normalise the messages table to isolate message as it assited potential company workflows:  for example, company staff admins will be able to upload content at will before it is sent to users in order to be checked/evaluated by supervisors. 

6. Content: id, bot_id(FK), content (varchar)

The Content model represents the content table which holds message contents belonging to a particular bot. Content held within the model is back-related to the bot model with a one to many relationship, that is - a bot can have more than one piece of content stored, however content can only belong to a single bot. This helps bots maintain their unquieness, given that each one has their own background and interests - their content should match this. Content is taken from the content model and fed into a message with the one-to-one relationship shared between the content and messages model. This means one piece of content can only belong to one bot and one message, and one message can only contain one piece of content.

## R9 describe db relations 

Six relations/tables were created for the Narma API, as seen in the ERD:

![](/docs/NarmaERD.png)

The realationships between each table has been discussed under the context of entities and models. This section will describe each realtion (table) in its own context.

Users:

This table contains user information and is used heavily during authentication. It is also used in refferencing by other related tables. All fields are required for validation purposes. Along with a serialised ID primary key, each user has stored their full name (string(20)), email address(string(50 - syntax validated by Marshmallow.Email)), password(string(8)-encrpyted/salted by Bcrypt), age (Date YYYY-MM-DD) - this is so ages can be auto updated by the client and also used as a vetting processed as only users over the age of 16 are permitted to be stored. Gender is also a requred field however, To make client forms simple, only 4 valid options exist: Male, Female, Non-binary and Other. The user table also contains an 'is_admin' column which is a boolean field indicating whether the user is authorised to access admin-only endpoints. Email and Password are unique fields, intending only one of each can be stored in the database.

Bots:

This table contains Narma bots, who are simulated users. Each entry (bot) has an id (PK), first name (string(15)), gender (with the same 4 valid string options as public users), as well as a bio (text(100)), age (integer) and display picture (VARCHAR(1000)). 

Connections: 

This table is a linking table for users and bots. It shares a many-to-one relationship with them both. It contains an ID primary key, as well as user_id and bot_id fields as foreign keys. Each field is not nullable. 

Messages:

The messages table contains each message sent between a bot and a user, i.e. a message per connection. It is therefore related to the connections table, by connection_id FK and can access the bot - i.e. sender of the message, and user - i.e. receiver of the message. Each message (entry) is timestamped upon storage (sending). The timestamp column is a DateTime Postgres datatype. Each column is not nullable. The content_id (integer) is a ForeignKey for the content table, the table where messasge content is stored and accessed. Each message is created by calling this relationship and taking the chosen content using the content model. 

Content:

The content table was created to store message content so that content could be edited once, instead of admins having to edit the content within each message a bot sends. It includes an id (primary key), it is linked to the bot table (as content genre is specific to each bot) by bot_id a foreign key. Content itself is stored as a varchar(1000) so it can contain text, video/webpage URLS or image files. 

Likes:

The likes table is to contain entries that represent 'likes' on a message. For instnace when a client sends a request to add a user like to a message, a new entry is made with an id (PK), as well as informaton about the message (using message_id as a foreign key) as well as the user who liked it (using the user_id as foreign key). This makes it easy for the client to calculate total likes (for instance) by just accessing a count of likes entries by user (an endpoint included in the Narma API). 


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

## References 

Hirstozov, K. 2019. MySQL vs PostgreSQL - Choose the right database for your project. https://developer.okta.com/blog/2019/07/19/mysql-vs-postgres. Accessed 10/11/22

Saravanan, Kavin, "The Comparison of Database Management Systems on the Speed of Analysis by Artificial Intelligence" (2022). South Carolina Junior Academy of Science. 2.
https://scholarexchange.furman.edu/scjas/2022/all/2 

PostgreSQL Documentation. N.d. About. https://www.postgresql.org/about/. Accessed 6/11/22.