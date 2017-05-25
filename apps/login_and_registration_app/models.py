# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import UserManager

from django.db import models
import bcrypt
import re

# Create your models here.
EMAIL_REGEX =re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

LETTERS_ONLY = re.compile(r'[A-Za-z]')

class UserManager(models.Manager):
    def validate_and_register(self, data):
        print data, "<<< this is the data"

        errors = []

        replicated = User.objects.filter(email=data['email'])

        if len(data['first_name']) < 2:
            print "First name must be at least 2 characters"
            errors.append("First name must be at least 2 characters")

        if not LETTERS_ONLY.match(data['first_name']):
            print "First name must contain letters only"
            errors.append("First name must contain letters only")

        if len(data['last_name']) < 2:
            print "Last name must be at least 2 characters"
            errors.append("Last name must be at least 2 characters")

        if not LETTERS_ONLY.match(data['last_name']):
            print "Last name must contain letters only"
            errors.append("Last name must contain letters only")

        if len(data['email']) < 1:
            print "Email cannot be blank"
            errors.append("Email cannot be blank")

        if not EMAIL_REGEX.match(data['email']):
            print "Email is not valid"
            errors.append("Email is not valid")

        if len(replicated) > 0:
            print "Email has already been registered"
            errors.append("Email has already been registered")

        if len(data['password']) < 8:
            print "Password must be at least 8 characters long"
            errors.append("Password must be at least 8 characters long")

        if data['password'] != data['confirm_password']:
            print "Passwords do not match"
            errors.append("Passwords do not match")

        if errors:
            return (False, errors)
        else:
            #Bcrypt encryption
            pw = data['password']
            hashed_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

            new_object = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                password = hashed_pw, #<---HASHED PASSWORD
                birthday = data['birthday']
            )
            return (True, new_object)

    def validate_and_login(self,data):

        User_Exists = User.objects.filter(email=data['email'])
        print User_Exists, "<--- replicated"
        errors = []
        if len(data['email']) < 1:
            print "Email and password combination does not exist"
            errors.append("Email and password combination does not exist")
        if not EMAIL_REGEX.match(data['email']):
            print "Email is not valid"
            errors.append("Email is not valid")
        #Check to see if email address entered is in database
        if len(User_Exists) == 0:
            print "Email is not registered"
            errors.append("Email is not registered")
        #validate password (at least 8 characters/ cannot be empty)
        if len(data['password']) < 8:
            print "Password must be at least 8 characters long"
            errors.append("Password must be at least 8 characters long")
        if errors:
            return (False, errors)
        else:
            login_user = User.objects.get(email=data['email'])
            pw = data['password']

            if bcrypt.hashpw(pw.encode(), login_user.password.encode()) == login_user.password.encode():
                print "the passwords match"
                return (True, login_user)
            else:
                print "the passwords DONT match"
                errors.append("Invalid Password")
                return (False, errors)

    def update_user_info(self, data, user_id):

        # Create list to hold errors
        errors = []
        replicated = User.objects.filter(email=data['email'])

        # Check for blank fields
        if len(data['email']) < 1:
            print "Email cannot be blank"
            errors.append("Email cannot be blank")

        if not EMAIL_REGEX.match(data['email']):
            print "Email is not valid"
            errors.append("Email is not valid")

        if len(replicated) > 0:
            print "Email has already been registered"
            errors.append("Email has already been registered")

        if len(data['password']) < 8:
            print "Password must be at least 8 characters long"
            errors.append("Password must be at least 8 characters long")

        if data['password'] != data['confirm_password']:
            print "Passwords do not match"
            errors.append("Passwords do not match")
        if errors:
            return (False, errors, data)

        try:
            pw = data['password']
            hashed_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

            user = User.objects.get(id=user_id)
            user.email = data['email']
            user.password = hashed_pw
            user.confirm_password = data['confirm_password']
            user.save()

        except Exception as e:
            print "there were problems"
            print '%s (%s)' % (e.message, type(e))
            return (False, e)

        return (True,user)

class User(models.Model):
    first_name = models.CharField(max_length = 75)
    last_name = models.CharField(max_length = 75)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 255)
    confirm_password = models.CharField(max_length = 255)
    birthday = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()
