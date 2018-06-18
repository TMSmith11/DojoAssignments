# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.db import models 
import bcrypt
import re

EMAIL_PATTERN = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

# Create your models here.

class UserManager(models.Manager):

    def validate_login(self, post_data):
        errors = []
        user = None

        if not self.filter(username = post_data['username']):
            errors.append('Invalid username/password')

        else:
            user = self.get(username=post_data['username'])
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('Invalid username/password')

        return errors, user

    def validate_registration(self, post_data):
        errors = []
        user = None

        #check for any empty fields
        for key, value in post_data.iteritems():
            if len(value) < 1:
                errors.append('All fields are required')
                break

        #check for minimum length on name
        if len(post_data['name']) < 3:
            errors.append('Name requires at least 3 characters')
        
        #check for minimum length on username
        if len(post_data['username']) < 3:
            errors.append('Username requires at least 3 characters')

        #check if password matches confirm password
        if post_data['password'] != post_data['password_confirm']:
            errors.append('Passwords do not match')
        
        #creates user
        if not errors:
            hashed_pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())

            user = self.create(
                name = post_data['name'],
                username = post_data['username'],
                password = hashed_pw
            
            )
        return errors, user

class DestinationManager(models.Manager):
        
    def validate_destination(self, post_data,user_id):
        errors = []
        destination = None
        for key, value in post_data.iteritems():
            if len(value) < 1:
                errors.append('All fields are required')
                break
             
            current_date = datetime.now()
            if datetime.strptime(post_data['start_date'], '%Y-%m-%d') < current_date:
                errors.append('Enter valid dates')

            if datetime.strptime(post_data['end_date'], '%Y-%m-%d') < current_date:
                errors.append('Enter valid dates')

            if post_data['start_date'] > post_data['end_date']:
                errors.append('Enter valid start date')

            if not errors: 
                d = Destination()
                d.destination = post_data['destination']
                d.description = post_data['description']
                d.start_date = post_data['start_date']
                d.end_date = post_data['end_date']
                d.save()
                d.users.add(User.objects.get(id=user_id))

                d.save()

                return errors, d
            
        return errors, []

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=250, default='pw')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Destination(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(max_length=100)
    end_date = models.DateField(max_length=100)
    users = models.ManyToManyField(User, related_name='destinations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DestinationManager()


