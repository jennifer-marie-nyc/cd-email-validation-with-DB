from mysqlconnection import connectToMySQL
from flask import flash
import re

class User:
    DB = 'users_schema'
    def __init__(self, data):
        self.id =  data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.DB).query_db(query)
        all_users = []
        for user in results:
            all_users.append(cls(user))
        return all_users
    
    @classmethod
    def validate_user(cls, user):
        is_valid = True
        if len(user['fname']) <= 0:
            flash('First name is required.')
            is_valid = False
        if len(user['lname']) <= 0:
            flash('Last name is required.')
            is_valid = False
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email format.')
            is_valid = False
        #Validate that the email being added is unique
        existing_users = cls.get_all()
        email_exists = False
        for existing_user in existing_users:
            if existing_user.email == user['email']:
                email_exists = True
        if email_exists and len(user['email']) > 0:
            flash('Email already exists.')
            is_valid = False
        print("VALIDATING USER")
        return is_valid
    
    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, NOW(), NOW());'
        return connectToMySQL(cls.DB).query_db(query, data)