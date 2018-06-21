from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
import re

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2 or len(postData['name']) > 255:
            errors['name'] = "Your name must be at least 2 characters"

        if len(postData['alias']) < 2 or len(postData['alias']) > 255:
            errors['alias'] = "Alias must be at least 2 characters"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email_invalid'] = "The email you entered is not valid."

        if len(postData['email']) < 8 or len(postData['email']) > 255:
            errors['email_length'] = "Email must be at least 8 characters long."

        elif Users.objects.filter(email = postData['email']):
            errors['email'] = "The email you entered has already been taken! Please log in."

        if len(postData['password']) < 8 or len(postData['password']) > 255:
            errors['password'] = "Password must be at least 8 characters long."
        
        elif len(postData['pw_confirm']) < 8 or len(postData['pw_confirm']) > 255:
            errors['pw_confirm'] = "Password must be at least 8 characters long."
        elif postData['password'] != postData['pw_confirm']:
            errors['password'] = "Your passwords do not match!"
        
        if len(errors):
            errors['valid'] = False
            return errors

        else:
            new_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            create_user =  Users.objects.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = new_pw)
            new_user = create_user.id
            return new_user

    def basic_validator2(self, postData):
        errors = {}
        user = Users.objects.filter(email = postData['email2'])
        if len(user):
            if bcrypt.checkpw(postData['password2'].encode(), user[0].password.encode()) == True:
                return user
            else:
                errors['invalid_email'] = "The email address or password you entered was not valid."
                return errors
        else:
            errors['empty'] = "Please enter a valid email address and password."
            return errors
    
    def basic_validator3(self, postData, my_id):
        errors = {}

        Review.objects.create(review = postData['review'], rating=postData['rating'], book = Books.objects.get(id = postData['book_id']), user = Users.objects.get(id = my_id) )
        return errors

    def basic_validator4(self, postData, my_id):
        errors = {}

        new_book = Books.objects.create(name = postData['title'], author = postData['author'], user = Users.objects.get(id = my_id))
        new_book.save()
        new_id = new_book.id
        Review.objects.create(review = postData['review'], rating = postData['rating'] , book = Books.objects.get(id = new_id) ,user = Users.objects.get(id = my_id))
        return new_book

class Users(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"{self.name} {self.alias}"

class Books(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    user = models.ForeignKey(Users, related_name="added_book")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __repr__(self):
        return f"{self.name} {self.author}"

class Review(models.Model):
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Books, related_name="reviewed_books")
    user = models.ForeignKey(Users, related_name="reviewer")
    objects = models.Manager()

    def __repr__(self):
        return f"{self.review} {self.rating}"
