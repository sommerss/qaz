""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db


from sqlalchemy.exc import IntegrityError



''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Snakes(db.Model):
    __tablename__ = 'Snakes'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _snakescore = db.Column(db.String(255), unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, snakescore):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self._snakescore = snakescore
        
        

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    

    
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def snakescore(self):
        return self._snakescore
    
    # a setter function, allows name to be updated after initial object creation
    @snakescore.setter
    def snakescore(self, snakescore):
        self._snakescore = snakescore



    
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            
            "snakescore": self.snakescore
            
           
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", snakescore=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(snakescore) > 0:
            self.snakescore = snakescore
        
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initSnakes():
    with app.app_context():
        
        
        db.create_all()
    
        s1 = Snakes(name='sabine', uid='sab', snakescore = 10)
        s2 = Snakes(name='xxx', uid='xxx', snakescore = 20)
        s3 = Snakes(name="bob", uid="bobby", snakescore=30)

        snakes = [s1, s2, s3]

        
        for snake in snakes:
            try:
                 '''add user/post data to table'''
                 snake.create()
            except IntegrityError:
                 '''fails with bad or duplicate data'''
                 db.session.remove()
                 print(f"Duplicate email, or error: {snake.uid}")