Narma - Stay connected off-grid with the Narma Network

---

Today, content on the internet is accessed by users visiting applications such as Instagram, TikTok and Youtube which distribute content via an algorithm which is trained by the user's activity on the application. This paradigm, enforced by companies to increase advertising revenue by maintaining a user's attention, encourages addictive behaviours in most people who 

It is especially harmful for people with anxiety and depression, particularly in younger demographics, who are more succeptable to a lower self esteem, rumination. 

Narma aims to be a solution to this problem by providing users access to content they are interested in albiet in healthy doses throughout the day via text messages. 

At its core, Narma is a one-way messaging app between users and the application's simulated users - called the 'narma' network. It is designed to permit the consumption of content without demanding 

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

 