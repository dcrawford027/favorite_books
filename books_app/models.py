from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 chars."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 chars."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        usedEmail = User.objects.filter(email=postData['email'])
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "The email you entered is not valid."
        elif usedEmail:
            errors['email'] = "That email is already registered."
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 chars."
        elif postData['password'] != postData['confirm']:
            errors['password'] = "Your passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        emailExists = User.objects.filter(email=postData['email'])
        if not emailExists:
            errors['email'] = "That email is not registered."
        elif not bcrypt.checkpw(postData['password'].encode(), emailExists[0].password.encode()):
            errors['password'] = "Your credentials do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class BookManager(models.Manager):
    def add_book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "A title is required."
        if len(postData['desc']) < 5:
            errors['desc'] = "Description must be at least 5 chars."
        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    uploaded_by_id = models.ManyToManyField(User, related_name="books_uploaded")
    users_who_like = models.ManyToManyField(User, related_name="liked_books")

    objects = BookManager()